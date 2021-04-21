from fastapi import FastAPI
from main import course_router
from security import security_router
import uvicorn
from sqlalchemy.orm import Session
import crud, models, schemas
import uvicorn, time
from database import SessionLocal, engine
from fastapi import Request, Depends
#import logging
#from qr_logger import create_or_get_logger, log_warning
from fastapi.middleware.cors import CORSMiddleware#, SessionMiddleware
#from starlette.middleware.gzip import GZipMiddleware


# filename = "pilot.log"
# logging = create_or_get_logger(filename)
# logging.getLogger(__name__)
# logging.debug('This will get logged to a file')


app = FastAPI(title='workpeer',
        description='workpeer API',
        version='1.0.0', redoc_url = None,)


def init_routers(app: FastAPI) -> None:
    #app.include_router(home_router)
    app.include_router(course_router, prefix='', tags=['courses'])
    app.include_router(security_router, prefix='', tags=['Security'])


def create_app() -> FastAPI:
    # config = get_config()
    # app = FastAPI(
        
    # )
    init_routers(app=app)
    # init_listeners(app=app)
    # check_vertexes(app=app)
    #app.add_middleware(DBSessionMiddleware, db_url=config.DB_URL)

    return app


app = create_app()


 
origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.debug = True


models.Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


if __name__ == "__main__":
    uvicorn.run("pilot:app", host="127.0.0.1", port=9000, reload=True)
    # app.run(debug=True)