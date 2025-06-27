def noteEntity(item) -> dict:
    return {
        "id": str(item["_id"]),
        "title": item["title", ""],
        "desc": item["title", ""],
        "important": item["title", False]
    }
    
def notesEntity(items) -> list:
    return [noteEntity(item) for item in items]
