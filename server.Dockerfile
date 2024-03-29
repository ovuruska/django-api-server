FROM python:3.8
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
ENV PORT=80
ENV DJANGO_DEBUG=False

RUN python3 manage.py collectstatic --noinput
#RUN python3 manage.py celery -A scrubbers_backend worker -l info
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:80", "--settings=scrubbers_backend.settings" ]