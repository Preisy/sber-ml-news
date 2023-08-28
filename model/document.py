from sqlalchemy import Boolean, String, Column
from database import Base
from fastapi_utils.guid_type import GUID, GUID_DEFAULT_SQLITE
from bs4 import BeautifulSoup

class Document(Base):
    __tablename__ = 'documents'

    guid = Column(GUID, primary_key=True, default=GUID_DEFAULT_SQLITE, index=True)
    content = Column(String, index=True)
