from unittest import TestCase
from managers import Manager


class QueueEventReceivedTestCase(TestCase):

    def setUp(self) -> None:
        self.manager = Manager()
        return super().setUp()

    def test_queue_group_event_received(self):
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
            "Paused": "0",
            "PausedReason": "",
            "Ringinuse": "0"
        }
        self.manager.update(event_received)
        queue_group = self.manager.queues.get('Queue_1')
        expect_data = {
            "queuename": "Queue_1",
            "unavailable_members" : [],
            "idle_members": ['SIP/IP100'],
            "busy_members": [],
            "paused_members": [],
            "ringing_members": [],
            "members": ['SIP/IP100']
        }
        self.assertDictEqual(queue_group.data, expect_data)
        event_received = {
            "Event": "DeviceStateChange",
            "Privilege": "call,all",
            "Device": "SIP/IP100",
            "State": "INUSE"
        }
        self.manager.update(event_received)
        expect_data = {
            "queuename": "Queue_1",
            "unavailable_members" : [],
            "idle_members": [],
            "busy_members": ['SIP/IP100'],
            "paused_members": [],
            "ringing_members": [],
            "members": ['SIP/IP100']
        }
        self.assertDictEqual(queue_group.data, expect_data)
        event_received = {
            "Event": "DeviceStateChange",
            "Privilege": "call,all",
            "Device": "SIP/IP100",
            "State": "UNAVAILABLE"
        }
        self.manager.update(event_received)
        expect_data = {
            "queuename": "Queue_1",
            "unavailable_members": ['SIP/IP100'],
            "idle_members": [],
            "busy_members": [],
            "paused_members": [],
            "ringing_members": [],
            "members": ['SIP/IP100']
        }
        self.assertDictEqual(queue_group.data, expect_data)
        event_received = {
            "Event": "DeviceStateChange",
            "Privilege": "call,all",
            "Device": "SIP/IP100",
            "State": "RINGING"
        }
        self.manager.update(event_received)
        expect_data = {
            "queuename": "Queue_1",
            "unavailable_members": [],
            "idle_members": [],
            "busy_members": [],
            "paused_members": [],
            "ringing_members": ['SIP/IP100'],
            "members": ['SIP/IP100']
        }
        self.assertDictEqual(queue_group.data, expect_data)
        event_received = {
            "Event": "DeviceStateChange",
            "Privilege": "call,all",
            "Device": "SIP/IP100",
            "State": "NOT_INUSE"
        }
        self.manager.update(event_received)
        expect_data = {
            "queuename": "Queue_1",
            "unavailable_members": [],
            "idle_members": ['SIP/IP100'],
            "busy_members": [],
            "paused_members": [],
            "ringing_members": [],
            "members": ['SIP/IP100']
        }
        self.assertDictEqual(queue_group.data, expect_data)