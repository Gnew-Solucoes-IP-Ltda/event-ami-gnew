from unittest import TestCase
from event_ami_gnew.managers import GnewManagerAMIEvents

class EndpointEventReceivedTestCase(TestCase):

    def setUp(self) -> None:
        self.manager = GnewManagerAMIEvents()
        return super().setUp()

    def test_endpoint_event_received(self):
        event_received = {
            "Event": "DeviceStateChange",
            "Privilege": "call,all",
            "Device": "SIP/IP100",
            "State": "INUSE"
        }
        self.manager.update(event_received)
        self.assertEqual(1, self.manager.endpoints.count())
        expect_data = {
            "device": "SIP/IP100",
            "state": "INUSE",
            "queues" : []
        }
        endpoint = self.manager.endpoints.get('SIP/IP100')
        self.assertDictEqual(endpoint.data, expect_data)
        self.assertEqual(1, self.manager.endpoints.count())
        event_received = {
            "Event": "DeviceStateChange",
            "Privilege": "call,all",
            "Device": "SIP/IP100",
            "State": "NOT_INUSE"
        }
        self.manager.update(event_received)
        expect_data = {
            "device": "SIP/IP100",
            "state": "NOT_INUSE",
            "queues" : []
        }
        self.assertDictEqual(endpoint.data, expect_data)
        self.assertEqual(1, self.manager.endpoints.count())

    def test_queue_member_event_received(self):
        event_received = {
            "Event": "QueueMemberStatus",
            "Privilege": "agent,all",
            "Queue": "Queue_1",
            "MemberName": "SIP/IP100",
            "Interface": "SIP/IP100",
            "StateInterface": "SIP/IP100",
            "Membership": "static",
            "Penalty": "0",
            "CallsTaken": "0",
            "LastCall": "0",
            "InCall": "0",
            "Status": "6",
            "Paused": "0",
            "PausedReason": "",
            "Ringinuse": "0"
        }
        self.manager.update(event_received)
        expect_data = {
            "device": "SIP/IP100",
            "state": "NOT_INUSE",
            "queues" : [
                {
                    "queuename": "Queue_1",
                    "calls_taken": 0,
                    "paused_reason": "",
                    "paused": False,
                    "penalty": 0,
                    "last_call": "0"
                }
            ]
        }
        endpoint = self.manager.endpoints.get('SIP/IP100')
        self.assertDictEqual(endpoint.data, expect_data)
        self.assertEqual(1, self.manager.endpoints.count())
        self.assertEqual(1, endpoint.queues.count())
        event_received = {
            "Event": "QueueMemberStatus",
            "Privilege": "agent,all",
            "Queue": "Queue_1",
            "MemberName": "SIP/IP100",
            "Interface": "SIP/IP100",
            "StateInterface": "SIP/IP100",
            "Membership": "static",
            "Penalty": "1",
            "CallsTaken": "1",
            "LastCall": "1676986135",
            "InCall": "0",
            "Status": "6",
            "Paused": "1",
            "PausedReason": "pausa-cafe",
            "Ringinuse": "0"
        }
        self.manager.update(event_received)
        expect_data = {
            "device": "SIP/IP100",
            "state": "NOT_INUSE",
            "queues" : [
                {
                    "queuename": "Queue_1",
                    "calls_taken": 1,
                    "paused_reason": "pausa-cafe",
                    "paused": True,
                    "penalty": 1,
                    "last_call": "1676986135"
                }
            ]
        }
        self.assertDictEqual(endpoint.data, expect_data)
        self.assertEqual(1, self.manager.endpoints.count())
        self.assertEqual(1, endpoint.queues.count())
        