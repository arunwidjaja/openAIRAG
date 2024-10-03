# External packages
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel
# Mangum wraps our ASGI app and allows it to communicate with AWS Lambda
from mangum import Mangum
# from src.rag_app.query_rag import query_rag, QueryResponse

# Modules
from query_data import query_rag

app = FastAPI()
handler = Mangum(app)


class SubmitQueryRequest(BaseModel):
    query_text: str


@app.get("/")
def index():
    return {"Arun Widjaja": "Sample Response"}


@app.post("/submit_query")
def submit_query_endpoint(request: SubmitQueryRequest):
    query_response = query_rag(request.query_text)
    return query_response


# Main function is only for testing locally
if __name__ == "__main__":
    port = 8000
    print(f"Running the FastAPI server on port {port}.")
    uvicorn.run("api_handler:app", host="0.0.0.0", port=port)
