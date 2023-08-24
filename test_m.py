from aiohttp import web
import pytest

from main import ping, cats


@pytest.fixture
def cli(event_loop, aiohttp_client):
    app = web.Application()
    app.router.add_get('/ping', ping)
    app.router.add_get('/cats', cats)
    return event_loop.run_until_complete(aiohttp_client(app))


async def test_ping(cli):
    resp = await cli.get('/ping')
    assert resp.status == 200
    text = await resp.text()
    assert 'Cats Service. Version 0.1' in text


async def test_cats(cli):
    resp = await cli.get('/cats')
    assert resp.status == 200
    data = await resp.text()
    assert len(data) > 700


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
