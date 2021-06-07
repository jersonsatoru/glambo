FROM python:3.9.5-alpine3.13

WORKDIR /usr/app

RUN apk add --no-cache gcc python3-dev linux-headers libc-dev musl-dev

RUN pip install pipenv

COPY Pipfile.lock ./

RUN pipenv shell

RUN pipenv sync

COPY . .

CMD ["python", "./src/main.py"]
