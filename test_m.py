import pytest
from aiohttp import web
from aiohttp.test_utils import TestClient

from db import delete_cat, get_cat
from main import cats, ping, post_cat


@pytest.fixture
def cli(loop, aiohttp_client) -> TestClient:
    app = web.Application()
    app.router.add_get('/ping', ping)
    app.router.add_get('/cats', cats)
    app.router.add_post('/cat', post_cat)
    # print(type(aiohttp_client(app)))
    return loop.run_until_complete(aiohttp_client(app))


async def test_ping(cli: TestClient) -> None:
    """Проверка доступа к сервису"""
    resp = await cli.get('/ping')
    assert resp.status == 200
    text = await resp.text()
    assert 'Cats Service. Version 0.1' in text


async def test_cats(cli: TestClient) -> None:
    """Общая проверка получения списка котов"""
    resp = await cli.get('/cats')
    assert resp.status == 200


async def test_cats_valid_params(cli: TestClient) -> None:
    """Проверка получения списка котов со всеми атрибутами"""
    params = '?attribute=color&order=asc&offset=1&limit=2'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200
    data = await resp.text()
    data = eval(data)
    assert data[0]['color'] == 'black'
    assert len(data) == 2


async def test_cats_valid_attr(cli: TestClient) -> None:
    """Проверка получения списка котов с корректными атрибутами"""
    params = '?attribute=name&order=asc'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200
    params = '?attribute=color&order=desc'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200


async def test_cats_valid_offset(cli: TestClient) -> None:
    """Проверка получения списка котов с валидным offset"""
    params = '?offset=1'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200
    params = '?offset=100'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200


async def test_cats_valid_limit(cli: TestClient) -> None:
    """Проверка получения списка котов с валидным limit"""
    params = '?limit=1'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200
    params = '?limit=100'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200


async def test_cats_invalid_attr(cli: TestClient) -> None:
    """Проверка получения списка котов с невалидным аттрибутом"""
    params = '?attribute=nnam&order=asc'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400


async def test_cats_invalid_order(cli: TestClient) -> None:
    """Проверка получения списка котов с невалидным порядком"""
    params = '?attribute=name&order=up'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400


async def test_cats_invalid_offset(cli: TestClient) -> None:
    """Проверка получения списка котов с невалидным offset"""
    params = '?offset=-1'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400
    params = '?offset=-100'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400


async def test_cats_invalid_limit(cli: TestClient) -> None:
    """Проверка получения списка котов с невалидным limit"""
    params = '?limit=-1'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400
    params = '?limit=-100'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400
    params = '?limit=0'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400


async def test_new_cat(cli: TestClient) -> None:
    """Проверка добавления нового кота"""
    new_cat = ("{\"name\": \"Test_cat\", \"color\": \"black\", "
               "\"tail_length\": 11, \"whiskers_length\": 11}")
    await delete_cat(eval(new_cat)['name'])
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 201
    cat = await get_cat(eval(new_cat)['name'])
    assert cat['name'] == 'Test_cat'
    assert cat['color'] == 'black'
    assert cat['tail_length'] == 11
    assert cat['whiskers_length'] == 11
    await delete_cat(eval(new_cat)['name'])


async def test_new_cat_invalid_name(cli: TestClient) -> None:
    """Проверка добаления кота с невалидным именем"""
    new_cat = ("{\"name\": \"Test_cat\", \"color\": \"black\", "
               "\"tail_length\": 11, \"whiskers_length\": 11}")
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 201
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 400
    await delete_cat(eval(new_cat)['name'])
    new_cat = ("{\"name\": \"\", \"color\": \"black\", \"tail_length\": 11, "
               "\"whiskers_length\": 11}")
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 400


async def test_new_cat_invalid_tail_length(cli: TestClient) -> None:
    """Проверка добаления кота с невалидной длинной хвоста"""
    new_cat = ("{\"name\": \"Test_cat\", \"color\": \"black\", "
               "\"tail_length\": -11, \"whiskers_length\": 11}")
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 400
    new_cat = ("{\"name\": \"Test_cat\", \"color\": \"black\", "
               "\"tail_length\": \"check\", \"whiskers_length\": 11}")
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 400


async def test_new_cat_invalid_whiskers_length(cli: TestClient) -> None:
    """Проверка добаления кота с невалидной длинной усов"""
    new_cat = ("{\"name\": \"Test_cat\", \"color\": \"black\", "
               "\"tail_length\": 11, \"whiskers_length\": -11}")
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 400
    new_cat = ("{\"name\": \"Test_cat\", \"color\": \"black\", "
               "\"tail_length\": 11, \"whiskers_length\": \"check\"}")
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 400
