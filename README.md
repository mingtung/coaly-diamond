# silver-funicular

Trying out framework, tools, and others

## Project: flask-vue-crud

This is an exercise about single page app using Flask and Vue.js inspired by the blog post at [testdriven.io](https://testdriven.io/blog/developing-a-single-page-app-with-flask-and-vuejs/#vue-setup).

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
* Using axios for AJAX requests to the back-end Flask app. Installing axios: `npm install axios@0.18.0 --save`
* Using Bootstrap CSS framework. Installing it: `npm install bootstrap@4.1.1 --save`
* Using Bootstrap Vue library. Installing it: `npm install bootstrap-vue@2.0.0-rc.11 --save`

- Run client: `npm run dev`
  * runs on http://localhost:8080

### [WIP] Tests
