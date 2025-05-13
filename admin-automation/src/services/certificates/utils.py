from datetime import date
from typing import Tuple, Dict, Any
from common.clients.bamboo.config import BambooHRClient
from common.utils.strings import format_spanish_date


client = BambooHRClient()

def get_employee_dataset_by_email(email: str) -> Dict[str, Any]:
    filters = {
        "match": "all",
        "filters": [
            {
                "field": "email",
                "operator": "equal",
                "value": f"{email}",
            }
        ],
    }
    fields = [
        "name",
        "compensationPayRate",
        "hireDate",
        "customField4584",
        "jobInformationJobTitle",
    ]
    return client.query_dataset(filters, fields).get("data", {})[0]


def map_bamboo_dataset(data: Dict):
    return {
        "name": data.get("name"),
        "document_id": data.get("customField4584"),
        "hire_date": format_spanish_date(data.get("hireDate")),
        "job_title": data.get("jobInformationJobTitle"),
        "current_date": format_spanish_date(date.today().isoformat()),
    }
