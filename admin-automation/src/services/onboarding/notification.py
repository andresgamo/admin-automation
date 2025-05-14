import os
from typing import NewType, Sequence, Tuple, List, Any
from services.onboarding.utils.pairing import unpairing_buddy_program
from common.utils.strings import capitalize_phrase
from common.notification.emailer import send_email

Base64Str = NewType("Base64Str", str)

BUDDY_PROGRAM_VENDOR_ADDRESSES = os.getenv("BUDDY_PROGRAM_VENDOR_ADDRESSES")
SECONDARY_GMAIL_ADDRESS = os.getenv("SECONDARY_GMAIL_SENDER_ADDRESS")


def _generate_buddy_email_body(buddy_program, date) -> str:
    """
    Generates formatted email text that separates the buddy program
    information into "Ingresos" (New Hires) and "Buddies".
    """
    new_hires, buddies = unpairing_buddy_program(buddy_program)

    email_content = [
        "Buen día Paulina y Diana! Esperamos se encuentren bien.\n",
        f"Relacionamos a continuación la información del ingreso que tendremos para el próximo {date}, así como su correspondiente buddy.\n",
    ]
    email_content.append("Ingresos:")
    for nh in new_hires:
        email_content.append(
            f"Nombre: {capitalize_phrase(nh.name)}\n"
            f"Dirección: {capitalize_phrase(nh.address)}\n"
            f"Celular: {nh.phone}\n"
        )
    email_content.append("_" * 90 + "\n")
    email_content.append("Buddies:")
    for bd in buddies:
        email_content.append(
            f"Nombre: {capitalize_phrase(bd.name)}\n"
            f"Dirección: {capitalize_phrase(bd.address)}\n"
            f"Celular: {bd.phone}\n"
        )
    email_content.append(
        "Muchas gracias por su ayuda, quedamos atentos a cualquier inquietud."
    )

    return "\n".join(email_content)


def _generate_nh_delivery_email_body(date) -> str:
    return (
        "¡Hola!\n\n"
        f"Adjunto se encuentran las guías para envío de equipos de los ingresos del próximo {date}.\n\n"
        "Cordialmente,"
    )


def send_buddy_program_email(buddy_program: List[Any], date) -> None:
    """Send boddy program email to vendor."""
    send_email(
        subject=f"Buddy program (Nuevos ingresos) - Gorilla Logic {date}",
        to=BUDDY_PROGRAM_VENDOR_ADDRESSES,
        body=_generate_buddy_email_body(buddy_program, date),
    )


def send_nh_delivery_email(
    attachments: List[Tuple[str, Base64Str]],
    date: str = None,
) -> None:
    """"""
    send_email(
        subject=f"Guía coordinadora (Nuevos ingresos) - {date}",
        to=SECONDARY_GMAIL_ADDRESS,
        body=_generate_nh_delivery_email_body(date),
        attachments=attachments,
    )
