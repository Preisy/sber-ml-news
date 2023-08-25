import uvicorn
from fastapi import FastAPI
from database import engine, Base
from controller import documentController as DocumentController

Base.metadata.create_all(bind=engine)
app = FastAPI()
app.include_router(DocumentController.router, prefix="/documents")

if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080, reload=True, workers=3)
