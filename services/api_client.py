import os
from dotenv import load_dotenv
import requests

load_dotenv()
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

def get(endpoint, **kwargs):
    url = f"{API_BASE_URL}{endpoint}"
    resp = requests.get(url, **kwargs)
    resp.raise_for_status()
    return resp.json()

def post(endpoint, json=None, **kwargs):
    url = f"{API_BASE_URL}{endpoint}"
    resp = requests.post(url, json=json, **kwargs)
    resp.raise_for_status()
    return resp.json()

def put(endpoint, json=None, **kwargs):
    url = f"{API_BASE_URL}{endpoint}"
    resp = requests.put(url, json=json, **kwargs)
    resp.raise_for_status()
    return resp.json()

def patch(endpoint, json=None, **kwargs):
    url = f"{API_BASE_URL}{endpoint}"
    resp = requests.patch(url, json=json, **kwargs)
    resp.raise_for_status()
    return resp.json()

def delete(endpoint, **kwargs):
    url = f"{API_BASE_URL}{endpoint}"
    resp = requests.delete(url, **kwargs)
    resp.raise_for_status()
    return resp.json() 