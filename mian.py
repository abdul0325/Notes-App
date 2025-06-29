from fastapi import FastAPI, Request, Form
from fastapi.responses import StreamingResponse, HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware

from routes.pineconetest import vector_db_query, query_together_ai

app = FastAPI()

# Serve static files (if any)
app.mount("/static", StaticFiles(directory="static"), name="static")

# Set up templates folder
templates = Jinja2Templates(directory="templates")

# CORS (only needed if frontend is separate; safe to keep)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"]
)

# Homepage route
@app.get("/", response_class=HTMLResponse)
async def get_home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

# Chat endpoint with streaming response
@app.post("/chat")
async def chat(request: Request):
    data = await request.json()
    user_query = data.get("query", "")
    results = vector_db_query(user_query)

    def generate():
        answer = query_together_ai(results, user_query)
        for char in answer:
            yield char
            import time
            time.sleep(0.01)

    return StreamingResponse(generate(), media_type="text/plain")
