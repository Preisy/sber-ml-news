from starlette.requests import Request
import os
from dotenv import load_dotenv

from model.document import Document
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from dto import documentDTO

import uuid

templates = Jinja2Templates(directory="templates")

load_dotenv('config/.env')
domen = os.getenv('DOMEN')


async def create_document(data: documentDTO.DocumentDTO, db: Session):
    document = Document(text=data.text)
    try:
        db.add(document)
        db.commit()
        db.refresh(document)
    except Exception as e:
        print(e)

    return f"https://{domen}/{document.id}"


async def get_document(request: Request, guid: str, db):
    document = db.query(Document).filter(Document.id == uuid.UUID(guid)).first()
    return templates.TemplateResponse("document.html", {"request": request, "text": document.text})


async def delete(db: Session, guid: str):
    document = db.query(Document).filter(Document.id == uuid.UUID(guid)).delete()
    db.commit()
    return "Successfully deleted"


async def delete_all(db: Session):
    db.query(Document).delete()
    db.commit()
    return "Successfully deleted"
