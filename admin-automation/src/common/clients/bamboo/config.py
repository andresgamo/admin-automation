import os
from typing import Any, Dict, Optional, List
from urllib.parse import urljoin

import requests
from requests.auth import HTTPBasicAuth
from tenacity import retry, stop_after_attempt, wait_fixed

# env-config (as before)
BAMBOOHR_SUBDOMAIN = os.getenv("BAMBOOHR_SUBDOMAIN")
BAMBOOHR_API_KEY = os.getenv("BAMBOOHR_API_KEY")
if not (BAMBOOHR_SUBDOMAIN and BAMBOOHR_API_KEY):
    raise RuntimeError("BAMBOOHR_SUBDOMAIN and BAMBOOHR_API_KEY must be set")


class BambooHRClient:
    def __init__(self, subdomain: Optional[str] = None, api_key: Optional[str] = None):
        self.subdomain = subdomain or BAMBOOHR_SUBDOMAIN
        self.auth = HTTPBasicAuth(api_key or BAMBOOHR_API_KEY, "x")
        self.headers = {"Accept": "application/json"}
        self.base_url = f"https://api.bamboohr.com/api/gateway.php/{self.subdomain}/v1/"

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def _get(
        self, path: str, params: Optional[Dict[str, Any]] = None
    ) -> Dict[str, Any]:
        url = urljoin(self.base_url, path)
        resp = requests.get(
            url, headers=self.headers, auth=self.auth, params=params, timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def _post(self, path: str, json: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        url = urljoin(self.base_url, path)
        resp = requests.post(
            url, headers=self.headers, auth=self.auth, json=json, timeout=30
        )
        resp.raise_for_status()
        return resp.json()

    def query_dataset(
        self, filters: Dict[str, Any], fields: List[str]
    ) -> Dict[str, Any]:
        """
        Query the employee dataset endpoint.
        """
        payload = {"filters": filters, "fields": fields}
        return self._post("datasets/employee", json=payload)

    def get_employee(self, employee_id: int, fields: List[str]) -> Dict[str, Any]:
        """
        Retrieve specified fields for a single employee.
        """
        params = {"fields": ",".join(fields)}
        return self._get(f"employees/{employee_id}", params=params)
