# -*- coding: utf-8 -*-
import aiohttp
from sanic import Sanic
from sanic.response import json, text

app = Sanic()
tokendealer = 'http://0.0.0.0:8000/app/token/verify'


@app.route('/')
async def plus(request):
    return json({"Hello": "world"})


@app.middleware('request')
async def print_on_request(request):
    authorization = request.headers.get('authorization', None)
    if authorization is None:
        return text(status=401)
    iden, token = authorization.split()
    async with aiohttp.ClientSession() as session:
        async with session.post(tokendealer, json={'access_token': token}) as resp:
            if not (resp.status == 200):
                return text('', status=401)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8888)
