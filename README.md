# Asterisk Configuration Portal

Dialog manager service for Chat Bot based on FSM model. 

## Built With

* [FastAPI](https://fastapi.tiangolo.com/) - Web framework
* [Redis](https://pypi.org/project/redis/) - In memory cache DB for manage chat sessions
* [Python Dotenv](https://pypi.org/project/python-dotenv/) - For configs
* [Uvicorn](https://www.uvicorn.org/) - ASGI server


## Getting Started
### Installing

```
pip install -r packages.txt
```

### Run
1) Deploy Redis with config in core/configs/redis.conf

2) Build docker image
```
docker build -t {your image name} .
```

3) Run docker container

```
docker run --name {your container name} --net=host -d --rm {your image name}
```


## TODO

1) Add sub scenarios
2) Add events

## Authors

* **Maksim Avramenko** - [Balkonsky](https://github.com/balkonsky/)