from sqlalchemy.orm import Session

from . import models, schemas


# ---------------------------------- CREATE ---------------------------------- #
def create_item(db: Session, item: schemas.ItemBase) -> models.Item:
    """
    Create an item in the database
    """
    db_item = models.Item(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item


# ----------------------------------- READ ----------------------------------- #
def get_inventory(db: Session, deleted: bool | None = False) -> list[schemas.Item]:
    """
    If <deleted> is None, return all items.
    If <deleted> is True, return all deleted items.
    If <deleted> is False, return all non-deleted items. **Note:** This is the default.
    """
    if deleted == False:
        return db.query(models.Item).filter(models.Item.deleted == False).all()
    elif deleted == True:
        return db.query(models.Item).filter(models.Item.deleted == True).all()

    return db.query(models.Item).all()


def get_items_in_stock(db: Session, in_stock: bool = True) -> list[schemas.Item]:
    """
    Return a list of all items in stock (and not deleted)
    """
    if in_stock:
        return (
            db.query(models.Item)
            .filter(models.Item.quantity > 0)
            .filter(models.Item.deleted == False)
            .all()
        )
    return (
        db.query(models.Item)
        .filter(models.Item.quantity == 0)
        .filter(models.Item.deleted == False)
        .all()
    )


def get_item_by_id(db: Session, item_id: int) -> models.Item | None:
    """
    Return an item by id, or None if it doesn't exist
    """
    return db.query(models.Item).filter(models.Item.id == item_id).first()


def get_item_by_name(db: Session, name: str) -> models.Item | None:
    """
    Return an item by name, or None if it doesn't exist
    """
    return db.query(models.Item).filter(models.Item.name == name).first()


# ---------------------------------- UPDATE ---------------------------------- #
def update_item(
    db: Session, item_id: int, item: schemas.ItemBase
) -> models.Item | None:
    """
    Update an item by id. Return None if the item doesn't exist
    """
    db_item = get_item_by_id(db, item_id)
    if db_item is None:
        return None
    db_item.name = item.name
    db_item.quantity = item.quantity
    db.commit()
    db.refresh(db_item)

    return db_item


def restore_deleted_item(db: Session, item_id: int) -> models.Item | None:
    """
    Restore a deleted item by id. Return None if the item doesn't exist
    """
    db_item = get_item_by_id(db, item_id)
    if db_item is None:
        return None
    db_item.deleted = False
    db_item.deletion_comments = ""
    db.commit()
    db.refresh(db_item)

    return db_item


def update_item_quantity(
    db: Session, item_id: int, quantity: int
) -> models.Item | None:
    """
    Update an item's quantity by id. Return None if the item doesn't exist
    """
    db_item = get_item_by_id(db, item_id)
    if db_item is None:
        return None
    db_item.quantity = quantity
    db.commit()
    db.refresh(db_item)

    return db_item


# ---------------------------------- DELETE ---------------------------------- #
def delete_item(db: Session, item_id: int, comments: str) -> models.Item | None:
    """
    Delete an item by id. Return None if the item doesn't exist
    """
    db_item = get_item_by_id(db, item_id)
    if db_item is None:
        return None
    # Check if the item has already been marked as deleted in the db
    if db_item.deleted:
        db.delete(db_item)
        db.commit()
    else:
        db_item.deleted = True
        db_item.deletion_comments = comments
        db.commit()
        db.refresh(db_item)

    return db_item
