# Preconditions
```bash
cd server/
```
```bash
npm install
```

# Change Port#
Default port# is ```3000```.

```bash
export HTTP_PORT=3001
```
*or*
```bash
env:HTTP_PORT=3001
```

# Run Server
```bash
npm start
```

# Get Message
```bash
curl localhost:3000/message
```

# Stop Server
```bash
curl -X POST localhost:3000/stop
```

# Cleanup
```bash
sh cleanup.sh
```
