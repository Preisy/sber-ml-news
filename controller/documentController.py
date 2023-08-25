from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from database import get_db

from service import documentService as DocumentService
from dto import documentDTO as DocumentDTO

router = APIRouter()


@router.post('/', tags=["document"])
async def create(data: DocumentDTO.DocumentDTO = None, db: Session = Depends(get_db)):
    return await DocumentService.create_document(data, db)


@router.delete('/', tags=["document"])
async def delete_all(db: Session = Depends(get_db)):
    return await DocumentService.delete_all(db)


@router.get('/{guid}', tags=["document"], response_class=HTMLResponse)
async def get(request: Request, guid: str, db: Session = Depends(get_db)):
    return await DocumentService.get_document(request, guid, db)


@router.delete('/{guid}', tags=["document"])
async def delete(guid: str, db: Session = Depends(get_db)):
    return await DocumentService.delete(db, guid)
