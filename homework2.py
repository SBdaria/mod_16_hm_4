from fastapi import FastAPI, Path, HTTPException
from typing import Annotated, List
from pydantic import BaseModel

app = FastAPI()

users = []


class User(BaseModel):
    id: int
    username: str
    age: int


@app.get('/users')
async def get_dict() -> List[User]:
    return users


@app.post('/user/{username}/{age}')
async def add_in_dict(
        user: User,
        username: Annotated[str, Path(min_length=5, max_length=20, description='Enter username', example='DariDari')],
        age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='27')]) -> User:
    if users:
        user.id = users[-1].id + 1
    else:
        user.id = 1
    user.username = username
    user.age = age
    users.append(user)
    return user


@app.put('/user/{user_id}/{username}/{age}')
async def update_dict(user_id: Annotated[int, Path(description='Enter ID', example='1')],
                      username: Annotated[
                          str, Path(min_length=5, max_length=20, description='Enter username', example='DariDari')],
                      age: Annotated[int, Path(ge=18, le=120, description='Enter age', example='27')]) -> User:
    try:
        for i in users:
            if i.id == user_id:
                i.username = username
                i.age = age
                return i
        raise Exception
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")


@app.delete('/user/{user_id}')
async def delete_user(user_id: Annotated[int, Path(description='Enter ID', example='1')]) -> User:
    try:
        for i in users:
            if i.id == user_id:
                users.remove(i)
                return i
        raise Exception
    except Exception:
        raise HTTPException(status_code=404, detail="User not found")
