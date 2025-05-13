import os
import json

from services.onboarding.utils.data_validation import validate_data
from services.onboarding.process import process_onboarding
from services.onboarding.notification import send_nh_delivery_email
from services.onboarding.notification import send_buddy_program_email
from common.utils.multipart_parser import parse_multipart
from common.utils.data_validation import handle_errors
from common.notification.slack import reply_to_slack
from common.notification.jira_ticket import send_buddy_program_issue
from common.notification.jira_ticket import send_onsite_lunch_issue
from common.delivery.manager import process_delivery

OB_CHANNEL = os.getenv("SLACK_OB_CHANNEL_ID")


@handle_errors
def lambda_handler(event, context):
    body_parts_dict = parse_multipart(event)
    date_str, file_stream = validate_data(body_parts_dict)
    bp_people, ol_pople, delivery_data = process_onboarding(file_stream)
    if bp_people:
        if send_buddy_program_issue(bp_people, date_str):
            reply_to_slack(
                OB_CHANNEL, ":white_check_mark:Created buddy program ticket."
            )
        else:
            reply_to_slack(OB_CHANNEL, "Could not created buddy program ticket.")
        send_buddy_program_email(bp_people, date_str)
        reply_to_slack(
            OB_CHANNEL, ":white_check_mark:Email for buddy program sent to vendor"
        )
    if ol_pople:
        if send_onsite_lunch_issue(ol_pople, date_str):
            reply_to_slack(OB_CHANNEL, ":white_check_mark:Created onsite lunch ticket.")
        else:
            reply_to_slack(OB_CHANNEL, "Could not created onsite lunch ticket.")
    if delivery_data:
        guides = process_delivery(delivery_data)
        send_nh_delivery_email(guides, date_str)
        reply_to_slack(OB_CHANNEL, ":white_check_mark:Email guides sent to Laura")
    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "message": "We are live",
            }
        ),
    }
