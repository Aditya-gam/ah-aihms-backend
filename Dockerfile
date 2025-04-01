FROM python:3.11-slim

WORKDIR /app

# System dependencies
RUN apt-get update && apt-get install -y git

# Copy and install requirements
COPY requirements.txt ./
RUN pip install --upgrade pip && pip install -r requirements.txt

# Copy the app
COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
