from bson import ObjectId
from fastapi import APIRouter, status,Response
from passlib.hash import sha256_crypt
from starlette.status import HTTP_204_NO_CONTENT

from models.user import User
from config.db import collection
from schemas.schemas import user_entity, users_entity

user = APIRouter()

@user.post('/login')
async def login(user: User):
    user = dict(user)
    res = collection.find_one({'user_name': user['user_name']})
    if res is None:
        return False
    else:
        return sha256_crypt.verify(user['password'], res['password'])

@user.post('/signup')
async def create_user(user: User):
    new_user = dict(user)
    new_user["password"] = sha256_crypt.encrypt(new_user["password"])
    del new_user["id"]
    check_username = collection.find_one({'user_name' : new_user['user_name']})
    if check_username:
        return str('existed')
    id = collection.insert_one(new_user).inserted_id
    user = collection.find_one({"_id": id})
    
    return False if user is None else True



@user.get('/users', response_model = list[User], tags = ['users'])
async def find_all_user():
    return users_entity(collection.find())



@user.put('/users/{id}', response_model = User, tags =['users'])
async def update_password(id: str, user: User):
    user = dict(user)
    del user['id']
    del user['user_name']
    collection.find_one_and_update(
        {'_id' : ObjectId(id)},
        {'$set' : user}
    )
    return user_entity(collection.find_one({"_id": ObjectId(id)}))


@user.delete("/users/{id}", status_code=status.HTTP_204_NO_CONTENT, tags=["users"])
async def delete_user(id: str):
    collection.find_one_and_delete({
        "_id": ObjectId(id)
    })
    return Response(status_code=HTTP_204_NO_CONTENT)