from bson import ObjectId
from fastapi import APIRouter, status,Response
from passlib.hash import sha256_crypt
from starlette.status import HTTP_204_NO_CONTENT

from models.user import User, Card
from config.db import collection, collection_card
from schemas.schemas import user_entity, users_entity, identify_card

user = APIRouter()

@user.post('/login', tags = ['users'])
async def login(user: User):
    user = dict(user)
    res = collection.find_one({'user_name': user['user_name']})
    if res is None:
        return False
    else:
        return sha256_crypt.verify(user['password'], res['password'])

@user.post('/signup', tags = ['users'])
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


@user.get('/cards/{user_name}', response_model = Card,  tags = ['cards'])
async def get_card_information(user_name: str):
    return identify_card(collection_card.find_one({'user_name': user_name}))


@user.post('/cards', tags = ['cards'])
async def register_card(card: Card):
    new_card = dict(card)
    del new_card['id']
    check_cccd = collection_card.find_one({'so_cccd': new_card['so_cccd']})
    if check_cccd:
        return str('existed')
    id = collection_card.insert_one(new_card).inserted_id
    card = collection_card.find_one({'id': id})
    
    return False if card is None else True


