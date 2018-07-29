FROM frolvlad/alpine-python3

ENV HOME /app

RUN mkdir ${HOME}
WORKDIR ${HOME}

ADD requirements.txt ${HOME}

RUN pip install -r requirements.txt
RUN pip install gunicorn

ADD . ${HOME}

EXPOSE ${PORT}

CMD gunicorn wsgi:app -b 0.0.0.0:${PORT} -w2  --access-logfile -