FROM python:3.10

COPY notificacion-requirements.txt ./
RUN pip install --no-cache-dir -r hsm-requirements.txt

COPY . .

CMD [ "python", "./src/hsm/main.py" ]