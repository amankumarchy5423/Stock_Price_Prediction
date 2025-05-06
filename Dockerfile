FROM python:3.12-slim

WORKDIR /app

COPY . /app/

ENV DAGSHUB_TOKEN=06ff030bf203ef6af72ea419852b98883469730a

RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 5050

CMD ["python", "main.py"]
