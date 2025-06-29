from fastapi import FastAPI
from routes.note import note
from fastapi.staticfiles import StaticFiles
from routes.vector_db import note

app = FastAPI()

# Include the note router
app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(note, tags=["notes"])