FROM python:3.9
WORKDIR /app

COPY ./requirements.txt ./
RUN pip install -r requirements.txt

COPY ./ ./

RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

RUN python3 manage.py collectstatic --noinput
CMD ["python3", "manage.py", "runserver", "8000"]