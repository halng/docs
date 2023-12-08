"""
This is script use for initialize project.
This require 2 request header key-value api-token-value but it will be hash by default value and secret.
"""
import os
import requests 

HEADER = {
    "Content-Type": "application/json",
    "X-REQUEST-API-TOKEN": os.getenv("API_KEY_NAME", ""),
}

