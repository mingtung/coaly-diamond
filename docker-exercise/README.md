# Coding exercise: docker

This is a coding exercise with docker.

## Background and Terminology

* [what is docker and how to use it with python](https://djangostars.com/blog/what-is-docker-and-how-to-use-it-with-python/)

* Container: a running instance, instantiated/created from a _image_, that encapsulated required software. A container can expose ports and volumes to interact with other containers and the outer world. Container don't keep state.

* Image: that is used to build and save snapshots of an environment

* Dockerfile: a file that contains a set of instructions to create an _image_

* Port: a TCP/ port. ...

* Volume: a shared folder that is initialized when a container is created. It is designed to persist data (unlike container).

## Installation and tools

* install docker Desktop for Mac from [Docker CE Desktop for Mac](https://hub.docker.com/editions/community/docker-ce-desktop-mac)

* `docker` (cli):
  ```
  $ docker --version
  Docker version 18.09.2, build 6247962
  ```
* `docker-compose`: for orchestrating a multi-container application into a single app ([dockerizing Flask with Compose by Real Python](https://realpython.com/dockerizing-flask-with-compose-and-machine-from-localhost-to-the-cloud/))

  ```
  $ docker-compose --version
  docker-compose version 1.23.2, build 1110ad01
  ```

## Example

* Example 1: creating a docker container for Flask application. (Reference to [Real Python](https://realpython.com/docker-in-action-fitter-happier-more-productive/))

  * the instructions of creating an image for the "web" app is specified in [`./web/Dockerfile`](./web/Dockerfile)

  * build the image and run the containers in the backgroud, by the specification in [`docker-compose.yml`](./docker-compose.yml) file
    ```
    $ docker-compose up --build -d
    ```
  * check web app in browser: http://localhost:80
  * check running services: `$ docker-compose ps`
  * stop and kill services: `$ docker-compose down`

## Commonly used commands

### docker-compose

* `docker-compose build`: to build the images
* `docker-compose up -d`: to get the containers running (-d to keep it running in the backgroud)
* `docker-compose up --build -d`: a combined command to build the images and get the containers running
* `docker-compose ps`: to list running processes
* `docker-compose down`: to kill the processes

* `docker ps -a`: to list containers. `-a` shows all containers (without -a, will show only running contains)
