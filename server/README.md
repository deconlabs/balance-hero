# How to Use

## Preconditions
```bash
cd server/
```
```bash
npm install
```

## Change Port#
Default port# is ```3000```.

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
```bash
curl localhost:3000/timer
```

## Set Stack
```bash
curl -H "Content-type:application/json" --data "{\"stack\" : 100}" http://127.0.0.1:3000/setStack
```

## Set Timer
milli-seconds
```bash
curl -H "Content-type:application/json" --data "{\"timer\" : 10000}" http://127.0.0.1:3000/setTimer
```

## Stop Server
```bash
curl -X POST localhost:3000/stop
```

## Cleanup
```bash
sh cleanup.sh
```
