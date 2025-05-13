from typing import List
from common.utils.csv_processor import CSVProcessor
from common.delivery.models import Recipient, Package, Delivery
from common.delivery.constants.packages import PACKAGES
from common.constants import CLIENTS_WITH_OWN_LAPTOPS
from services.onboarding.utils.pairing import create_pairs, categorize_pairs
from services.onboarding.models import NewHire


def build_recipients_from_new_hire(nh: NewHire) -> Recipient:
    return Recipient(
        nit=1, div=1, name=nh.name, address=nh.address, phone=nh.phone, city=nh.city
    )


def get_packages_type_from_new_hire(nh: NewHire) -> Package:
    if nh.client in CLIENTS_WITH_OWN_LAPTOPS:
        return PACKAGES["DOUBLE_DELIVERY_LAPTOP"]
    return PACKAGES["STANDARD_DELIVERY_LAPTOP"]


def build_deliveries(new_hires: List[NewHire]) -> List[Delivery]:
    return [
        Delivery(
            recipient=build_recipients_from_new_hire(nh),
            package=get_packages_type_from_new_hire(nh),
        )
        for nh in new_hires
    ]


def process_onboarding(file):
    rows = CSVProcessor(file).read_and_clean()
    pairs = create_pairs(rows)
    buddy_program, onsite_lunch, raw_delivery_info = categorize_pairs(pairs)
    delivery_info = build_deliveries(raw_delivery_info) if raw_delivery_info else []
    return buddy_program, onsite_lunch, delivery_info
