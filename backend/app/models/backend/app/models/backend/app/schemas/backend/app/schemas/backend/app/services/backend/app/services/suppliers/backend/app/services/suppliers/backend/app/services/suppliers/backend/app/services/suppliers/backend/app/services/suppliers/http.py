import requests

class SupplierHTTPClient:
    def __init__(self, base_url: str, api_key: str | None):
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key

    def get(self, path: str, params: dict | None = None) -> dict:
        headers = {"Accept": "application/json"}
        if self.api_key:
            headers["Authorization"] = f"Bearer {self.api_key}"
        response = requests.get(f"{self.base_url}/{path.lstrip('/')}", params=params, headers=headers, timeout=20)
        response.raise_for_status()
        return response.json()
