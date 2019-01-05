# silver-funicular

Trying out framework, tools, and others

## Project: flask-vue-crud

This is an exercise inspired by the blog post at [testdriven.io](https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/#vue-setup)

### Server

* `cd flask-vue-crud`
* `python3 -m venv env`
* `source env/bin/activate`
* `pip install -r requirments.txt`

- Run server: `python server/app.py`
  * runs on http://localhost:5000
  * try hit http://localhost:5000/ping

### Client

* `npm install -g vue-cli@2.9.3`
* `vue init webpack client`
* `cd client`

- Run client: `npm run dev`
  * runs on http://localhost:8080
