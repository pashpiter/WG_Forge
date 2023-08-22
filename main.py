from aiohttp import web

from db import cats_list


routes = web.RouteTableDef()
app = web.Application()


@routes.get('/ping')
async def ping(request):
    return web.Response(text='Cats Service. Version 0.1')


@routes.get('/cats')
async def cats(requset):
    all_cats = await cats_list(requset)
    return web.json_response(data=all_cats, status=200)

if __name__ == '__main__':
    app.add_routes(routes)
    web.run_app(app)
