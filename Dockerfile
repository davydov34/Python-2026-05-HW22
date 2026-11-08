FROM python:3.14-bookworm

ENV JWT_SECRET_KEY=sEcReT_kEy
ENV JWT_ALG=HS256
ENV JWT_EXP_TIME=30

WORKDIR /fastapi_app

COPY requirements.txt .

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8100

RUN pip uninstall jwt

CMD [ "python3", "main.py"]

