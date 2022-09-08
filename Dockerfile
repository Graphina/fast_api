FROM python:3.10

WORKDIR /code

ARG SERVICE

RUN apt install libffi-dev libssl-dev

COPY ./services/${SERVICE}/requirements.txt /code/requirements.txt
RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY ./services/${SERVICE}/app /code/app
COPY ./services/log_config.yaml /code/log_config.yaml

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80", "--log-config", "log_config.yaml"]