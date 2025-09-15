import requests
import json
import base64

from kubernetes import client, config
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

@app.route("/coins", methods=["GET"])
def get_coins():
    """
    Get cryptocurrency prices
    ---
    get:
        description: Get a list of cryptocurrencies and their prices
        responses:
            200:
                description: Returns cryptocurrency prices
                content:
                    application/json:
                        schema:
                            type: object
                            properties:
                                coins:
                                    type: object
                                    properties:
                                        BTC:
                                            type: number
                                            example: 45000.00
                                        ETH:
                                            type: number
                                            example: 3000.00
    """
    coins = {
        "coins": {
            "BTC": 45000.00,
            "ETH": 3000.00,
            "SOL": 100.00,
            "DOGE": 0.15
        }
    }
    return coins

@app.route("/ai", methods=["POST"])
def ai_faq():
    data = request.json or {}
    message = data.get("message", "")
    url = "https://api.dify.ai/v1/chat-messages"

    # get k8s secret
    secret_name = "dify-api"
    namespace = "default"
    
    secret_values = get_secret(secret_name, namespace)
    
    if secret_values:
        print(f"Values from secret '{secret_name}':")
        for key, value in secret_values.items():
            print(f"- {key}: {value}")
            dify_api_key = value
    else:
        print(f"Failed to retrieve secret '{secret_name}'.")

    payload = json.dumps({
        "inputs": {},
        "query": message,
        "response_mode": "blocking",
        "conversation_id": "",
        "user": "plenty"
    })
    headers = {
        'Authorization': 'Bearer '+dify_api_key,
        'Content-Type': 'application/json'
    }

    response = requests.request("POST", url, headers=headers, data=payload)

    print(response.text)
    answer = response.json().get("answer")
    return {"answer": answer}
    

def get_secret(secret_name, namespace="default"):
    """
    Reads a Kubernetes Secret, decodes its values, and returns them.
    """
    try:
        # Tries to load the config from inside a cluster
        config.load_incluster_config()
    except config.ConfigException:
        # Fallback to local kubeconfig file
        config.load_kube_config()

    v1 = client.CoreV1Api()
    
    try:
        secret = v1.read_namespaced_secret(name=secret_name, namespace=namespace)
        # Get the single key and its base64-encoded value
        secret_key, encoded_value = next(iter(secret.data.items()))
        
        # Decode the value and return
        decoded_value = base64.b64decode(encoded_value).decode('utf-8')
        
        return {secret_key: decoded_value}
    except client.ApiException as e:
        print(f"Error fetching secret: {e}")
        return None
