from typing import List
from fastapi import APIRouter, status, HTTPException

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


@router.get("/", response_model=List[NoteDB])
async def read_all_notes():
    return await crud.get_all()


@router.get("/{id}/", response_model=NoteDB)
async def read_note(id: int):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")
    return note


@router.put("/{id}/", response_model=NoteDB)
async def update_note(id: int, payload: NoteSchema):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    note_id = await crud.put(id, payload)

    response_object = NoteDB(id=note_id, **payload.model_dump())

    return response_object


@router.delete("/{id}/")
async def remove_note(id: int):
    note = await crud.get(id)
    if not note:
        raise HTTPException(status_code=404, detail="Note not found")

    await crud.delete(id)

    return note
