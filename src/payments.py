import time
from aiohttp import web
import aiohttp
import asyncio
from hashlib import md5
from .db.database import db
from .config import config

CREATE_ORDER_URL = 'https://tegro.money/api/createOrder/'

async def _webhook_handler(request):
    data = await request.json()
    order_id = data['order_id']
    await db.confirm_booking(order_id)
    booking = await db.get_booking(order_id)
    user = await db.get_user(booking.user)
    if user.referer_id:
        referer = await db.get_user(user.referer_id)
        if referer:
            await db.add_points(referer.id, int(config['services']['prices'][booking.massage]*0.13))
            if referer.referer_id:
                _referer = await db.get_user(referer.referer_id)
                if _referer:
                    await db.add_points(_referer.id, int(config['services']['prices'][booking.massage]*0.04))

    return web.Response(status=200)

async def _init_app(loop):
    app = web.Application(loop=loop, middlewares=[])
    app.router.add_post('/AAFrDOcFUcCywfKh_wdFv9Q-8HrxGLrz49I', _webhook_handler)
    web.run_app(app, host='0.0.0.0', port=49344, loop=loop)

def init_webhook():
    loop = asyncio.get_event_loop()
    loop.create_task(_init_app(loop))

async def _get_sign(data: dict) -> str:
    secret = config['payments']['secret']

    _data_list = sorted(list(data.items()))

    _data_to_hash = '&'.join([f'{k}&{v}' for e in _data_list for k, v in e]) + secret

    _sign_hash = md5(_data_to_hash)

    return _sign_hash.hexdigest()

async def create_order(order_id, amount) -> str:
    data = {
        'shop_id': config['payments']['shop_id'],
        'nonce': time.time(),
        'currency': 'RUB',
        'amount': amount,
        'order_id': order_id,
        'payment_system': 25
    }

    headers = {
        'Authorization': await _get_sign(data)
    }

    async with aiohttp.ClientSession(headers=headers) as session:
        async with session.post(CREATE_ORDER_URL, json=data) as response:
            data = await response.json()
            if not data['type'] == 'success':
                return None
            return data['data']['url']
