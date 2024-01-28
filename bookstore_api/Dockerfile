# Dockerfile
FROM python:3.9

# copy project
COPY . /project/

# set work directory
WORKDIR /project

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# create and activate virtual environment
ENV VIRTUAL_ENV=/opt/venv
RUN python3 -m venv $VIRTUAL_ENV

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# install dependencies
RUN pip install pip --upgrade && \ 
    pip install --no-cache-dir -r requirements.txt && \
    chmod +x entrypoint.sh
CMD ["/project/entrypoint.sh"]
