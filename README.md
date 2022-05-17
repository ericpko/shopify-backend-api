# Shopify Developer Intern Challenge - Fall 2022

## Tech Stack & Dependencies

- Python 3.8 :snake:
- [FastAPI](https://fastapi.tiangolo.com/)
- SQLite

## Installation & Startup

1. From this project page on replit.com, simply hit `run`.
   - This should start the unicorn server
2. Expand the replit web view into your browser: `https://shopify-backend-api.ericpko.repl.co/`
3. To use the API, add path `docs` to the URL:
   - [https://shopify-backend-api.ericpko.repl.co/docs](https://shopify-backend-api.ericpko.repl.co/docs)

## File Structure

```none
shopify-backend-api
│
│   pyproject.toml
│   README.md
│   sql_app.db
│
└───app
    │   __init__.py
    │   main.py
    │   crud.py
    │   database.py
    │   dependencies.py
    │   models.py
    │   schema.py
    │
    └───routers
        │   __init__.py
        │   inventory.py
```

### main.py

This is the main file that sets up the database, initializes
the FastAPI, and starts the app.

### models.py

This is where I defined the `inventory` database table.
Each row is an `Item`

### schemas.py

There are two classes in this file: `ItemBase` and `Item`.
`ItemBase` is used for the request bodies, and `Item` is used
in the response bodies. `Item` includes 3 extra fields that
clients don't input themselves when creating an Item.

### crud.py & routers/inventory.py

These are the meat of the API. `crud.py` is where I interacted
with the ORM database, and `inventory.py` is where I handled
the client requests (GET, POST, PUT, PATCH, DELETE).

## RESTful API

### GET

- `https://shopify-backend-api.ericpko.repl.co/inventory/`
  - Returns all non-deleted items in the inventory
- `https://shopify-backend-api.ericpko.repl.co/inventory/deleted`
  - Returns all deleted items in the inventory
- `https://shopify-backend-api.ericpko.repl.co/inventory/in-stock`
  - Returns all non-deleted in-stock items
- `https://shopify-backend-api.ericpko.repl.co/inventory/out-of-stock`
  - Returns all non-deleted out-of-stock items
- `https://shopify-backend-api.ericpko.repl.co/inventory/all`
  - Returns all items (including out-of-stock and deleted items)
- `https://shopify-backend-api.ericpko.repl.co/inventory/{item_id}`
  - Returns the item with `{item_id}` or `404` if not found.

### POST

- `https://shopify-backend-api.ericpko.repl.co/inventory/`
  - Creates a new item in the database

### PUT

- `https://shopify-backend-api.ericpko.repl.co/inventory/{item_id}`
  - Updates an item in the database.
- `https://shopify-backend-api.ericpko.repl.co/inventory/restore/{item_id}`
  - Restores a deleted item in the database.

### PATCH

- `https://shopify-backend-api.ericpko.repl.co/inventory/{item_id}`
  - Takes an item id and a quantity and updates the quantity of the item.

### DELETE

- `https://shopify-backend-api.ericpko.repl.co/inventory/{item_id}`
  - Takes an item ID and deletion comments and marks an item as deleted
  - If this item as already been marked as deleted, then calling this again, will permanently remove the item from the database.

## Feature

The feature I implemented was the
"When deleting, allow deletion comments and undeletion". Originally, I
decided to implement this by creating two separate disjoin tables
in the database. One table would be an `inventory` and the other table
would be the `deleted items`. However, rather than try to sync two
separate tables, I decided to only keep one table called `inventory` and
added a `deleted` column and a `deletion_comments` column.

Thus, when an item is `deleted`, it gets marked as `deleted = True`,
so when a client tries to get a list of the inventory, it won't include
the items that are marked as `deleted`. If a client wants to restore
a deleted item, the database gets updated to set
`deleted = False` and `deletion_comments = ""`. Thus, this item is
queryable again from `GET /inventory/`. However, if a client requests to delete
an item that is already marked as deleted, then that item is permanently
removed from the database.
