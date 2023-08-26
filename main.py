from aiohttp import web
from aiohttp_swagger import setup_swagger

from db import cats_list, new_cat_to_db
from validation import validation_cat, validation_request


routes = web.RouteTableDef()
app = web.Application()


@routes.get('/ping')
async def ping(request):
    """Проврека работы сервера"""
    return web.Response(text='Cats Service. Version 0.1')


@routes.get('/cats')
async def cats(requset):
    """Функция для возврата списка котов с дополнительными параметрами"""
    params_or_text, status = await validation_request(requset)
    if status == 400:
        return web.Response(text=params_or_text, status=status)
    all_cats, status = await cats_list(*params_or_text)
    return web.json_response(data=all_cats, status=status)


@routes.post('/cat')
async def post_cat(request):
    """Добавление котов"""
    new_cat = await request.json()
    text, status = await validation_cat(new_cat)
    if status == 400:
        return web.Response(text=text, status=status)
    status = await new_cat_to_db(new_cat)
    return web.Response(text='New cat sucsessfuly added', status=status)


if __name__ == '__main__':
    app.add_routes(routes)
    setup_swagger(app, swagger_url="/redoc")
    web.run_app(app)
