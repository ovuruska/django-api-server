# Use the AWS Lambda Python runtime as the base image
FROM public.ecr.aws/lambda/python:3.8
WORKDIR ${LAMBDA_TASK_ROOT}

# Install GCC
RUN yum install -y gcc postgresql-devel
# Copy the requirements.txt file and install dependencies
COPY requirements.txt  .
RUN  pip3 install -r requirements.txt --target "${LAMBDA_TASK_ROOT}"

# Copy the Django app
COPY ./ ${LAMBDA_TASK_ROOT}

# Set the handler to your Django lambda_handler
CMD ["app.handler"]
