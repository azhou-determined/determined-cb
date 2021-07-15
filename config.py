import os

DB_USER = os.environ.get("DB_USER")
DB_PASSWORD = os.environ.get("DB_PASSWORD")

DB_HOST = "determined-cb.cluster-csrkoc1nkoog.us-west-2.rds.amazonaws.com"
DB_PORT = "5432"
DB_NAME = "determined"

CIRCLECI_ORG = "determined-ai"
CIRCLECI_PROJECT = "determined"

CIRCLECI_API_KEY = os.environ.get("CIRCLECI_API_KEY")

APP_ACCESS_KEY = os.environ.get("DET_CI_ACCESS_KEY")