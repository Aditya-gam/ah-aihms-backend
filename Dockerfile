FROM python:3.11-slim

WORKDIR /app

# Copy Pipenv files first for efficient layer caching
COPY Pipfile* ./
RUN pip install --no-cache-dir pipenv && pipenv install --system --deploy

# Copy the rest of the code
COPY . .

# Default command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
