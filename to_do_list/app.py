from http import HTTPStatus

from fastapi import Depends, FastAPI, status
from fastapi.exceptions import HTTPException
from fastapi.responses import HTMLResponse
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from to_do_list.db.connection import get_session
from to_do_list.db.models import User
from to_do_list.schemas.user import (
    Token,
    UserList,
    UserSchema,
    responseUserSchema,
)
from to_do_list.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
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
def create_user(user: UserSchema, session=Depends(get_session)):
    db_user = session.scalar(
        select(User).where(
            (User.username == user.username) | (User.email == user.email)
        )
    )

    if db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'Existe um usuário com esse name e/ou email!',
                'id': db_user.id,
            },
        )
    db_user = User(
        username=user.username,
        email=user.email,
        password=get_password_hash(user.password),
    )

    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.get('/users/', response_model=UserList)
def read_users(
    limit: int = 2,
    skip: int = 0,
    session: Session = Depends(get_session),
):
    users_on_db = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': users_on_db}


@app.get('/users/{user_id}', response_model=responseUserSchema)
def read_user(
    user_id: int,
    session=Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'Não existe nenhum usuário cadastrado com esse ID!',
                'id': user_id,
            },
        )
    return db_user


@app.put('/users/{user_id}', response_model=responseUserSchema)
def update_user(
    user_id: int,
    user: UserSchema,
    session=Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'Não existe nenhum usuário cadastrado com esse ID!',
                'id': user_id,
            },
        )
    if current_user.id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'Você não tem direitos para excluir o usuário!',
                'id': user_id,
            },
        )

    db_user.username = user.username
    db_user.email = user.email
    db_user.password = get_password_hash(user.password)
    session.add(db_user)
    session.commit()
    session.refresh(db_user)

    return db_user


@app.delete('/users/{user_id}')
def delete_user(
    user_id: int,
    session=Depends(get_session),
    current_user: str = Depends(get_current_user),
):
    db_user = session.scalar(select(User).where(User.id == user_id))
    if not db_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'Não existe nenhum usuário cadastrado com esse ID!',
                'id': user_id,
            },
        )
    if current_user.id != db_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={
                'message': 'Você não tem direitos para modificar o usuário!',
                'id': user_id,
            },
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'Usuário deletado com sucesso!', 'id': user_id}


@app.post('/token', response_model=Token)
def login_for_access_token(
    data: OAuth2PasswordRequestForm = Depends(),
    session=Depends(get_session),
):
    user = session.scalar(select(User).where(User.username == data.username))

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Usuário ou senha estão incorretos!'
        )

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}
