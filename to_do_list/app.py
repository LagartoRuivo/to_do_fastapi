from http import HTTPStatus

from fastapi import FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse

from to_do_list.schemas.user import (
    UserDB,
    UserList,
    UserSchema,
    responseUserSchema,
)

app = FastAPI()

database = []


@app.get('/', status_code=HTTPStatus.OK)
def read_root():
    return {'message': 'Olá mundo!'}


@app.get('/html', status_code=HTTPStatus.OK, response_class=HTMLResponse)
def read_root_html():
    return """
    <html>
        <head>
            <title> Teste de retorno HTML </title>
        </head>
        <body>
            <h1> Meu primeiro teste sozinho! </h1>
        </body>
    """


@app.post(
    '/users/',
    status_code=HTTPStatus.CREATED,
    response_model=responseUserSchema,
)
def create_user(user: UserSchema):
    user_with_id = UserDB(id=len(database) + 1, **user.model_dump())

    database.append(user_with_id)

    return user_with_id


@app.get('/users/', response_model=UserList)
def read_users():
    return {'users': database}


@app.get('/users/{user_id}', response_model=responseUserSchema)
def read_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'message': 'Não foi encontrado nenhum usuário com esse id!',
                'id': user_id,
            },
        )
    user_with_id = database[user_id - 1]
    return user_with_id


@app.put('/users/{user_id}', response_model=responseUserSchema)
def update_user(user_id: int, user: UserSchema):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'message': 'Não foi encontrado nenhum usuário com esse id!',
                'id': user_id,
            },
        )
    user_with_id = UserDB(id=user_id, **user.model_dump())
    database[user_id - 1] = user_with_id
    return user_with_id


@app.delete('/users/{user_id}', response_model=responseUserSchema)
def delete_user(user_id: int):
    if user_id < 1 or user_id > len(database):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail={
                'message': 'Não foi encontrado nenhum usuário com esse id!',
                'id': user_id,
            },
        )
    user_with_id = database[user_id - 1]
    del database[user_id - 1]
    return user_with_id
