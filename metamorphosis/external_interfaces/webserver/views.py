##
# File: external_interfaces\webserver\views.py.
#
# Summary:  Views class.

"""
Routes and views for the flask application.
"""

from datetime import datetime
from metamorphosis import app

@app.route("/")
@app.route("/home")
def home():
    """Renders the home page."""
    return datetime.now()

@app.route("/routes", methods = ["GET"])
def get_routes():
    routes = {}
    for r in app.url_map._rules:
        routes[r.rule] = {}
        routes[r.rule]["functionName"] = r.endpoint
        routes[r.rule]["methods"] = list(r.methods)

    #routes.pop("/static/ < path:filename > ")

    return jsonify(routes)

