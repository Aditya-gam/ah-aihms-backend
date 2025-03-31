FROM python:3.11-slim

WORKDIR /app

# Install dependencies using Pipenv
COPY Pipfile* ./
RUN pip install pipenv && pipenv install --system --deploy --ignore-pipfile

COPY . .

ENV FLASK_APP=run.py
ENV FLASK_ENV=production

EXPOSE 5000

CMD ["gunicorn", "-b", "0.0.0.0:5000", "run:app"]
