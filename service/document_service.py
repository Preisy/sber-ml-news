import re
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
from dto.exceptions.not_found_exception import NotFoundException
from dto.exceptions.bad_request_exception import BadRequestException
from dto.response.simple_url_response import SimpleUrlResponse

templates = Jinja2Templates(directory="templates")


class DocumentService:
    guid_pattern = "^(?:\\{{0,1}(?:[0-9a-fA-F]){8}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){4}-(?:[0-9a-fA-F]){4}-(?:[" \
                   "0-9a-fA-F]){12}\\}{0,1})$"

    async def create_document(self, db: Session, request: Request, data: document_request.DocumentRequest):
        template = templates.TemplateResponse("document.html", {"request": request, "content": data.content})
        soup = BeautifulSoup(template.body)
        document = Document(content=str(soup))
        app_base_url = EnvVariablesReader.get_app_base_url('config/.env')
        db.add(document)
        db.commit()
        db.refresh(document)
        return SimpleUrlResponse(f"{app_base_url}/documents/{document.guid}")

    async def get_document(self, db: Session, guid: str):
        if re.match(self.guid_pattern, guid) is None:
            raise BadRequestException()
        document = db.query(Document).filter(Document.guid == uuid.UUID(guid)).first()
        if document is not None:
            res = HTMLResponse(document.content).body
            formatted_res = res.decode('utf-8')
            return HTMLResponse(content=formatted_res)
        else:
            raise NotFoundException("document")

    async def delete(self, db: Session, guid: str):
        if re.match(self.guid_pattern, guid) is None:
            raise BadRequestException()
        document = db.query(Document).filter(Document.guid == uuid.UUID(guid)).first()
        if document is not None:
            db.query(Document).filter(Document.guid == uuid.UUID(guid)).delete()
            db.commit()
            return SimpleMessageResponse("Successfully deleted")
        else:
            raise NotFoundException("document")

    async def delete_all(self, db: Session):
        document = db.query(Document).first()
        if document is not None:
            db.query(Document).delete()
            db.commit()
            return SimpleMessageResponse("Successfully deleted")
        else:
            raise NotFoundException("documents")
