FROM python:3.10

EXPOSE 5100/tcp

COPY requirements.txt ./
RUN pip install --upgrade --no-cache-dir "pip<24.1" setuptools wheel
RUN pip install --no-cache-dir wheel
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD [ "flask", "--app", "./src/anonimizacion/api", "run", "--host=0.0.0.0", "--port", "5100"]