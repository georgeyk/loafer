FROM python:3.7-slim-buster

WORKDIR /loafer
COPY . /loafer

RUN pip install -e .

CMD ["python", "-m", "examples.echo"]
