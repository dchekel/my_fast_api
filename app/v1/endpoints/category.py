import asyncio
from typing import Any, Optional
import httpx
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from app.crud import crud_category
# from app.api import deps
from app.v1.api import get_db, get_current_user
from app.core.schemas.category import Category, CategoryCreate, CategorySearchResults, CategoryUpdateRestricted
from app.core.models.models import User

router = APIRouter(prefix="/v1/categories")


# OK
@router.get("/{category_id}", status_code=200, response_model=Category)
def fetch_category(
    # *,
    category_id: int,
    db: Session = Depends(get_db),
) -> Any:
    """
    Fetch a single category by ID
    """
    result = crud_category.category.get(db=db, id=category_id)
    if not result:
        # the exception is raised, not returned - you will get a validation
        # error otherwise.
        raise HTTPException(
            status_code=404, detail=f"Category with ID {category_id} not found"
        )

    return result


# OK
@router.get("/search/", status_code=200, response_model=CategorySearchResults)
def search_categories(
    *,
    keyword: str = Query(None, min_length=3, example="Auto"),
    max_results: Optional[int] = 10,
    db: Session = Depends(get_db),
) -> dict:
    """
    Search for categories based on label keyword
    """
    categories = crud_category.category.get_multi(db=db, limit=max_results)
    results = filter(lambda category: keyword.lower() in category.name.lower(), categories)

    return {"results": list(results)}


# OK
@router.post("/", status_code=201, response_model=Category)
def create_category(
    *,
    category_in: CategoryCreate,
    db: Session = Depends(get_db),
    # current_user: User = Depends(get_current_user)
) -> dict:
    """
    Create a new category in the database. Создание новой категории.
    """
    print('router.post create_category', category_in.name)
    # print('current_user.id=', current_user.id, current_user.email)
    # if category_in.submitter_id != current_user.id:
    #     raise HTTPException(status_code=403, detail=f"You can only submit categories as yourself")
    category = crud_category.category.create(db=db, obj_in=category_in)

    return category


@router.put("/", status_code=201, response_model=Category)
def update_category(
        *,
        category_in: CategoryUpdateRestricted,
        db: Session = Depends(get_db),
        current_user: User = Depends(get_current_user)
) -> dict:
    """
    Update category in the database.
    """
    print('router.put update_category', category_in.name, category_in.id)
    print('category_in=', category_in)

    category = crud_category.category.get(db, id=category_in.id)
    print('category=', category.name, category.id)
    if not category:
        raise HTTPException(status_code=400, detail=f"Category with ID: {category_in.id} not found.")

    if category.submitter_id != current_user.id:
        raise HTTPException(status_code=403, detail=f"You can only update your categories.")

    updated_category = crud_category.category.update(db=db, db_obj=category, obj_in=category_in)

    print('updated_category=', updated_category)
    return updated_category


# убрать имя в запросе
@router.delete('/delete/{category_id}/', status_code=201, response_model=Category)
async def delete_category(
        *,
        category_in: CategoryUpdateRestricted,
        db: Session = Depends(get_db),
):
    deleted_category = crud_category.category.remove(db=db, id=category_in.id)

    return deleted_category




"""
async def get_reddit_top_async(subreddit: str, data: dict) -> None:
    async with httpx.AsyncClient() as client:
        response = await client.get(
            f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
            headers={"User-agent": "category bot 0.1"},
        )

    subreddit_categories = response.json()
    subreddit_data = []
    for entry in subreddit_categories["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    data[subreddit] = subreddit_data


def get_reddit_top(subreddit: str, data: dict) -> None:
    response = httpx.get(
        f"https://www.reddit.com/r/{subreddit}/top.json?sort=top&t=day&limit=5",
        headers={"User-agent": "category bot 0.1"},
    )
    subreddit_categories = response.json()
    # print('subreddit_categories=', subreddit_categories)
    subreddit_data = []
    for entry in subreddit_categories["data"]["children"]:
        score = entry["data"]["score"]
        title = entry["data"]["title"]
        link = entry["data"]["url"]
        subreddit_data.append(f"{str(score)}: {title} ({link})")
    data[subreddit] = subreddit_data


@router.get("/ideas/async")
async def fetch_ideas_async() -> dict:
    data: dict = {}

    await asyncio.gather(
        get_reddit_top_async("auto", data),
        get_reddit_top_async("easyauto", data),
        get_reddit_top_async("TopSecretAuto", data),
    )

    return data


@router.get("/ideas/")
def fetch_ideas() -> dict:
    data: dict = {}
    get_reddit_top("auto", data)
    get_reddit_top("easyauto", data)
    get_reddit_top("TopSecretAuto", data)

    return data
"""
