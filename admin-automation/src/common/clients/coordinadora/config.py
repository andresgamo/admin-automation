import re
import logging
import textwrap
import requests
from tenacity import retry, stop_after_attempt, wait_fixed

from common.utils.strings import extractor_with_regex
from common.delivery.constants.dane_codes import DANE


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class CoordinadoraClient:

    _FAULTSTRING_RE = re.compile(r"<faultstring[^>]*>(.*?)</faultstring>")

    def __init__(self, user, password, api_url, user_id):
        self.api_url = api_url
        self.headers = {"Content-Type": "text/xml"}
        self.user = user
        self.password = password
        self.session = requests.Session()
        self.user_id = user_id

    def _build_envelope(self, body: str) -> str:
        return textwrap.dedent(
            f"""
                <soap:Envelope 
                    xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/" 
                    xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
                    xmlns:xsd="http://www.w3.org/2001/XMLSchema"
                    xmlns:tns="https://sandbox.coordinadora.com/agw/ws/guias/1.6/server.php">
                <soap:Body>
                    {body}
                </soap:Body>
                </soap:Envelope>
            """
        )

    @retry(stop=stop_after_attempt(3), wait=wait_fixed(2))
    def _post(self, body_envelope):
        envelope = self._build_envelope(body_envelope)
        try:
            response = self.session.post(
                url=self.api_url, data=envelope, headers=self.headers, timeout=30
            )
            response.raise_for_status()
            return response
        except requests.HTTPError as error:
            text_error = error.response.text
            try:
                fault_msg = extractor_with_regex(self._FAULTSTRING_RE, text_error)
            except ValueError:
                fault_msg = "<no <faultstring> in body>"
            logger.error(
                "SOAP call failed with HTTP %d: %s; faultstring: %s",
                error.response.status_code,
                error,
                fault_msg,
            )
            raise
        except requests.RequestException as error:
            logger.error("RequestException on SOAP call: %s", error)
            raise
        except Exception as error:
            logger.error("%s", error)
            raise

    def generate_guide_number(self, sender, package, recipient):
        success_tag = re.compile(r"<codigo_remision[^>]*>(.*?)</codigo_remision>")
        body_envelope = f"""
            <Guias_generarGuia>
                <p>
                    <id_cliente>{self.user_id}</id_cliente>
                    <id_remitente>{sender.id}</id_remitente>
                    <nit_remitente>{sender.nit}</nit_remitente>
                    <nombre_remitente>Gorilla {sender.name} SAS</nombre_remitente>
                    <direccion_remitente>{sender.address}</direccion_remitente>
                    <telefono_remitente>{sender.phone}</telefono_remitente>
                    <ciudad_remitente>{sender.city}</ciudad_remitente>
                    <nit_destinatario>{recipient.nit}</nit_destinatario>
                    <div_destinatario>{recipient.div}</div_destinatario>
                    <nombre_destinatario>{recipient.name}</nombre_destinatario>
                    <direccion_destinatario>{recipient.address}</direccion_destinatario>
                    <ciudad_destinatario>{DANE[recipient.city.upper()]}</ciudad_destinatario>
                    <telefono_destinatario>{recipient.phone}</telefono_destinatario>
                    <valor_declarado>{package.value}</valor_declarado>
                    <codigo_cuenta>2</codigo_cuenta>
                    <codigo_producto>0</codigo_producto>
                    <nivel_servicio>1</nivel_servicio>
                    <contenido>{package.content_description}</contenido>
                    <referencia>{package.reference_description}</referencia>
                    <observaciones>{package.comments}</observaciones>
                    <estado>IMPRESO</estado>
                    <detalle>
                        <item>
                            <ubl>1</ubl>
                            <alto>{package.height}</alto>
                            <ancho>{package.width}</ancho>
                            <largo>{package.length}</largo>
                            <peso>{package.weight}</peso>
                            <unidades>{package.items_count}</unidades>
                        </item>
                    </detalle>
                    <margen_izquierdo>1</margen_izquierdo>
                    <margen_superior>1</margen_superior>
                    <usuario>{self.user}</usuario>
                    <clave>{self.password}</clave>
                </p>
            </Guias_generarGuia>
        """
        response = self._post(body_envelope)
        guide_number = extractor_with_regex(success_tag, response.text)
        return guide_number

    def generate_guide_file(self, code):
        success_tag = re.compile(r"<rotulos[^>]*>(.*?)</rotulos>")
        error_tag = re.compile(r"<error[^>]*>(.*?)</error>")
        body_envelope = f"""
            <Guias_imprimirRotulos>
                <p>
                    <id_rotulo>44</id_rotulo>
                    <codigos_remisiones>
                        <item>{code}</item>
                    </codigos_remisiones>
                    <usuario>{self.user}</usuario>
                    <clave>{self.password}</clave>
                </p>
            </Guias_imprimirRotulos>
        """
        response = self._post(body_envelope)
        file = extractor_with_regex(success_tag, response.text)
        if not file:
            logger.error(
                "Error generating pdf. Error: %s",
                extractor_with_regex(error_tag, response.text),
            )
            return None
        return file
