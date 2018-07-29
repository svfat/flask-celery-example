FROM frolvlad/alpine-python3

ENV C_FORCE_ROOT true


# copy source code
COPY . /flask-celery
WORKDIR /flask-celery

# install requirements
RUN pip install -r requirements.txt


# run the worker
#ENTRYPOINT ['celery']
#CMD ['-A','tasks', 'worker','--loglevel=info']
CMD celery -A tasks worker --loglevel=info
