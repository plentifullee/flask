
from flask import Flask, request
from flasgger import Swagger


app = Flask(__name__)
swagger = Swagger(app)

@app.route("/", methods=["GET", "POST"])
def hello():
    """
    A simple GET and POST endpoint.
    ---
    get:
        description: Get a hello message
        responses:
            200:
                description: Returns a hello message
    post:
        description: Post some data
        requestBody:
            required: false
            content:
                application/json:
                    schema:
                        type: object
        responses:
            200:
                description: Returns a message and the posted data
    """
    if request.method == "POST":
        data = request.get_json(silent=True) or {}
        return {"message": "Received POST", "data": data}
    else:
        return {"message": "Hello, World! (GET)"}