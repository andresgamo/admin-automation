from typing import List
from common.delivery.models import Sender, Delivery
from common.delivery.constants.sender import DEFAULT as DEFAULT_SENDER
from common.delivery.constants.couriers import AVAILABLE_COURIERS


def process_delivery(
    delivery_data: List[Delivery],
    sender: Sender | None = None,
    courier: str | None = None,
) -> List:
    # errors = [] generate_guide_number must return errors dont blow up the code for just one.
    sender = sender or DEFAULT_SENDER
    courier_client = AVAILABLE_COURIERS.get(courier or "coordinadora")

    if courier_client is None:
        raise ValueError(f"Unsupported courier from input: '{courier}'")

    guides = []

    for delivery in delivery_data:
        guide_number = courier_client.generate_guide_number(
            sender=sender,
            package=delivery.package,
            recipient=delivery.recipient,
        )
        b64str = courier_client.generate_guide_file(guide_number)
        b64bytes  = b64str.encode()
        name = delivery.recipient.name.strip().replace(" ", "_")
        filename = f"{name}_guide_{guide_number}.pdf"
        guides.append((filename, b64bytes))

    return guides
