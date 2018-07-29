import os
import time
import random
import string
from celery import Celery


env = os.environ
redis_url = os.getenv('REDIS_URL')
CELERY_BROKER_URL = env.get('CELERY_BROKER_URL', redis_url),
CELERY_RESULT_BACKEND = env.get('CELERY_RESULT_BACKEND', redis_url)

CELERY_ACCEPT_CONTENT = ['pickle']

celery = Celery('tasks',
                broker=CELERY_BROKER_URL,
                backend=CELERY_RESULT_BACKEND)


@celery.task(bind=True, name='mytasks.long_task')
def long_task(self):
    """Background task that runs a long function with progress reports."""
    total = random.randint(10, 30)
    message = ''
    N = 20
    for i in range(total):
        if not message or random.random() < 0.25:
            message = ''.join(
                random.choices(string.ascii_uppercase + string.digits, k=N)
            )
            self.update_state(state='PROGRESS',
                              meta={'current': i, 'total': total,
                                    'status': message})
        time.sleep(0.5)
    return {'current': 100, 'total': 100, 'status': 'Task completed!',
            'result': message}
