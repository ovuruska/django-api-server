FROM python:3.9
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate
ENV PORT=80
ENV DJANGO_DEBUG=False

RUN python3 manage.py collectstatic --noinput
CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000", "--settings=scrubbers_backend.settings" ]
