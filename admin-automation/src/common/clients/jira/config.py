"""Jira basic configuration."""

import os
import logging
from urllib.parse import urljoin
from jira import JIRA

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class JiraClient:
    def __init__(self, server=None, user=None, api_token=None):
        self.server = server or os.getenv("JIRA_SERVER")
        self.user = user or os.getenv("JIRA_USER")
        self.token = api_token or os.getenv("JIRA_API_TOKEN")

        if not all([self.server, self.user, self.token]):
            raise ValueError("JIRA_SERVER, JIRA_USER and JIRA_API_TOKEN must be set")

        self.client = JIRA(server=self.server, basic_auth=(self.user, self.token))

    def create_ticket(self, payload):
        # headers = {
        #     "Content-Type": "application/json",
        # }
        endpoint = urljoin(self.server, "/rest/servicedeskapi/request")
        try:
            print(endpoint, payload)
            # response = self.client._session.post(
            #     endpoint, json=payload, headers=headers
            # )
            # response.raise_for_status()
            # return response.json()
        except Exception as e:
            logger.error("Failed to create issue: %s", e)
            raise
