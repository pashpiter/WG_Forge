from db import get_cat


async def validation_cat(cat):
    if cat['tail_length'] < 0:
        return '"tail_length" must be positive', 400
    if cat['tail_length'] >= 20:
        return "Cat can't have such a big tail, check it.", 400
    if cat['whiskers_length'] < 0:
        return '"whiskers_length" must be positive', 400
    if cat['whiskers_length'] >= 20:
        return "Cat can't have such a big whiskers, check them.", 400
    if not cat['color']:
        return "Cat can't be without color", 400
    if not cat['name']:
        return "Cat name can't be empty", 400
    if await get_cat(cat['name']):
        return 'Cat with this name is already exsist', 400
    return True, True


async def validation_request(request):
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
    if limit <= '0':
        return ('LIMIT must be more then 0'), 400
    if offset < '0':
        return ('OFFSET must be more or even 0'), 400
    return (attr, order, limit, offset), True
