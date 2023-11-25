from app.api.models import NoteSchema
from app.db import notes, database


async def post(payload: NoteSchema):
    query = notes.insert().values(**payload.model_dump())
    return await database.execute(query=query)
