from fastapi import Depends
from sqlalchemy.orm import Session
from starlette.requests import Request
from starlette.responses import HTMLResponse

from database import get_db
from service.document_service import DocumentService
from dto.request import document_request
from fastapi_utils.cbv import cbv
from fastapi_utils.inferring_router import InferringRouter

router = InferringRouter(tags=["document"])

@cbv(router)
class DocumentController:
    session: Session = Depends(get_db)
    document_service = DocumentService()

    @router.post('/')
    async def create(self, request: Request, data: document_request.DocumentRequest = None):
        return await self.document_service.create_document(self.session, request, data)

    @router.delete('/')
    async def delete_all(self):
        return await self.document_service.delete_all(self.session)

    @router.get('/{guid}', response_class=HTMLResponse)
    async def get(self, guid: str):
        return await self.document_service.get_document(self.session, guid)

    @router.delete('/{guid}')
    async def delete(self, guid: str):
        return await self.document_service.delete(self.session, guid)
