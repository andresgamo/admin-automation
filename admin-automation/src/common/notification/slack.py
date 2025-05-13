from common.clients.slack.config import SlackClient


client = SlackClient()


def reply_to_slack(channel, msg: str):
    return client.post_message(channel, msg)

def upload_file(channel, file_bytes, filename):
    return client.upload_file(channel, file_bytes, filename)
