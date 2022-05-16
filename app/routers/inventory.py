# ------------------------------------------------------------
# RESTful API
#
# ------------------------------------------------------------
from fastapi import APIRouter, Body, status, Depends, HTTPException
from sqlalchemy.orm import Session

from .. import schemas
from .. import models
from .. import crud
from ..dependencies import get_db


router = APIRouter(
    prefix="/inventory",
    tags=["inventory"],
    responses={404: {"description": "Not found"}},
)


# ------------------------------------ GET ----------------------------------- #
# localhost:3000/inventory/
@router.get("/", response_model=list[schemas.Item])
async def get_inventory(db: Session = Depends(get_db)) -> list[schemas.Item]:
    """
    Returns a list of all the non-deleted items in the inventory
    """
    return crud.get_inventory(db, deleted=False)


@router.get("/deleted", response_model=list[schemas.Item])
async def get_deleted_inventory(db: Session = Depends(get_db)) -> list[schemas.Item]:
    """
    Returns a list of all the deleted items in the inventory
    """
    return crud.get_inventory(db, deleted=True)


@router.get("/all", response_model=list[schemas.Item])
async def get_all_inventory(db: Session = Depends(get_db)) -> list[schemas.Item]:
    """
    Returns a list of all the items in the inventory
    """
    return crud.get_inventory(db, deleted=None)


@router.get("/in-stock", response_model=list[schemas.Item])
async def get_items_in_stock(db: Session = Depends(get_db)) -> list[schemas.Item]:
    """
    Returns a list of all the in-stock items in the inventory
    """
    return crud.get_items_in_stock(db, in_stock=True)


@router.get("/out-of-stock", response_model=list[schemas.Item])
async def get_items_out_of_stock(db: Session = Depends(get_db)) -> list[schemas.Item]:
    """
    Returns a list of all the out-of-stock items in the inventory
    """
    return crud.get_items_in_stock(db, in_stock=False)


@router.get("/{item_id}", response_model=schemas.Item)
async def get_item_by_id(item_id: int, db: Session = Depends(get_db)) -> schemas.Item:
    """
    Returns an item by id, or raises a 404 if it doesn't exist
    """
    db_item = crud.get_item_by_id(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# ----------------------------------- POST ----------------------------------- #
@router.post("/", response_model=schemas.Item, status_code=status.HTTP_201_CREATED)
async def create_item(
    item: schemas.ItemBase, db: Session = Depends(get_db)
) -> schemas.Item:
    """
    Takes a JSON object and creates a new item in the database.
    """
    return crud.create_item(db, item)


# ------------------------------------ PUT ----------------------------------- #
@router.put("/{item_id}", response_model=schemas.Item)
async def update_item(
    item_id: int, item: schemas.ItemBase, db: Session = Depends(get_db)
) -> schemas.Item:
    """
    Takes a JSON object and updates an item in the database.
    Raises a 404 if the item doesn't exist.
    """
    db_item = crud.update_item(db, item_id, item)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


@router.put("/restore/{item_id}", response_model=schemas.Item)
async def restore_deleted_item(
    item_id: int, db: Session = Depends(get_db)
) -> schemas.Item:
    """
    If an Item has been delelted (i.e. item.deleted = True), this will
    set item.deleted = False and item.deletion_comments = "",
    then will return the updated item.
    """
    db_item = crud.restore_deleted_item(db, item_id)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# ----------------------------------- PATCH ---------------------------------- #
@router.patch("/{item_id}", response_model=schemas.Item)
async def update_item_quantity(
    item_id: int, quantity: int = 0, db: Session = Depends(get_db)
) -> schemas.Item:
    """
    Takes an item id and a quantity and updates the quantity of the item.
    """
    db_item = crud.update_item_quantity(db, item_id, quantity)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item


# ---------------------------------- DELETE ---------------------------------- #
@router.delete("/{item_id}", response_model=schemas.Item)
async def delete_item(
    item_id: int, comments: str | None = "", db: Session = Depends(get_db)
) -> schemas.Item:
    """
    Takes an item ID and deletes the item from the database.
    """
    db_item = crud.delete_item(db, item_id, comments)
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item
