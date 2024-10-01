from typing import Annotated

from fastapi import APIRouter, Depends
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy import select
from sqlalchemy.orm import Session

from to_do_list.db.connection import get_session
from to_do_list.db.models import User
from to_do_list.schemas.user import Token
from to_do_list.security import (
    create_access_token,
    verify_password,
)

router = APIRouter(prefix='/auth', tags=['auth'])

T_Session = Annotated[Session, Depends(get_session)]
T_OAuth2PasswordRequestForm = Annotated[OAuth2PasswordRequestForm, Depends()]


@router.post('/token', response_model=Token)
def login_for_access_token(
    session: T_Session, data: T_OAuth2PasswordRequestForm
):
    user = session.scalar(select(User).where(User.username == data.username))

    if not user or not verify_password(data.password, user.password):
        raise HTTPException(
            status_code=400, detail='Usuário ou senha estão incorretos!'
        )

    access_token = create_access_token(data={'sub': user.username})

    return {'access_token': access_token, 'token_type': 'Bearer'}
