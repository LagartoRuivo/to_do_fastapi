from http import HTTPStatus

from fastapi import FastAPI
from fastapi.responses import HTMLResponse

from to_do_list.routes.auth import router as auth_router
from to_do_list.routes.user import router as user_router

app = FastAPI()

app.include_router(user_router)
app.include_router(auth_router)


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
