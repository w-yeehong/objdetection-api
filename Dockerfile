FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

RUN curl -Lo /tmp/model.tar.gz \
    https://storage.googleapis.com/tfhub-modules/google/faster_rcnn/openimages_v4/inception_resnet_v2/1.tar.gz

RUN tar -xzvf /tmp/model.tar.gz --directory /tmp && \
    mkdir -p /code/models && \
    mv /tmp/saved_model.pb /code/models && \
    rm -rf /tmp/*

COPY ./app /code/app

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
