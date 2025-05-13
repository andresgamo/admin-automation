from dataclasses import dataclass

@dataclass
class NewHire:
    """
    Represents a new onboarded employee at Gorilla Logic.
    """

    name: str
    newhire_id: str
    gl_email: str
    personal_email: str
    address: str
    phone: str
    size: str
    onboarding: str
    city: str
    client: str


@dataclass
class Buddy:
    """
    Represents the “buddy” assigned to guide a new hire through onboarding.
    """

    name: str
    address: str
    phone: str
    support: str
