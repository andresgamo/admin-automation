from common.delivery.models import Package

PACKAGES = {
    "STANDARD_DELIVERY_LAPTOP": Package(
        value=10000000,
        content_description="Computador - MacBook Pro 16''.",
        reference_description="",
        comments="Tener cuidado equipo delicado.",
        height=10.0,
        width=15.0,
        length=20.0,
        weight=1.2,
        items_count=1,
    ),
    "DOUBLE_DELIVERY_LAPTOP": Package(
        value=20000000,
        content_description="Computadores - MacBook Pro 16''.",
        reference_description="",
        comments="Tener cuidado equipo delicado.",
        height=10.0,
        width=15.0,
        length=20.0,
        weight=1.2,
        items_count=1,
    ),
}
