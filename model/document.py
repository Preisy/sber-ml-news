from sqlalchemy import Boolean, String, Column
from database import Base
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE

class Document(Base):
    __tablename__ = 'documents'

    id = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE, index=True)
    text = Column(String, index=True)
