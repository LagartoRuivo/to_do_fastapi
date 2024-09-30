from http import HTTPStatus

from to_do_list.schemas.user import responseUserSchema


def test_read_root_deve_retornar_ok_e_ola_mundo(client):
    # Arrange (Organização do teste)

    response = client.get('/')  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {'message': 'Olá mundo!'}  # Assert (Afirmação)


def test_read_root_html_deve_retornar_ok_e_uma_pagina_html(client):
    response = client.get('/html')  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert (
        response.text
        == """
    <html>
        <head>
            <title> Teste de retorno HTML </title>
        </head>
        <body>
            <h1> Meu primeiro teste sozinho! </h1>
        </body>
    """
    )  # Assert (Afirmação)


def test_create_user(client):
    response = client.post(
        '/users/',
        json={
            'username': 'teste_cod',
            'password': 'pass_cod',
            'email': 'email_cod@teste.com',
        },
    )  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.CREATED  # Assert (Afirmação)
    assert response.json() == {
        'username': 'teste_cod',
        'email': 'email_cod@teste.com',
        'id': 1,
    }


def test_create_user_username_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste',
            'password': 'tsttst',
            'email': 'email_cod@teste.com',
        },
    )  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert (Afirmação)
    assert response.json() == {
        'detail': {
            'message': 'Existe um usuário com esse name e/ou email!',
            'id': 1,
        }
    }


def test_create_user_email_already_exist(client, user):
    response = client.post(
        '/users/',
        json={
            'username': 'Teste_email',
            'password': 'tsttst',
            'email': 'teste@test.com',
        },
    )  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert (Afirmação)
    assert response.json() == {
        'detail': {
            'message': 'Existe um usuário com esse name e/ou email!',
            'id': 1,
        }
    }


def test_read_users_with_no_users(client):
    response = client.get('/users/')  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {'users': []}


def test_read_users_with_users(client, user):
    user_schema = responseUserSchema.model_validate(user).model_dump()

    response = client.get('/users/')  # Act (Ação do teste)
    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {'users': [user_schema]}


def test_update_user(client, user, token):
    response = client.put(
        f'/users/{user.id}',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'teste_nick',
            'password': 'pass_nick',
            'email': 'email_nick@teste.com',
        },
    )  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {
        'username': 'teste_nick',
        'email': 'email_nick@teste.com',
        'id': 1,
    }


def test_update_user_not_exist(client, user, token):
    response = client.put(
        '/users/4',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'username': 'teste_nick',
            'password': 'pass_nick',
            'email': 'email_nick@teste.com',
        },
    )  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert (Afirmação)
    assert response.json() == {
        'detail': {
            'message': 'Não existe nenhum usuário cadastrado com esse ID!',
            'id': 4,
        }
    }


def test_read_user(client, user, token):
    response = client.get(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {
        'username': 'Teste',
        'email': 'teste@test.com',
        'id': 1,
    }


def test_read_user_not_exist(client, user, token):
    response = client.get(
        '/users/4', headers={'Authorization': f'Bearer {token}'}
    )  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert (Afirmação)
    assert response.json() == {
        'detail': {
            'message': 'Não existe nenhum usuário cadastrado com esse ID!',
            'id': 4,
        }
    }


def test_delete_user(client, user, token):
    response = client.delete(
        f'/users/{user.id}', headers={'Authorization': f'Bearer {token}'}
    )  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {
        'message': 'Usuário deletado com sucesso!',
        'id': 1,
    }


def test_delete_user_not_exist(client, user, token):
    response = client.delete(
        '/users/4', headers={'Authorization': f'Bearer {token}'}
    )  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.BAD_REQUEST  # Assert (Afirmação)
    assert response.json() == {
        'detail': {
            'message': 'Não existe nenhum usuário cadastrado com esse ID!',
            'id': 4,
        }
    }
