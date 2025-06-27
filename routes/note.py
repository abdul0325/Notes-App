from fastapi import APIRouter
from models.note import Note
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from config.db import conn
from fastapi.templating import Jinja2Templates
from schemas.note import noteEntity, notesEntity
from fastapi.responses import RedirectResponse
from bson import ObjectId
from fastapi import Form


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



# DELETE
@note.get("/delete/{id}")
async def delete_note(id: str):
    conn.notes.notes.delete_one({"_id": ObjectId(id)})
    return RedirectResponse(url="/", status_code=303)

# UPDATE FORM (GET)
@note.get("/update/{id}", response_class=HTMLResponse)
async def update_form(request: Request, id: str):
    doc = conn.notes.notes.find_one({"_id": ObjectId(id)})
    return templates.TemplateResponse("update.html", {
        "request": request,
        "doc": doc
    })

# UPDATE ACTION (POST)
@note.post("/update/{id}")
async def update_note(id: str, title: str = Form(...), desc: str = Form(...), important: str = Form(None)):
    conn.notes.notes.update_one(
        {"_id": ObjectId(id)},
        {"$set": {
            "title": title,
            "desc": desc,
            "important": important == "on"
        }}
    )
    return RedirectResponse(url="/", status_code=303)