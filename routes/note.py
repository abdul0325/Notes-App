from fastapi import APIRouter
from models.note import Note
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from config.db import conn
from fastapi.templating import Jinja2Templates
from schemas.note import noteEntity, notesEntity
from fastapi.responses import RedirectResponse


note = APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs = conn.notes.notes.find({})
    newDocs = []
    for doc in docs:
        newDocs.append({
        "id": doc["_id"],
        "title": doc["title"],
        "desc": doc["desc"],
        "important": doc.get("important", False),  # <-- fixed here
    })

    return templates.TemplateResponse("index.html", {"request": request, "newDocs": newDocs}) 

@note.post("/add")
async def add_note(request: Request):
    form = await request.form()
    formDict = dict(form)
    important = formDict.get("important") == "on"

    note_data = {
        "title": formDict["title"],
        "desc": formDict["desc"],
        "important": important,
    }

    # INSERT TO DATABASE
    conn.notes.notes.insert_one(note_data)

    # Optionally redirect to homepage
    return RedirectResponse(url="/", status_code=303)



# @note.post("/")
# async def create_item(request: Request):
#     form = await request.form()
#     formDict = dict(form)
#     formDict["important"] = True if formDict["important"] == "on" else False
#     note = conn.notes.notes.insert_one(formDict)
#     return {"Success": True }
    # title = form.get("title")
    # desc = form.get("desc")
    # important = form.get("important") == "on"
# def add_note(note : Note):
#     inserted_note = conn.notes.notes.insert_one(dict(note))
#     return noteEntity(inserted_note)
 