import pytest
from aiohttp import web

from db import delete_cat, get_cat
from main import cats, ping, post_cat


@pytest.fixture
def cli(event_loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/ping', ping)
    app.router.add_get('/cats', cats)
    app.router.add_post('/cat', post_cat)
    return event_loop.run_until_complete(aiohttp_client(app))


async def test_ping(cli):
    resp = await cli.get('/ping')
    assert resp.status == 200
    text = await resp.text()
    assert 'Cats Service. Version 0.1' in text


async def test_cats(cli):
    resp = await cli.get('/cats')
    assert resp.status == 200


async def test_cats_valid_params(cli):
    params = '?attribute=color&order=asc&offset=1&limit=2'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200
    data = await resp.text()
    data = eval(data)
    assert data[0]['color'] == 'black'
    assert len(data) == 2


async def test_cats_valid_attr(cli):
    params = '?attribute=name&order=asc'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200
    params = '?attribute=color&order=desc'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200


async def test_cats_valid_offset(cli):
    params = '?offset=1'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200
    params = '?offset=100'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200


async def test_cats_valid_limit(cli):
    params = '?limit=1'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200
    params = '?limit=100'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 200


async def test_cats_invalid_attr(cli):
    params = '?attribute=nnam&order=asc'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400


async def test_cats_invalid_order(cli):
    params = '?attribute=name&order=up'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400


async def test_cats_invalid_offset(cli):
    params = '?offset=-1'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400
    params = '?offset=-100'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400


async def test_cats_invalid_limit(cli):
    params = '?limit=-1'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400
    params = '?limit=-100'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400
    params = '?limit=0'
    resp = await cli.get(f'/cats{params}')
    assert resp.status == 400


async def test_new_cat(cli):
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


async def test_new_cat_invalid_name(cli):
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


async def test_new_cat_invalid_tail_length(cli):
    new_cat = ("{\"name\": \"Test_cat\", \"color\": \"black\", "
               "\"tail_length\": -11, \"whiskers_length\": 11}")
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 400
    new_cat = ("{\"name\": \"Test_cat\", \"color\": \"black\", "
               "\"tail_length\": \"check\", \"whiskers_length\": 11}")
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 400


async def test_new_cat_invalid_whiskers_length(cli):
    new_cat = ("{\"name\": \"Test_cat\", \"color\": \"black\", "
               "\"tail_length\": 11, \"whiskers_length\": -11}")
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 400
    new_cat = ("{\"name\": \"Test_cat\", \"color\": \"black\", "
               "\"tail_length\": 11, \"whiskers_length\": \"check\"}")
    resp = await cli.post('/cat', data=new_cat)
    assert resp.status == 400
