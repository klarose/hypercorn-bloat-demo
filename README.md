# Hypercorn Bloat

This demonstrates an unbounded buffer in hypercorn 0.5.2 when using WebSockets.
The issue occurs if the client connection is much slower than the server produces content.
You can easily simulate the problem on Linux by using this python script in conjunction with
an iptables rule to artificially slow down the client connection.

## Demo

```bash
# Drop a large amount of traffic to slow down the client connection
sudo iptables -A INPUT -p tcp --source-port 8080 -m statistic --mode random --probability 0.50 -j DROP
python3.7 -m venv /tmp/test-env
source /tmp/test-env/bin/activate
pip3 install -r requirements.txt
python3 server.py
```

In another window:

```bash
curl --header "Connection: Upgrade" \
     --header "Upgrade: websocket" \
     --header "Host:  localhost:8080" \
     --header "Sec-WebSocket-Key: SGVsbG8sIHdvcmxkIQ==" \
     --header "Sec-WebSocket-Version: 13" \
     http://localhost:8080/ws --output /dev/null
```

You should see the server outputting that its memory usage is increasing, like this:

```text
Running on https://0.0.0.0:8080 (CTRL + C to quit)
[2019-02-21 13:51:29,510] ASGI Framework Lifespan error, continuing without Lifespan support
[2019-02-21 13:51:36,712] 127.0.0.1:40150 GET /ws 1.1 101 - 19639
Using 39485440
Using 47943680
Using 56590336
Using 65048576
Using 73695232
Using 82345984
Using 90996736
Using 99647488
Using 108306432
Using 116957184
Using 125607936
Using 134258688
Using 142909440
...
```

To clean up:

```bash
sudo iptables -D INPUT -p tcp --source-port 8080 -m statistic --mode random --probability 0.50 -j DROP
rm -rf /tmp/test-env
```
