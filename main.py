from fastapi import FastAPI
from typing import Optional

app = FastAPI()
@app.get("/")
async def read_root() -> dict[str, str]:
    return {"message": "Server working"}

# Any parameter in function, will be considered a query parameter if not defined in path. Defined in path is path parameter
@app.get("/greet")
async def greet_name(name: Optional[str] = "User", age: int = 0)-> dict[str, str]:
    return {"message": f"Hello {name} !! Age {age}"}

