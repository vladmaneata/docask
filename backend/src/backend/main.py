import uuid

from fastapi import FastAPI, UploadFile

app = FastAPI()
documents: dict[str, dict] = {}


@app.get("/health")
def health():
    return {"status": "ok"}


@app.post("/documents")
async def upload_document(file: UploadFile):
    content = await file.read()
    text = content.decode("utf-8")
    doc_id = str(uuid.uuid4())
    documents[doc_id] = {"filename": file.filename, "content": text}
    return {"id": doc_id, "filename": file.filename, "characters": len(text)}