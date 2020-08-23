# OnlineStore
REST API for online store

## Deployment
This application uses `Docker` to running *flask-app* and *database* in two containers.<br>
You can find information about installing Docker here: [Windows](https://docs.docker.com/docker-for-windows/install/),
[Mac](https://docs.docker.com/docker-for-mac/install/), [Linux](https://docs.docker.com/engine/install/ubuntu/).<br>
To build Docker images from `docker-compose.yml` use:
```
docker-compose build
```
and to run containers:
```
docker-compose up -d
```
## Available functions
the api contains 2 simple types:
* **Cart {"id", "items"=[]}**
* **CartItem {"id", "cart_id",   "product", "quantity"**
}
***
the following methods are available:
* `/online-store/api/carts` - creat a Cart *(method **POST**)*
* `/online-store/api/carts/<cart_id>` - get a Cart *(method **GET**)*
* `/online-store/api/carts/<cart_id>/items` - add CartItem to Cart *(method **POST**)*
* `/online-store/api/carts/<cart_id>/items/<item_id>` - delete CartItem from Cart *(method **DELETE**)*
## ORM and CRUD
You may also change the method to access database from ORM peewee to adapter psycopg2.<br>
In file app.py replace the code
```python
import orm_db.db as db
```
with
```python
import crud_db.db as db
```