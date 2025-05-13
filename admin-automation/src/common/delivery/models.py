from dataclasses import dataclass


@dataclass
class Package:
    """
    Represents the dimensions and metadata for
    a single standard package shape.
    """

    value: int
    content_description: str
    reference_description: str
    comments: str
    height: float
    width: float
    length: float
    weight: float
    items_count: int


@dataclass
class Sender:
    """
    Represents the Sender info required.
    If nit is given, id must be 0
    """

    id: int
    nit: int
    name: str
    address: str
    phone: int
    city: str


@dataclass
class Recipient:
    """
    Represents the dimensions and metadata for
    a single standard package shape.
    """

    nit: str
    div: str
    name: str
    address: str
    phone: float
    city: float


@dataclass
class Delivery:
    """
    Represents a delivery unit composed of a recipient and the package assigned to them.
    """

    recipient: Recipient
    package: Package
