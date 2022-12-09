FROM python:3.9

RUN mkdir -p /code

WORKDIR /code/

# set env variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./app /code/app
# CD /code/app
EXPOSE 8000
ENV PYTHONPATH=$PWD/code/app

CMD ["uvicorn", "app.main:app", "--host=0.0.0.0", "--reload", "--port", "8000"]
