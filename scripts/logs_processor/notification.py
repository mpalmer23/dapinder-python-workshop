import argparse
import json
from http import HTTPStatus

import requests

class Notification:

    python_workshop_webhook_url = 'https://webhook.site/d02c4f10-feab-4d87-acbd-32313306ee36'  # python_workshop channel in TIOEngineering workspace.
    message = "Super! {username}, you have successfully completed kata `{kata}` in your journey of learning python best " \
            "practices."

    def get_kata_number(self) -> int:
        parser = argparse.ArgumentParser()
        parser.add_argument('--kata', type=int)
        args = parser.parse_args()
        if args.kata is None:
            return 0
        return args.kata

    def get_slack_message(self, username: str) -> dict:
        slack_data = {'text': self.message.format(username=username.strip(), kata=self.get_kata_number())}
        return slack_data


    def send_notification(self, username: str) -> int:
        slack_data = self.get_slack_message(username = username)
        response = requests.post(
            self.python_workshop_webhook_url, data=json.dumps(slack_data), headers={"Content-Type": "application/json"}
        )
        if response.status_code != HTTPStatus.OK:
            raise ValueError(
                'Request to slack returned an error %s, the response is:\n%s'
                % (response.status_code, response.text)
            )
        return response.status_code


if __name__ == "__main__":
    notification = Notification()
    username = "Matthew"
    # username = 1

    notification.send_notification(username = username)

####### COMMAND TO RUN IN TERMINAL TO RUN THIS FILE WITH MYPY TESTING --> "mypy scripts\logs_processor\notification.py"