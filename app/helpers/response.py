from fastapi.encoders import jsonable_encoder
from starlette.responses import JSONResponse


def make_error_response(app_status=500, detail=None):
    if detail is None:
        detail = {}

    return JSONResponse(
        status_code=app_status.status_code,
        content=jsonable_encoder({"detail": detail}),
    )


def make_response_object(data, meta={}):
    return {"data": data, "meta": meta}
