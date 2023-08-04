from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import models
from routers import auth, user, post
from database import engine

models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="EXAMPLE-API",
    version="0.1.0",
    description="FASTAPI to use as an example for deployments.",
    contact={
        "name": "James Twose",
        "email": "contact@jamestwose.com",
    },
)


app.include_router(auth.router)
app.include_router(post.router)
app.include_router(user.router)

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


@app.get("/", tags=["Root"])
def read_root():
    """Root endpoint.
    
    Parameters
    ----------
    None
    
    Returns
    -------
    dict
        A dictionary containing a welcome message.
    
    """
    return {"Hello": "Welcome to the EXAMPLE API"}
