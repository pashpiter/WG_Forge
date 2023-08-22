import asyncpg
import asyncio

from settings import config


async def create_connection():
    database, user, password, host, port = config.values()
    try:
        conn = await asyncpg.connect(
            user=user, host=host, port=port, database=database,
            password=password
        )
    except Exception as e:
        raise e
    return conn


async def cats_color_count():
    """Подсчет количества котов по цветам"""
    try:
        conn = await create_connection()
        await conn.execute(
            '''INSERT INTO cat_colors_info (color, count)
            SELECT color, count(color) FROM cats GROUP BY color;'''
        )
    except Exception as e:
        raise e


async def cats_list(request):
    try:
        conn = await create_connection()
        attr = request.query.get('attribute', 'name')
        order = request.query.get('order', 'ASC')
        r = await conn.fetch(
            f'SELECT name, color, tail_length, whiskers_length FROM cats '
            f'ORDER BY {attr} {order};'
        )
    except Exception as e:
        raise e
    return [dict(c) for c in r]


# async def cats_stats():
#     try:
#         conn = await create_connection()
#         await conn.execute(
#             '''INSERT INTO cats_stat (tail_length_mean, tail_length_median,
#             tail_length_mode, whiskers_length_mean, whiskers_length_median,
#             whiskers_length_mode)
#             SELECT AVG(tail_length), 
#             '''
#         )
#     except Exception as e:
#         raise e

if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cats_color_count())
