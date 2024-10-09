# External packages
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from mangum import Mangum  # AWS Lambda handler
from pydantic import BaseModel
from starlette.requests import Request
import uvicorn

# Modules
import config
from query_data import query_rag, build_response_string
from update_database import copy_to_tmp

# Initialize FastAPI handler and Mangum handler
app = FastAPI()
handler = Mangum(app)

# Mount HTML/CSS
app.mount("/static", StaticFiles(directory=config.PATH_STATIC), name="static")
templates = Jinja2Templates(directory=config.PATH_TEMPLATES)


class Query(BaseModel):
    query_text: str

# GET


@app.get("/")
async def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# POST

@app.post("/copy_DB_to_tmp")
def copy_DB_to_tmp():
    """
    Copy DB to AWS /tmp storage
    """
    copy_status = copy_to_tmp()
    return {"copy_status": {copy_status}}


@app.post("/repeat_query")
def repeat_query(request: Query):
    """
    Debugging function
    """
    query_response = request.query_text
    return {"query_response": {query_response}}


@app.post("/submit_query")
def submit_query(request: Query):
    message = query_rag(request.query_text)
    return {"query_response": message}


# Run main to test locally on localhost:8000
if __name__ == "__main__":
    print(f"Running the FastAPI server on port {config.port}.")
    uvicorn.run("api_handler:app", host="0.0.0.0", port=config.port)
