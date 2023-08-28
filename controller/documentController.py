from fastapi import FastAPI, Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse
from database import get_db

from service import documentService as DocumentService
from dto.request import documentRequest as DocumentRequest

from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter(tags=["document"])


@cbv(router)
class DocumentController:
    session: Session = Depends(get_db)

    @router.post('/')
    async def create(self, data: DocumentRequest.DocumentRequest = None):
        return await DocumentService.create_document(self.session, data)

    @router.delete('/')
    async def delete_all(self):
        return await DocumentService.delete_all(self.session)

    @router.get('/{guid}', response_class=HTMLResponse)
    async def get(self, request: Request, guid: str):
        return await DocumentService.get_document(self.session, request, guid)

    @router.delete('/{guid}')
    async def delete(self, guid: str):
        return await DocumentService.delete(self.session, guid)
