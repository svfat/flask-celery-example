import os
from flask import Flask, request, render_template, session, flash, redirect, \
    url_for, jsonify

from celery import Celery
from celery.result import AsyncResult
import celery.states as states

template_folder = os.path.abspath('templates')
app = Flask(__name__, template_folder=template_folder)

app.config['SECRET_KEY'] = 'SECRET_KEY'
app.config['DEBUG'] = True

# Celery configuration
redis_url = os.getenv('REDIS_URL')
app.config['CELERY_BROKER_URL'] = redis_url
app.config['CELERY_RESULT_BACKEND'] = redis_url

# Initialize Celery
celery = Celery(app.name, broker=app.config['CELERY_BROKER_URL'])
celery.conf.update(app.config)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'GET':
        return render_template('index.html')
    return redirect(url_for('index'))


@app.route('/longtask', methods=['POST'])
def longtask():
    task = celery.send_task('mytasks.long_task')
    return jsonify({}), 202, {'Location': url_for('taskstatus',
                                                  task_id=task.id)}


@app.route('/status/<task_id>')
def taskstatus(task_id):
    res = AsyncResult(task_id)
    print(res.state, states.PENDING)
    if res.state == states.PENDING:
        response = {
            'state': res.state,
            'current': 0,
            'total': 1,
            'status': 'Pending...'
        }
    elif res.state != states.FAILURE:
        response = {
            'state': res.state ,
            'current': res.info.get('current', 0),
            'total': res.info.get('total', 1),
            'status': res.info.get('status', '')
        }
        if 'result' in res.info:
            response['result'] = res.info['result']
    else:
        # something went wrong in the background job
        response = {
            'state': res.state,
            'current': 1,
            'total': 1,
            'status': str(res.info),  # this is the exception raised
        }
    return jsonify(response)
