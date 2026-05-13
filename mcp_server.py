import httpx
from mcp.server.fastmcp import FastMCP

API_BASE = "https://bookmark-api-808779870972.us-central1.run.app"

mcp = FastMCP("Bookmark & Knowledge Base Manager")


# --- Bookmark Tools ---

@mcp.tool()
async def save_bookmark(url: str, title: str, description: str = "", tags: list[str] = []) -> dict:
    """Save a new bookmark with URL, title, description, and tags."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/bookmarks", json={
            "url": url, "title": title, "description": description, "tags": tags
        })
        return resp.json()


@mcp.tool()
async def list_bookmarks(tag: str = "") -> list:
    """List all bookmarks, optionally filtered by tag."""
    params = {"tag": tag} if tag else {}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/bookmarks", params=params)
        return resp.json()


@mcp.tool()
async def search_bookmarks(query: str) -> list:
    """Search bookmarks by keyword in title, description, or URL."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/bookmarks/search", params={"q": query})
        return resp.json()


@mcp.tool()
async def get_bookmark(id: str) -> dict:
    """Get a single bookmark by its ID."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/bookmarks/{id}")
        return resp.json()


@mcp.tool()
async def update_bookmark(id: str, url: str = "", title: str = "", description: str = "", tags: list[str] = []) -> dict:
    """Update a bookmark. Only non-empty fields will be updated."""
    payload = {}
    if url: payload["url"] = url
    if title: payload["title"] = title
    if description: payload["description"] = description
    if tags: payload["tags"] = tags
    async with httpx.AsyncClient() as client:
        resp = await client.put(f"{API_BASE}/bookmarks/{id}", json=payload)
        return resp.json()


@mcp.tool()
async def delete_bookmark(id: str) -> dict:
    """Delete a bookmark by its ID."""
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{API_BASE}/bookmarks/{id}")
        return resp.json()


# --- Note Tools ---

@mcp.tool()
async def save_note(title: str, content: str, tags: list[str] = []) -> dict:
    """Save a new knowledge note with title, content, and tags."""
    async with httpx.AsyncClient() as client:
        resp = await client.post(f"{API_BASE}/notes", json={
            "title": title, "content": content, "tags": tags
        })
        return resp.json()


@mcp.tool()
async def list_notes(tag: str = "") -> list:
    """List all notes, optionally filtered by tag."""
    params = {"tag": tag} if tag else {}
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/notes", params=params)
        return resp.json()


@mcp.tool()
async def search_notes(query: str) -> list:
    """Search notes by keyword in title or content."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/notes/search", params={"q": query})
        return resp.json()


@mcp.tool()
async def get_note(id: str) -> dict:
    """Get a single note by its ID."""
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{API_BASE}/notes/{id}")
        return resp.json()


@mcp.tool()
async def update_note(id: str, title: str = "", content: str = "", tags: list[str] = []) -> dict:
    """Update a note. Only non-empty fields will be updated."""
    payload = {}
    if title: payload["title"] = title
    if content: payload["content"] = content
    if tags: payload["tags"] = tags
    async with httpx.AsyncClient() as client:
        resp = await client.put(f"{API_BASE}/notes/{id}", json=payload)
        return resp.json()


@mcp.tool()
async def delete_note(id: str) -> dict:
    """Delete a note by its ID."""
    async with httpx.AsyncClient() as client:
        resp = await client.delete(f"{API_BASE}/notes/{id}")
        return resp.json()


if __name__ == "__main__":
    mcp.run()
