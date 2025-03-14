# filepath: /mi-fastapi-app/mi-fastapi-app/app/routers/__init__.py
from fastapi import APIRouter

router = APIRouter()

# Aquí puedes definir tus rutas
# Ejemplo:
# @router.get("/items/")
# async def read_items():
#     return [{"item_id": "foo"}, {"item_id": "bar"}]

# Exporta el router para usarlo en main.py
# from . import router