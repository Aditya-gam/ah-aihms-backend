import logging

from dotenv import load_dotenv  # ✅ Add this

from app import create_app

load_dotenv()  # ✅ Load .env before create_app()


logger = logging.getLogger(__name__)

app = create_app()

if __name__ == "__main__":
    """
    Entry point for running the Flask development server locally.
    This block is typically bypassed in production if you use Gunicorn
    or another WSGI server (as defined in your Dockerfile).
    """
    # Example logging statements on startup
    logger.info("Starting Flask development server...")

    # Run the app
    # NOTE: 'debug=True' should typically be disabled in production environments
    # to avoid detailed stack traces and possible security issues.
    # If FLASK_ENV=production is set, debug will usually be off.
    app.run(host="0.0.0.0", port=5000, debug=True)
