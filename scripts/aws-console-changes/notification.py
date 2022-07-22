import argparse
import json
from http import HTTPStatus

import requests

python_workshop_webhook_url = 'https://webhook.site/d02c4f10-feab-4d87-acbd-32313306ee36'  # python_workshop channel in TIOEngineering workspace.
message = "Super! {username}, you have successfully completed kata `{kata}` in your journey of learning python best " \
          "practices. "


def send_notification(username):
    slack_data = {'text': message.format(username=username, kata=get_kata_number())}
    response = requests.post(
        python_workshop_webhook_url, data=json.dumps(slack_data), headers={"Content-Type": "application/json"}
    )
    if response.status_code != HTTPStatus.OK:
        raise ValueError(
            'Request to slack returned an error %s, the response is:\n%s'
            % (response.status_code, response.text)
        )


def get_kata_number():
    parser = argparse.ArgumentParser()
    parser.add_argument('--kata', type=int)
    args = parser.parse_args()
    if args.kata is None:
        return 0
    return args.kata


if __name__ == "__main__":
    username = "Matthew"
    send_notification(username)