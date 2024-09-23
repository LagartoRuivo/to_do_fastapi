from http import HTTPStatus


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


def test_read_users(client):
    response = client.get('/users/')  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {
        'users': [
            {
                'username': 'teste_cod',
                'email': 'email_cod@teste.com',
                'id': 1,
            }
        ]
    }


def test_update_user(client):
    response = client.put(
        '/users/1',
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


def test_update_user_not_exist(client):
    response = client.put(
        '/users/4',
        json={
            'username': 'teste_nick',
            'password': 'pass_nick',
            'email': 'email_nick@teste.com',
        },
    )  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Afirmação)
    assert response.json() == {
        'detail': {
            'message': 'Não foi encontrado nenhum usuário com esse id!',
            'id': 4,
        }
    }


def test_read_user(client):
    response = client.get('/users/1')  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {
        'username': 'teste_nick',
        'email': 'email_nick@teste.com',
        'id': 1,
    }


def test_read_user_not_exist(client):
    response = client.get('/users/4')  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Afirmação)
    assert response.json() == {
        'detail': {
            'message': 'Não foi encontrado nenhum usuário com esse id!',
            'id': 4,
        }
    }


def test_delete_user(client):
    response = client.delete('/users/1')  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.OK  # Assert (Afirmação)
    assert response.json() == {
        'username': 'teste_nick',
        'email': 'email_nick@teste.com',
        'id': 1,
    }


def test_delete_user_not_exist(client):
    response = client.delete('/users/4')  # Act (Ação do teste)

    assert response.status_code == HTTPStatus.NOT_FOUND  # Assert (Afirmação)
    assert response.json() == {
        'detail': {
            'message': 'Não foi encontrado nenhum usuário com esse id!',
            'id': 4,
        }
    }
