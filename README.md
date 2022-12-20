# rpi-logger

Use below command to build docker image compatible with RPI
```
docker build --platform=linux/arm/v7 -t lakshanbanneheke/rpi-metrics-logger:latest -f Dockerfile .
```

Push to the DockerHub repo
```
docker push lakshanbanneheke/rpi-metrics-logger:latest
```