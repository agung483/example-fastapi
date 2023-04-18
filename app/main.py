from . import models
from .database import engine
from .routers import post, user, auth, menu, kelMenu, vote, transaksi
from fastapi import FastAPI, APIRouter
from fastapi.middleware.cors import CORSMiddleware
#from .config import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI()
#router = APIRouter(
#    prefix="/users",
#    tags=['Users']
#)

origins = ["*"] # ["https://www.google.com","https://www.youtube.com"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(menu.router)
app.include_router(kelMenu.router)
app.include_router(vote.router)
app.include_router(transaksi.router)

@app.get("/")
def read_items():
    return {"message": "Welcome to my Api"}



