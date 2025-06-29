from fastapi import APIRouter, FastAPI, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates

from bson import ObjectId
from . import pineconetest


chatbot = APIRouter()
templates = Jinja2Templates(directory="templates")



@chatbot.get("/")
def read_item():
    return {"world": "hello world"}


@chatbot.get("/pinecone")
def read_item1(query):
    return pineconetest.vector_db_query(query)

@chatbot.get("/together")
def read_item2(query: str):
    results = pineconetest.vector_db_query(query)
    answer = pineconetest.query_together_ai(results, query)
    return {"response": answer}
