# start by pulling the python image
	# checkov:skip=CKV_DOCKER_2: ADD REASON
	# checkov:skip=CKV_DOCKER_3: ADD REASON
FROM python:3.8-alpine

# copy the requirements file into the image
COPY ./requirements.txt /app/requirements.txt

# switch working directory
WORKDIR /app

# install the dependencies and packages in the requirements file
RUN apt-get update
RUN apt-get install -y gcc
RUN apt-get install -y libxml2-dev libxslt1-dev zlib1g-dev g++
RUN apt-get update
RUN apt-get install -y tdsodbc unixodbc-dev
RUN apt install unixodbc-bin -y
RUN apt-get clean -y
RUN pip install -r requirements.txt

# copy every content from the local file to the image
COPY . /app

# configure the container to run in an executed manner
ENTRYPOINT [ "python" ]

CMD [ "app.py" ]