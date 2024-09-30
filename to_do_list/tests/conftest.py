import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy.pool import StaticPool

from to_do_list.app import app
from to_do_list.db.connection import get_session
from to_do_list.db.models import User, table_registry
from to_do_list.security import get_password_hash


@pytest.fixture
def token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.clean_password},
    )
    print(response.json())
    return response.json()['access_token']


@pytest.fixture
def user(session):
    pwd = 'testtest'
    user = User(
        username='Teste',
        email='teste@test.com',
        password=get_password_hash(pwd),
    )
    session.add(user)
    session.commit()
    session.refresh(user)

    user.clean_password = pwd  # Monkey Patch

    return user


@pytest.fixture
def client(session):
    def get_session_override():
        return session

    with TestClient(app) as client:
        app.dependency_overrides[get_session] = get_session_override

        yield client

    app.dependency_overrides.clear()


@pytest.fixture
def session():
    engine = create_engine(
        'sqlite:///:memory:',
        connect_args={'check_same_thread': False},
        poolclass=StaticPool,
    )

    table_registry.metadata.create_all(engine)

    # Gerenciamento de contexto
    with Session(engine) as session:
        yield session

    table_registry.metadata.drop_all(engine)
