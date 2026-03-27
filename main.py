from fastapi import FastAPI

app = FastAPI()
@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Server working"}

@app.get("/greet/{name}")
async def greet_name(name:str)-> dict[str, str]:
    return {"message": f"Hello {name}"}