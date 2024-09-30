from http import HTTPStatus

from jwt import decode

from to_do_list.security import ALGORITHM, SECRET_KEY, create_access_token


def test_jwt():
    data = {'sub': 'nickolas'}
    token = create_access_token(data)

    decoded = decode(token, SECRET_KEY, algorithms=[ALGORITHM])

    assert decoded['sub'] == data['sub']
    assert decoded['exp']


def test_jwt_with_invalid_token(client):
    response = client.delete(
        '/users/1', headers={'Authorization': 'Bearer token_invalido'}
    )

    assert response.status_code == HTTPStatus.UNAUTHORIZED
    assert response.json() == {
        'detail': 'Não foi possível validar as credenciais'
    }


def test_get_token(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': user.clean_password},
    )

    token = response.json()
    assert response.status_code == HTTPStatus.OK
    assert token['token_type'] == 'Bearer'
    assert 'access_token' in token


def test_get_token_with_wrong_user_or_password(client, user):
    response = client.post(
        '/token',
        data={'username': user.username, 'password': '2151241'},
    )

    token = response.json()

    assert response.status_code == HTTPStatus.BAD_REQUEST
    assert token['detail'] == 'Usuário ou senha estão incorretos!'
