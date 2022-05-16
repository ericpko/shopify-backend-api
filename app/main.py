# ------------------------------------------------------------
# Shopify Developer Intern Challenge - Fall 2022
#
# RESTful API:
# - GET /inventory/
# - GET /inventory/deleted
# - GET /inventory/all
# - GET /inventory/in-stock
# - GET /inventory/out-of-stock
# - GET /inventory/:id
# - POST /inventory/
# - PUT /inventory/:id
# - PUT /inventory/restore/:id
# - PATCH /inventory/:id
# - DELETE /inventory/:id
#
# Author: Eric Koehli
# ------------------------------------------------------------
from fastapi import FastAPI

from .routers import inventory
from .database import engine
from . import models

# Create the database tables
models.Base.metadata.create_all(bind=engine)

# Initialize the FastAPI application
app = FastAPI()

# Include all the routers. (Only one in this case)
app.include_router(inventory.router)


# Home/Root
@app.get("/")
async def root() -> dict[str, str]:
    return {"Greetings": "Shopify!"}
