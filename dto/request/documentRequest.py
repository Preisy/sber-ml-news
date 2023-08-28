from pydantic import BaseModel
from pydantic import BaseConfig

BaseConfig.arbitrary_types_allowed = True


class DocumentDTO(BaseModel):
    content: str
