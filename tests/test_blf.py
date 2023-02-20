from unittest import TestCase
from managers import Endpoints

class BlfTestCase(TestCase):

    def setUp(self) -> None:
        self.endpoints = Endpoints()
        return super().setUp()

    def test_endpoint_event_received(self):
        self.assertEqual(0, self.endpoints.objects.count())
        event_received = {
            "Event": "DeviceStateChange",
            "Privilege": "call,all",
            "Device": "SIP/IP100",
            "State": "INUSE"
        }
        endpoint = self.endpoints.objects.update(event_received)
        self.assertEqual(1, self.endpoints.objects.count())
        expect_data = {
            "device": "SIP/IP100",
            "state": "INUSE"
        }
        self.assertDictEqual(endpoint.data, expect_data)
        self.assertEqual(1, self.endpoints.objects.count())
        event_received = {
            "Event": "DeviceStateChange",
            "Privilege": "call,all",
            "Device": "SIP/IP100",
            "State": "NOT_INUSE"
        }
        endpoint = self.endpoints.objects.update(event_received)
        expect_data = {
            "device": "SIP/IP100",
            "state": "NOT_INUSE"
        }
        self.assertDictEqual(endpoint.data, expect_data)
        self.assertEqual(1, self.endpoints.objects.count())
