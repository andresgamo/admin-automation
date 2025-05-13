import os
from common.clients.coordinadora.config import CoordinadoraClient

COORDINADORA_USER = os.getenv("COORDINADORA_USER")
COORDINADORA_PASSWORD = os.getenv("COORDINADORA_PASSWORD")
COORDINADORA_API = os.getenv("COORDINADORA_API")
COORDINADORA_USER_ID = os.getenv("COORDINADORA_USER_ID")


AVAILABLE_COURIERS = {
    "coordinadora": CoordinadoraClient(
        COORDINADORA_USER, COORDINADORA_PASSWORD, COORDINADORA_API, COORDINADORA_USER_ID
    ),
}
