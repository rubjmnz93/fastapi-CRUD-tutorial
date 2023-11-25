from fastapi import APIRouter, status

from app.api import crud
from app.api.models import NoteSchema, NoteDB

router = APIRouter()


@router.post("/",
             response_model=NoteDB,
             status_code=status.HTTP_201_CREATED)
async def crete_note(payload: NoteSchema):
    note_id = await crud.post(payload)

    response_object = NoteDB(id=note_id, **payload.model_dump())

    return response_object
