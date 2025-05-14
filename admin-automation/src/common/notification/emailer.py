import os
import smtplib
import base64
from typing import Optional, Union, List, Tuple
from email.message import EmailMessage


Attachment = Tuple[str, bytes]
AttachmentsArg = Optional[Union[Attachment, List[Attachment]]]


PRIMARY_GMAIL_ADDRESS = os.getenv("PRIMARY_GMAIL_SENDER_ADDRESS")
SECONDARY_GMAIL_ADDRESS = os.getenv("SECONDARY_GMAIL_SENDER_ADDRESS")
GMAIL_APP_PASSWORD = os.getenv("GMAIL_APP_PASSWORD")

if not (PRIMARY_GMAIL_ADDRESS and GMAIL_APP_PASSWORD):
    raise RuntimeError(
        "PRIMARY_GMAIL_ADDRESS and GMAIL_APP_PASSWORD must be set in the environment"
    )


def is_single_attachment(obj: object) -> bool:
    return (
        isinstance(obj, tuple)
        and len(obj) == 2
        and isinstance(obj[0], str)
        and isinstance(obj[1], (bytes, bytearray))
    )


def normalize_attachments(attachments: AttachmentsArg) -> List[Attachment]:
    """
    Accepts:
        - None
        - A single (filename, base64-bytes) tuple
        - A list of such tuples
    Returns a flat list of (filename, base64-bytes) tuples.
    """
    if attachments is None:
        return []

    if is_single_attachment(attachments):
        return [attachments]

    if isinstance(attachments, list) and all(
        is_single_attachment(attachment) for attachment in attachments
    ):
        return attachments

    raise ValueError(
        "attachments must a (filename, base64-bytes) tuple, or a list of such tuples"
    )


def send_email(
    subject: str,
    to: str,
    body: str,
    from_addr: Optional[str] = None,
    cc_addr: Optional[str] = None,
    attachments: AttachmentsArg = None,
) -> None:
    """
    Sends a plain-text email via Gmail SMTP.

    attachments: None, a single (filename, base64-bytes) tuple,
    or a list of such tuples.
    """

    sender = from_addr or PRIMARY_GMAIL_ADDRESS
    cc = cc_addr or SECONDARY_GMAIL_ADDRESS

    msg = EmailMessage()
    msg["Subject"] = subject
    msg["From"] = sender
    msg["To"] = to
    if cc:
        msg["Cc"] = cc
    msg.set_content(body)

    for filename, b64data in normalize_attachments(attachments):
        pdf_bytes = base64.b64decode(b64data)
        msg.add_attachment(
            pdf_bytes, maintype="application", subtype="pdf", filename=filename
        )

    with smtplib.SMTP_SSL("smtp.gmail.com", 465) as smtp:
        smtp.login(sender, GMAIL_APP_PASSWORD)
        smtp.send_message(msg)
