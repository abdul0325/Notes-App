from pydantic import BaseModel, Field

class Note(BaseModel):
    title: str = Field(..., min_length=1, max_length=100, description="Title of the note")
    desc: str = Field(..., min_length=1, max_length=500, description="Description of the note")
    important: bool = Field(default=False, description="Whether the note is important or not")