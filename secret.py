from google.cloud import secretmanager
import json
import os

def get_secret(secret_name):
    client = secretmanager.SecretManagerServiceClient()

    # Full resource name of the secret version
    name = f"projects/891722383681/secrets/{secret_name}/versions/latest"

    response = client.access_secret_version(request={"name": name})
    secret_data = response.payload.data.decode("UTF-8")

    # If it's JSON (like {"example": "123"}), parse it
    return json.loads(secret_data)
