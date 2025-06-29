from fastapi import APIRouter, FastAPI, Request, Form
from models.note import Note
from fastapi.responses import HTMLResponse, RedirectResponse
from config.db import conn
from fastapi.templating import Jinja2Templates
from schemas.note import noteEntity, notesEntity
from bson import ObjectId
from . import pineconetest


note = APIRouter()
templates = Jinja2Templates(directory="templates")



@note.get("/")
def read_item():
    return {"world": "hello world"}


@note.get("/pinecone")
def read_item1(query):
    return pineconetest.vector_db_query(query)

@note.get("/together")
def read_item2(query: str):
    results = pineconetest.vector_db_query(query)
    answer = pineconetest.query_together_ai(results, query)
    return {"response": answer}
