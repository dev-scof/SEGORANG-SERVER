FROM python:3.10

ENV FLASK_APP=manage:application
ENV FLASK_CONFIG=development
ENV FLASK_ENV=development

COPY ./ /home/SEGORANG-SERVER/
WORKDIR /home/SEGORANG-SERVER/

RUN pip install --upgrade pip && \
	pip install -r requirements.txt

EXPOSE 50505

CMD ["gunicorn","-w","2", \
	"--bind","0.0.0.0:50505", \
	"--log-level", "debug", \
	"--access-logfile", "-", \
	"--access-logformat", "%(h)s [ACCESS] %(l)s %(u)s %(t)s '%(r)s' %(s)s %(b)s '%(f)s' '%(a)s'", \
	"manage:application"]