# from fastapi import FastAPI
# from pydantic import BaseModel

# app = FastAPI()

# @app.get("/hello")
# async def hello():
#     return "Welcome to FastAPI tutorial"

# @app.get("/hello/{name}")
# async def hello_name(name: str):
#     return f"Welcome {name}"

# class User(BaseModel):
#     name: str
#     age: int

# @app.post("/user")
# async def create_user(user: User):
#     return {
#         "message": "User created successfully",
#         "name": user.name,
#         "age": user.age
#     }


from fastapi import FastAPI
from pydantic import BaseModel
from app import run_orchestrator

app = FastAPI(title="Research Summarization API")

class ResearchRequest(BaseModel):
    topic: str

@app.post("/research")
async def research_pipeline(request: ResearchRequest):
    result = run_orchestrator(request.topic)
    return result
