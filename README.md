1. `$ git clone https://github.com/svfat/flask-celery-example`
2. `$ cd flask-celery-example/`
3. `$ docker-compose up`
4. Open http://127.0.0.1:3000 in the browser
5. Click the button to create a task (Repeat to create another one)
6. `$ docker-compose scale worker=5` to add 5 workers
7. Open http://127.0.0.1:5555 in the browser to monitor stuff