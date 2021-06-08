FROM python:3.9.5-alpine3.13

WORKDIR /usr/app

RUN apk add --no-cache gcc python3-dev linux-headers libc-dev musl-dev

ENV PIPENV_VENV_IN_PROEJCT=true

COPY Pipfile.lock ./

RUN pip install --no-cache-dir pipenv

RUN pip install -U pylint

RUN pip install -U mypy

RUN pip install -U autopep8

RUN pipenv sync --system

COPY . .

CMD ["python", "-u", "./src/main.py"]
