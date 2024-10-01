from http import HTTPStatus
from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.exceptions import HTTPException
from sqlalchemy import select
from sqlalchemy.orm import Session

from to_do_list.db.connection import get_session
from to_do_list.db.models import User
from to_do_list.schemas.user import (
    UserList,
    UserSchema,
    responseUserSchema,
)
from to_do_list.security import (
    get_current_user,
    get_password_hash,
)

router = APIRouter(prefix='/users', tags=['users'])

T_Session = Annotated[Session, Depends(get_session)]
T_CurrentUser = Annotated[User, Depends(get_current_user)]


@router.post(
    '/',
    status_code=HTTPStatus.CREATED,
    response_model=responseUserSchema,
)
def create_user(user: UserSchema, session: T_Session):
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


@router.get('/', response_model=UserList)
def read_users(session: T_Session, limit: int = 2, skip: int = 0):
    users_on_db = session.scalars(select(User).limit(limit).offset(skip))
    return {'users': users_on_db}


@router.get('/{user_id}', response_model=responseUserSchema)
def read_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
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
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                'message': 'Você não tem direitos para ver o usuário!',
                'id': user_id,
            },
        )

    return db_user


@router.put('/{user_id}', response_model=responseUserSchema)
def update_user(
    user_id: int,
    user: UserSchema,
    session: T_Session,
    current_user: T_CurrentUser,
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
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                'message': 'Você não tem direitos para modificar o usuário!',
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


@router.delete('/{user_id}')
def delete_user(
    user_id: int,
    session: T_Session,
    current_user: T_CurrentUser,
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
            status_code=status.HTTP_403_FORBIDDEN,
            detail={
                'message': 'Você não tem direitos para deletar o usuário!',
                'id': user_id,
            },
        )

    session.delete(db_user)
    session.commit()

    return {'message': 'Usuário deletado com sucesso!', 'id': user_id}
