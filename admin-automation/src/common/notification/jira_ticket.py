from common.clients.jira.config import JiraClient
from common.clients.jira.hr_sd import OnboardingWelcoming

client = JiraClient()
ob_client = OnboardingWelcoming(client)


def _submit(builder_fn, items, date):
    fields = builder_fn(items, date)
    return ob_client.submit_issue(fields)


def send_buddy_program_issue(buddy_program, date):
    return _submit(ob_client.buddy_program_builder, buddy_program, date)


def send_onsite_lunch_issue(onsite_lunch, date):
    return _submit(ob_client.onsite_lunch_builder, onsite_lunch, date)
