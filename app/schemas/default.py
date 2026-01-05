from pydantic import BaseModel

class DefaultResponse(BaseModel):
    message: str
    status: str


DeletedResponse = DefaultResponse(
    message="Resource has been deleted",
    status="success"
)

UpdatedResponse = DefaultResponse(
    message="Resource has been updated",
    status="success"
)



