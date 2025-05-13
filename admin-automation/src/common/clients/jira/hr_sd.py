"""HR service desk configuration."""

import logging
from typing import List, Dict, Any
from common.clients.jira.config import JiraClient
from common.utils.strings import parse_names

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OnboardingWelcoming:
    """
    Builds and submits Jira issues for onboarding activities like lunch and buddy programs.
    """

    SERVICE_DESK_ID: str = "5"
    REQUEST_TYPE_ID: str = "245"
    BUDDY_PROGRAM_COST: int = 40
    LUNCH_COST_USD: int = 10
    BASE_ISSUE_FIELDS: Dict[str, Any] = {
        "customfield_10587": {"value": "Facilities"},
        "customfield_10593": [{"value": "Facilities Logistics"}],
        "customfield_10321": [{"accountId": "62fe63a12e3849d13777e63b"}],
    }

    def __init__(self, jira_client: JiraClient):
        self.jira_client = jira_client

    @staticmethod
    def _format_description(title: str, names: List[str]) -> str:
        """
        Turn a list of names into a bullet-list description string.
        """
        return f"{title}:\n\n- {parse_names(names)}\n\nRegards."

    def _build_fields(
        self,
        people: List[Any],
        date: str,
        description_title: str,
        category: str,
        activity_type: str,
        cost_per_person: int,
    ) -> Dict[str, Any]:
        """
        Build the Jira ticket fields based on onboarding parameters.
        """
        names = [p.name for p in people]
        count = len(people)
        return {
            **self.BASE_ISSUE_FIELDS,
            "description": self._format_description(description_title, names),
            "customfield_10588": {"value": category},
            "customfield_10589": {"value": activity_type},
            "customfield_10365": date,
            "customfield_10367": cost_per_person * count,
            "customfield_10591": {"value": str(count)},
        }

    def onsite_lunch_builder(
        self, onsite_lunch: List[Any], date: str
    ) -> Dict[str, Any]:
        """
        Build an onsite lunch ticket fields.
        """
        return self._build_fields(
            people=onsite_lunch,
            date=date,
            description_title="People joining the lunch",
            category="Buddy Program Lunch",
            activity_type="Onsite",
            cost_per_person=self.LUNCH_COST_USD,
        )

    def buddy_program_builder(
        self, buddy_program: List[Any], date: str
    ) -> Dict[str, Any]:
        """
        Build a buddy program ticket fields.
        """
        return self._build_fields(
            people=buddy_program,
            date=date,
            description_title="People receiving boxes:",
            category="Buddy Program Box",
            activity_type="Remote",
            cost_per_person=self.BUDDY_PROGRAM_COST,
        )

    def submit_issue(self, fields: Dict[str, Any]) -> Dict[str, Any]:
        """
        Submit ticket with its corresponding fields.
        """
        payload = {
            "serviceDeskId": self.SERVICE_DESK_ID,
            "requestTypeId": self.REQUEST_TYPE_ID,
            "requestFieldValues": fields,
        }
        return self.jira_client.create_ticket(payload)
