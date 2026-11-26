import uuid

from fastapi import FastAPI, UploadFile, HTTPException

app = FastAPI()
documents: dict[str, dict] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents")
async def upload_document(file: UploadFile):
    content = await file.read()
    try:
        text = content.decode("utf-8")
    except UnicodeDecodeError:
        raise HTTPException(status_code=400, detail="File must be UTF-8 text")
    doc_id = str(uuid.uuid4())
    documents[doc_id] = {"filename": file.filename, "content": text}
    return {"id": doc_id, "filename": file.filename, "characters": len(text)}


@app.get("/documents/{doc_id}")
def get_document(doc_id: str):
    document = documents.get(doc_id)
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return {
        "id": doc_id,
        "filename": document["filename"],
        "content": document["content"],
        "characters": len(document["content"]),
    }


@app.get("/documents")
def list_documents():
    return [
        {"id": doc_id, "filename": doc["filename"], "characters": len(doc["content"])}
        for doc_id, doc in documents.items()
    ]
