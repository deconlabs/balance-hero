# How to Use

## Preconditions
```bash
cd server/
```
```bash
npm install
```

## Change Port#
* Default port# is ```3000```.

```bash
export HTTP_PORT=3001
```
*or*
```bash
env:HTTP_PORT=3001
```

## Run Server
```bash
npm start
```

## Get Stack
```bash
curl localhost:3000/stack
```

## Get Timer
* UNIX timestamp.   
* Return setting value, start time, and time remaining.
```bash
curl localhost:3000/timer
```

## Get Orderbook
```bash
curl localhost:3000/orderBook
```
You can pretty-print JSON with:
```bash
curl http://127.0.0.1:3000/orderBook | python -m json.tool
```
* result: 
```JSON
{
    "orderBook": [
        {
            "amount": 11,
            "id": 2,
            "when": 100
        },
        {
            "amount": 7,
            "id": 0,
            "when": 89
        },
        {
            "amount": 32,
            "id": 1,
            "when": 82
        },
        {
            "amount": 32,
            "id": 1,
            "when": 50
        }
    ]
}
```

## Get Status
* isAlive: ```true``` when episode runs, ```false``` otherwise.
* isSuccess: ```true``` when ```stack==0 && isAlive```, ```false``` otherwise.
```bash
curl localhost:3000/stack
```

## Set Stack
```bash
curl -H "Content-type:application/json" --data "{\"stack\" : 100}" http://127.0.0.1:3000/setStack
```

## Set Timer
* milli-seconds
```bash
curl -H "Content-type:application/json" --data "{\"timer\" : 10000}" http://127.0.0.1:3000/setTimer
```

## Purchase
```bash
curl -H "Content-type:application/json" --data "{\"id\" : 2, \"amount\" : 11}" http://127.0.0.1:3000/purchase
```

## Reset
* reset stacks
* reset (cancel) timer
```bash
curl -X POST localhost:3000/stop
```

## Stop Server
```bash
curl -X POST localhost:3000/stop
```

## Cleanup
```bash
sh cleanup.sh
```
