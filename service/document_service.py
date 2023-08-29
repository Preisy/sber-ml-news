from html.parser import HTMLParser

from fastapi import HTTPException
from starlette.requests import Request
from starlette.responses import HTMLResponse

from model.document import Document
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates

from dto.request import document_request
from dto.response.simple_message_response import SimpleMessageResponse
from utils.env_variables_reader import EnvVariablesReader
import uuid
from bs4 import BeautifulSoup

templates = Jinja2Templates(directory="templates")


class DocumentService:
    async def create_document(self, db: Session, request: Request, data: document_request.DocumentRequest):
        template = templates.TemplateResponse("document.html", {"request": request, "content": data.content})
        soup = BeautifulSoup(template.body)
        document = Document(content=str(soup))
        domain = EnvVariablesReader.get_domain('config/.env')
        db.add(document)
        db.commit()
        db.refresh(document)
        return SimpleMessageResponse(f"https://{domain}/{document.guid}")

    async def get_document(self, db: Session, guid: str):
        document = db.query(Document).filter(Document.guid == uuid.UUID(guid)).first()
        if document is None:
            raise HTTPException(status_code=404, detail="document not found")
        res = HTMLResponse(document.content).body
        formatted_res = res.decode('utf-8')
        return HTMLResponse(content=formatted_res)

    async def delete(self, db: Session, guid: str):
        document = db.query(Document).filter(Document.guid == uuid.UUID(guid)).first()
        if document is not None:
            db.query(Document).filter(Document.guid == uuid.UUID(guid)).delete()
            db.commit()
            return SimpleMessageResponse("Successfully deleted")
        else:
            raise HTTPException(status_code=404, detail="document not found")

    async def delete_all(self, db: Session):
        document = db.query(Document).first()
        if document is not None:
            db.query(Document).delete()
            db.commit()
            return SimpleMessageResponse("Successfully deleted")
        else:
            raise HTTPException(status_code=404, detail="documents not found")
