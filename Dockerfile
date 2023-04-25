# Use the AWS Lambda Python runtime as the base image
FROM public.ecr.aws/lambda/python:3.8
WORKDIR ${LAMBDA_TASK_ROOT}

# Install GCC
RUN yum install -y gcc postgresql-devel
# Copy the requirements.txt file and install dependencies
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

ARG DB_HOST
ARG DB_USER
ARG DB_PASSWORD
ARG DB_NAME
ARG DB_PORT


ENV DB_HOST=${DB_HOST:-""}
ENV DB_USER=${DB_USER:-""}
ENV DB_PASSWORD=${DB_PASSWORD:-""}
ENV DB_NAME=${DB_NAME:-""}
ENV DB_PORT=${DB_PORT:-""}

# Copy the Django app
COPY ./ ${LAMBDA_TASK_ROOT}

RUN python manage.py collectstatic --noinput
RUN python manage.py migrate

# Set the handler to your Django lambda_handler
CMD ["app.handler"]
