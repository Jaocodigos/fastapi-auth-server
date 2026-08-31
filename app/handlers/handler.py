import inspect

from fastapi.responses import JSONResponse

import app.handlers.errors.default as default_errors


def default_error_handler(request, exc) -> JSONResponse:
    return JSONResponse(
        status_code=exc.status_code,
        content={"message": exc.message}
    )

def get_default_error_classes():
    errors = []

    for _, obj in inspect.getmembers(default_errors, inspect.isclass):
        if issubclass(obj, Exception):
            errors.append(obj)

    return errors

def register_error_handlers(app):

    for error_cls in get_default_error_classes():
        app.add_exception_handler(error_cls, default_error_handler)
