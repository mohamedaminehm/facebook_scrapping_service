from fastapi import Depends, FastAPI, HTTPException, Request, Form
import uvicorn
from bson.objectid import ObjectId


from endpoints.scrapper import router
from settings import app

app = FastAPI()


app.include_router(router, tags=["posts"])




if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=5000, log_level="info", reload=True)