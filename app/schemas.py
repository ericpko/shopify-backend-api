from pydantic import BaseModel, Field


class ItemBase(BaseModel):
    name: str = Field(..., title="Item Name", max_length=100)
    quantity: int = Field(ge=0, title="Item Quantity")


# Inherit from ItemBase above
class Item(ItemBase):
    id: int = Field(..., title="Item ID")
    deleted: bool = Field(False, title="Item Deleted")
    deletion_comments: str = Field("", title="Deleted Item Comments", max_length=300)

    class Config:
        orm_mode = True
