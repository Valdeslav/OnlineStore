FROM python:3.7

# set a directory for the app
WORKDIR /usr/src/app

COPY pyproject.toml poetry.lock ./

RUN pip install --no-cache-dir --upgrade pip \
 && pip install --no-cache-dir poetry \
 \
 && poetry install --no-dev


#copy all the files to the container

COPY . ./

EXPOSE 5000

CMD ["poetry", "run", "python", "./app.py"]


