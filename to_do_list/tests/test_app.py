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
