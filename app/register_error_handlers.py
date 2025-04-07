# File: app/register_error_handlers.py
import logging

from flask import jsonify

logger = logging.getLogger(__name__)


def register_error_handlers(app):
    @app.errorhandler(404)
    def not_found_error(error):
        logger.warning("404 Not Found: %s", error)
        return (
            jsonify({"error": "Not Found", "message": "The requested resource was not found."}),
            404,
        )

    @app.errorhandler(405)
    def method_not_allowed_error(error):
        logger.warning("405 Method Not Allowed: %s", error)
        return (
            jsonify(
                {
                    "error": "Method Not Allowed",
                    "message": "The method is not allowed for this endpoint.",
                }
            ),
            405,
        )

    @app.errorhandler(500)
    def internal_error(error):
        logger.error("500 Internal Server Error: %s", error, exc_info=True)
        return (
            jsonify({"error": "Internal Server Error", "message": "An unexpected error occurred."}),
            500,
        )

    @app.errorhandler(Exception)
    def unhandled_exception(error):
        logger.error("Unhandled Exception: %s", error, exc_info=True)
        return jsonify({"error": "Server Error", "message": "An unexpected error occurred."}), 500
