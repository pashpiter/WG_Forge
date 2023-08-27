import asyncio
from typing import Union

import asyncpg

from settings import config


async def create_connection() -> asyncpg.Connection:
    """Подключение к базе данных"""
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


async def cats_list(
        attr: str, order: str, limit: int, offset: int) -> (list[dict], int):
    """Получение списка котов с доп аттрибутами по запросу из базы"""
    try:
        conn = await create_connection()
        r = await conn.fetch(
            f'SELECT name, color, tail_length, whiskers_length FROM cats '
            f'ORDER BY {attr} {order} LIMIT {limit} OFFSET {offset}'
        )
    except Exception as e:
        raise e
    return [dict(c) for c in r], 200


async def new_cat_to_db(cat: dict) -> int:
    """Добавление нового кота в базу"""
    try:
        conn = await create_connection()
        await conn.execute(
            'INSERT INTO cats (name, color, tail_length, whiskers_length) '
            'VALUES ($1, $2, $3, $4);', cat['name'], cat['color'],
            cat['tail_length'], cat['whiskers_length']
        )
    except Exception as e:
        raise e
    return 201


async def get_cat(name: str) -> Union(dict, None):
    """Получение одного кота из базы по имени"""
    try:
        conn = await create_connection()
        cat = await conn.fetch(
            'SELECT * FROM cats WHERE name = $1', name
        )
    except Exception as e:
        raise e
    return dict(cat[0]) if cat else None


async def delete_cat(name: str) -> bool:
    """Удаление кота из базы по имени"""
    try:
        conn = await create_connection()
        await conn.execute(
            'DELETE FROM cats WHERE name = $1', name
        )
    except Exception as e:
        raise e
    return True


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(cats_color_count())
