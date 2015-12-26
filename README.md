# myadventure-front

## Build Docker image
```
docker build -t="myadventure/myadventure-front" .
```

## Run Docker container
```
docker run -P -t -i -v $(CURDIR)/app:/opt/app myadventure/myadventure-front
```
