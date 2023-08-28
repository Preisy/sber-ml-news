import uvicorn
from fastapi import FastAPI
from database import engine, Base
from controller import document_сontroller
from utils.global_exception_handler import GlobalExceptionHandler




Base.metadata.create_all(bind=engine)
exception_handlers = {500: GlobalExceptionHandler.internal_exception_handler}
app = FastAPI(exception_handlers=exception_handlers)
app.include_router(document_сontroller.router, prefix="/documents")





if __name__ == '__main__':
    uvicorn.run("main:app", host='127.0.0.1', port=8080, reload=True, workers=3)
