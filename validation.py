from typing import Union

from aiohttp import web

from db import get_cat


async def validation_cat(cat: dict) -> Union((str, int), (bool, bool)):
    """Валидация кота на входе"""
    name = cat.get('name')
    color = cat.get('color')
    tail_length = cat.get('tail_length')
    whiskers_length = cat.get('whiskers_length')

    if type(tail_length) is not int or tail_length < 0 or not tail_length:
        return '"tail_length" must be positive number', 400
    if tail_length >= 20:
        return "Cat can't have such a big tail, check it.", 400
    if type(
        whiskers_length
    ) is not int or whiskers_length < 0 or not whiskers_length:
        return '"whiskers_length" must be positive number', 400
    if whiskers_length >= 20:
        return "Cat can't have such a big whiskers, check them.", 400
    if not color:
        return "Cat can't be without color", 400
    if not name:
        return "Cat name can't be empty", 400
    if await get_cat(name):
        return 'Cat with this name is already exsist', 400
    return True, True


async def validation_request(request: web.Request) -> Union(
        (str, int), (set(str, str, int, int), bool)):
    """Валидация аттрибутов request"""
    attr = request.query.get('attribute', 'name')
    order = request.query.get('order', 'ASC')
    limit = request.query.get('limit', '10')
    offset = request.query.get('offset', '0')
    if attr.lower() not in [
        'name', 'color', 'tail_length', 'whiskers_length'
    ]:
        return ('No such attribute'), 400
    if order.lower() not in ['asc', 'desc']:
        return ('Check order'), 400
    if limit <= '0' or not limit.isdigit():
        return ('LIMIT must be more then 0'), 400
    if offset < '0' or not offset.isdigit():
        return ('OFFSET must be more or even 0'), 400
    return (attr, order, limit, offset), True
