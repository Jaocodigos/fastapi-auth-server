import importlib
import pkgutil
from fastapi import FastAPI, APIRouter


def register_controllers(app: FastAPI, package: str):
    """
    Discover and register all controllers in package.
    """
    module = importlib.import_module(package)

    for _, module_name, _ in pkgutil.iter_modules(module.__path__):
        full_module_name = f"{package}.{module_name}"
        imported_module = importlib.import_module(full_module_name)

        router = getattr(imported_module, "router", None)

        if isinstance(router, APIRouter):
            app.include_router(router)