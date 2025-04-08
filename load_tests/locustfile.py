# File: locustfile.py
"""
Locust Load Test for the Auth Endpoints

This file defines load test scenarios for the authentication endpoints of your Flask application.
It simulates user behavior by registering new users concurrently.

Key features:
- Inherits from HttpUser to simulate HTTP requests.
- The host is configurable (default: http://localhost:5000).
- Uses the `@task` decorator to mark the registration flow as a task.
- The registration payload is dynamically modified to avoid duplicate user email issues.

To run this load test, install locust (pip install locust) and run:
    locust -f locustfile.py
"""

import random
import string

from locust import HttpUser, between, task


def random_email():
    """Generate a random email address for testing."""
    username = "".join(random.choices(string.ascii_lowercase + string.digits, k=8))
    domain = "example.com"
    return f"{username}@{domain}"


def random_string(length=10):
    """Generate a random string of given length."""
    return "".join(random.choices(string.ascii_letters, k=length))


class AuthLoadTest(HttpUser):
    # The host URL of the Flask application under test; adjust as needed.
    host = "http://localhost:5000"
    # Wait time between tasks to simulate real user behavior.
    wait_time = between(1, 3)

    @task
    def register_user(self):
        """Simulate a user registration flow by POSTing to /api/auth/register/patient."""
        payload = {
            "email": random_email(),  # Dynamic email to avoid duplicates.
            "password": "LoadTestPassword!",
            "first_name": random_string(6),
            "last_name": random_string(8),
            "phone_number": "0001112222",
            "address": "Load Test Ave",
            "emergency_contact": {
                "name": "Test Contact",
                "relationship": "Friend",
                "phone_number": "3334445555",
            },
        }
        # POST request to the registration endpoint.
        response = self.client.post("/api/auth/register/patient", json=payload)
        # Optional: Log the result for debugging.
        if response.status_code != 201:
            print(f"Registration failed: {response.status_code}, {response.text}")
