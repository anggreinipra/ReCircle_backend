FROM python:3.11-slim-bullseye

WORKDIR /app

# Copy semua file dari host ke dalam container
COPY . /app

# Update, upgrade, dan bersihkan apt cache
RUN apt-get update && apt-get upgrade -y && apt-get clean && apt-get autoremove -y

# Salin requirements.txt dan install dependencies
COPY requirements.txt . 
RUN pip install --no-cache-dir -r requirements.txt

# Salin script entrypoint untuk menjalankan perintah saat container mulai
COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

# Tentukan entrypoint script
ENTRYPOINT ["/docker-entrypoint.sh"]

# Ekspos port yang digunakan oleh Flask
EXPOSE 5000

# CMD for fallback (debugging)
CMD ["flask", "run", "--host=0.0.0.0"]
