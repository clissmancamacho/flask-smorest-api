# CONTRIBUTING

## How to run the Dockerfile locally

```
docker build --target debug -t flask-smorest-api:debug .
 docker run -dp 5005:5000 -p 5678:5678 -w /app -v "$(pwd):/app" flask-smorest-api:debug
 Initialize Debugger
```
