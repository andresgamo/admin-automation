import os
from slack_bolt import App
from slack_bolt.adapter.aws_lambda import SlackRequestHandler

app = App(
    token=os.environ["SLACK_BOT_TOKEN"],
    signing_secret=os.environ["SLACK_SIGNING_SECRET"],
)


# @app.command("/send-package")
# def show_courier_menu(ack, body, client):
#     ack()
#     client.chat_postMessage(
#         channel=body["channel_id"],
#         text="¿Con quién quieres enviar tu paquete?",
#         blocks=[
#             {
#                 "type": "section",
#                 "text": {"type": "mrkdwn", "text": "Selecciona tu courier:"},
#                 "accessory": {
#                     "type": "static_select",
#                     "action_id": "select_courier",
#                     "placeholder": {"type": "plain_text", "text": "Elige un courier"},
#                     "options": [
#                         {"text": {"type": "plain_text", "text": "Coordinadora"}, "value": "coordinadora"},
#                         {
#                             "text": {"type": "plain_text", "text": "FedEx"},
#                             "value": "fedex",
#                         },
#                         {"text": {"type": "plain_text", "text": "UPS"}, "value": "ups"},
#                     ],
#                 },
#             }
#         ],
#     )


# @app.action("select_courier")
# def handle_courier(ack, body, client):
#     ack()
#     courier = body["actions"][0]["selected_option"]["value"]
#     # Here you’d call your existing `process_delivery` or similar
#     client.chat_postMessage(
#         channel=body["channel_id"],
#         text=f"Genial, vamos a usar *{courier.upper()}*. Ahora necesito los detalles de tu envío…",
#     )


lambda_handler = SlackRequestHandler(app).handle
