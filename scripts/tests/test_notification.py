import json
import unittest
from http import HTTPStatus
from unittest.mock import MagicMock

import requests_mock

import sys
# insert into system path to allow the python modules within that folder to be callable
sys.path.insert(0, 'C:/Users/palmerm/GitHub/dapinder-python-workshop/scripts/logs_processor') ##this line works
# sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from notification import Notification ## this line works

## THE .. SYNTAX IS FOR JUMPING UP 1 FOLDER FROM THE CURRENT FILE'S LOCATION
# import notification

# from ..logs_processor import notification


class TestNotification(unittest.TestCase):
    TEST_USERNAME = "MATTHEW"
    notification = None
    EXPECTED_SLACK_MESSAGE = json.loads(
        '{ "text": "Super! MATTHEW, you have successfully completed kata `5` in your journey of learning '
        'python best practices."}')

    def setUp(self) -> None:
        print("I am setup, You can use me to define instructions that will be executed before each test method.")
        # create Notification Object
        self.notification = Notification()
        # mock `get_kata_number()` as our scope here is to test `get_slack_message()` function
        self.notification.get_kata_number = MagicMock(name="get_kata_number")
        self.notification.get_kata_number.return_value = 5

    def tearDown(self) -> None:
        print("I am teardown, You can use me to define instructions that will be executed after each test method.")

    def test_slack_message(self) -> None:
        slack_message_returned = self.notification.get_slack_message(username=TestNotification.TEST_USERNAME)
        self.assertEqual(TestNotification.EXPECTED_SLACK_MESSAGE, slack_message_returned)

    def test_send_notification_http_ok(self) -> None:
        with requests_mock.Mocker() as m:
            m.post(requests_mock.ANY, text=json.dumps(TestNotification.EXPECTED_SLACK_MESSAGE),
                status_code=HTTPStatus.OK)
            status_code_returned = self.notification.send_notification(username=TestNotification.TEST_USERNAME)
            self.assertEqual(HTTPStatus.OK, status_code_returned)

    def test_send_notification_http_not_ok(self) -> None:
        with requests_mock.Mocker() as m:
            m.post(requests_mock.ANY, text=json.dumps(TestNotification.EXPECTED_SLACK_MESSAGE),
                status_code=HTTPStatus.NOT_FOUND)
            with self.assertRaises(ValueError) as context:
                self.notification.send_notification(username=TestNotification.TEST_USERNAME)
            self.assertTrue(
                str(context.exception.args[0]).startswith("Request to slack returned an error HTTPStatus.NOT_FOUND"))

####### COMMAND TO RUN IN TERMINAL TO RUN THIS FILE WITH UNITTEST -> "python -m pipenv run python -m unittest scripts\tests\test_notification.py"