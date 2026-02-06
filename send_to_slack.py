from slack_sdk import WebClient
import os


def send_file(filepath, channel=None):
token = os.getenv('SLACK_BOT_TOKEN')
if not token:
raise RuntimeError('SLACK_BOT_TOKEN required')
client = WebClient(token=token)
channel = channel or os.getenv('SLACK_CHANNEL')
client.files_upload(channels=channel, file=filepath, title='Daily Chat Report')


if __name__ == '__main__':
import sys
send_file(sys.argv[1])
