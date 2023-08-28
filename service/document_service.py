from starlette.requests import Request
import os
from dotenv import load_dotenv
from fastapi import HTTPException
from model.document import Document
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from dto.request import document_request
from dto.response.simple_message_response import SimpleMessageResponse

import uuid

templates = Jinja2Templates(directory="templates")

load_dotenv('config/.env')
domen = os.getenv('DOMEN')


class DocumentService:
    async def create_document(db: Session, data: document_request.DocumentRequest):
        document = Document(text=data.content)
        db.add(document)
        db.commit()
        db.refresh(document)
        return SimpleMessageResponse(f"https://{domen}/{document.guid}")

    async def get_document(db: Session, request: Request, guid: str):
        document = db.query(Document).filter(Document.guid == uuid.UUID(guid)).first()
        return templates.TemplateResponse("document.html", {"request": request, "content": document.content})

    async def delete(db: Session, guid: str):
        document = db.query(Document).filter(Document.guid == uuid.UUID(guid)).delete()
        db.commit()
        return SimpleMessageResponse("Successfully deleted")

    async def delete_all(db: Session):
        db.query(Document).delete()
        db.commit()
        return SimpleMessageResponse("Successfully deleted")
