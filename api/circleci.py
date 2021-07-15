import config
import requests
from app import app

CIRCLECI_API = f"https://circleci.com/api/v1.1/project/github/{config.CIRCLECI_ORG}/{config.CIRCLECI_PROJECT}"
api_token = app.config["CIRCLECI_API_KEY"]


def get_job_details(job_id):
    return get(f"{CIRCLECI_API}/{job_id}")


def get(uri):
    header = {"Circle-Token": api_token}
    response = requests.get(uri, headers=header)
    return response.json()
