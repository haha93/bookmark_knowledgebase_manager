from fastapi import FastAPI, HTTPException, Query
from database import db
from models import BookmarkCreate, BookmarkUpdate, NoteCreate, NoteUpdate
from bson import ObjectId
from datetime import datetime
from fastapi_mcp import FastApiMCP

app = FastAPI(title="Bookmark & Knowledge Base Manager")


def serialize_doc(doc):
    doc["id"] = str(doc.pop("_id"))
    return doc


# --- Bookmarks ---

@app.post("/bookmarks")
async def create_bookmark(bookmark: BookmarkCreate):
    doc = bookmark.dict()
    doc["created_at"] = datetime.utcnow()
    result = await db.bookmarks.insert_one(doc)
    return {"message": "Bookmark saved", "id": str(result.inserted_id)}


@app.get("/bookmarks")
async def list_bookmarks(tag: str = Query(None)):
    query = {"tags": tag} if tag else {}
    cursor = db.bookmarks.find(query).sort("created_at", -1)
    bookmarks = [serialize_doc(doc) async for doc in cursor]
    return bookmarks


@app.get("/bookmarks/search")
async def search_bookmarks(q: str = Query(...)):
    query = {"$or": [
        {"title": {"$regex": q, "$options": "i"}},
        {"description": {"$regex": q, "$options": "i"}},
        {"url": {"$regex": q, "$options": "i"}},
    ]}
    cursor = db.bookmarks.find(query)
    return [serialize_doc(doc) async for doc in cursor]


@app.get("/bookmarks/{id}")
async def get_bookmark(id: str):
    doc = await db.bookmarks.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return serialize_doc(doc)


@app.put("/bookmarks/{id}")
async def update_bookmark(id: str, bookmark: BookmarkUpdate):
    update_data = {k: v for k, v in bookmark.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = await db.bookmarks.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return {"message": "Bookmark updated"}


@app.delete("/bookmarks/{id}")
async def delete_bookmark(id: str):
    result = await db.bookmarks.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return {"message": "Bookmark deleted"}


# --- Notes ---

@app.post("/notes")
async def create_note(note: NoteCreate):
    doc = note.dict()
    doc["created_at"] = datetime.utcnow()
    result = await db.notes.insert_one(doc)
    return {"message": "Note saved", "id": str(result.inserted_id)}


@app.get("/notes")
async def list_notes(tag: str = Query(None)):
    query = {"tags": tag} if tag else {}
    cursor = db.notes.find(query).sort("created_at", -1)
    return [serialize_doc(doc) async for doc in cursor]


@app.get("/notes/search")
async def search_notes(q: str = Query(...)):
    query = {"$or": [
        {"title": {"$regex": q, "$options": "i"}},
        {"content": {"$regex": q, "$options": "i"}},
    ]}
    cursor = db.notes.find(query)
    return [serialize_doc(doc) async for doc in cursor]


@app.get("/notes/{id}")
async def get_note(id: str):
    doc = await db.notes.find_one({"_id": ObjectId(id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Note not found")
    return serialize_doc(doc)


@app.put("/notes/{id}")
async def update_note(id: str, note: NoteUpdate):
    update_data = {k: v for k, v in note.dict().items() if v is not None}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")
    result = await db.notes.update_one({"_id": ObjectId(id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note updated"}


@app.delete("/notes/{id}")
async def delete_note(id: str):
    result = await db.notes.delete_one({"_id": ObjectId(id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Note not found")
    return {"message": "Note deleted"}


mcp = FastApiMCP(app)
mcp.mount()
