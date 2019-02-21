import asyncio
import os
import random
import psutil

from quart import Quart
from quart import websocket

app = Quart(__name__)

@app.websocket('/ws')
async def ws():
    proc = psutil.Process(os.getpid())
    data = bytearray(random.getrandbits(8) for _ in range(2**16))
    data_sent = 0
    mem_used = proc.memory_info().rss
    while data_sent < 10**9:
        await websocket.send(data)
        await asyncio.sleep(0.01)
        data_sent += len(data)
        mem_used_now = proc.memory_info().rss
        if abs(mem_used_now - mem_used) > 2**23:
            # log every time memory use changes by 8MB
            print("Using %u" % mem_used_now)
            mem_used = mem_used_now

app.run(host='0.0.0.0', port=8080)
