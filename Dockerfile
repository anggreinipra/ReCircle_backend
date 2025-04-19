FROM python:3.11-slim-bullseye

WORKDIR /app

COPY requirements.txt . 

COPY . /app

RUN apt-get update && apt-get upgrade -y && apt-get clean && apt-get autoremove -y

RUN pip install --no-cache-dir -r requirements.txt

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["/docker-entrypoint.sh"]

EXPOSE 5000

CMD ["flask", "run", "--host=0.0.0.0"]
