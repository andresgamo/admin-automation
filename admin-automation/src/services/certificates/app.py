import os
import json
import boto3
from services.certificates.utils import get_employee_dataset_by_email
from services.certificates.utils import map_bamboo_dataset
from common.notification.emailer import send_email
from common.notification.slack import reply_to_slack
from common.notification.slack import upload_file


OB_CHANNEL = os.getenv("SLACK_OB_CHANNEL_ID")
JSREPORT_FN = os.environ["JSREPORT_FUNCTION_NAME"]
lambda_client = boto3.client("lambda")


def lambda_handler(event, context):
    email = "miguel.sierra@gorillalogic.com"
    data_set = get_employee_dataset_by_email(email)
    clean_data = map_bamboo_dataset(data_set)
    report_payload = {
        "renderRequest": {
            "template": {"name": "/samples/certificates/labour_none_salary"},
            "data": clean_data,
        }
    }
    response = lambda_client.invoke(
        FunctionName=JSREPORT_FN,
        InvocationType="RequestResponse",
        Payload=json.dumps(report_payload).encode(),
    )
    payload_str = response["Payload"].read().decode("utf-8")
    payload_obj = json.loads(payload_str)
    pdf_bytes = payload_obj["body"].encode()
    reply_to_slack(OB_CHANNEL, "Yes Sr. We are live")
    upload_file(OB_CHANNEL, pdf_bytes, f"{clean_data["document_id"]}_certificate.pdf")
    send_email(
        subject="Tu Certificado Laboral",
        attachments=(f"{clean_data["document_id"]}_certificate.pdf", pdf_bytes),
        to="ana.molina@gorillalogic.com",
        body="Adjunto encontrarás tu certificado.",
        cc_addr="andres.garcia.molina@gorillalogic.com",
    )

    return {"statusCode": 200, "body": "Correo enviado correctamente"}
