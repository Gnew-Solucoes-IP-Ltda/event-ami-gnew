from unittest import TestCase
from event_ami_gnew.managers import GnewManagerAMIEvents


class QueueCallsEventReceivedTestCase(TestCase):

    def setUp(self) -> None:
        self.manager = GnewManagerAMIEvents()
        return super().setUp()

    def test_queue_call_event_received(self):
        event_received = {
            "Event": "QueueCallerJoin",
            "Privilege": "agent,all",
            "Channel": "SIP/IPEu91w-00000002",
            "ChannelState": "6",
            "ChannelStateDesc": "Up",
            "CallerIDNum": "7340",
            "CallerIDName": "Tatianno",
            "ConnectedLineNum": "<unknown>",
            "ConnectedLineName": "<unknown>",
            "Language": "pt_BR",
            "AccountCode": "1",
            "Context": "macro-filas",
            "Exten": "s",
            "Priority": "10",
            "Uniqueid": "1668187694.3",
            "Linkedid": "1668187694.3",
            "Queue": "Queue_1",
            "Position": "1",
            "Count": "1"
        }
        self.manager.update(event_received)
        queue_group = self.manager.queues.get('Queue_1')
        expect_data = {
            "callerid": {
                "num": "7340",
                "name": "Tatianno"
            },
            "uniqueid": "1668187694.3",
            "linkedid": "1668187694.3",
            "position": 1,
            "count": 1
        }
        self.assertEqual(queue_group.calls_waiting.get("1668187694.3").data, expect_data)
        event_received = {
            "Event": "QueueCallerLeave",
            "Privilege": "agent,all",
            "Channel": "SIP/IPEu91w-00000002",
            "ChannelState": "6",
            "ChannelStateDesc": "Up",
            "CallerIDNum": "7340",
            "CallerIDName": "Tatianno",
            "ConnectedLineNum": "100",
            "ConnectedLineName": "100",
            "Language": "pt_BR",
            "AccountCode": "1",
            "Context": "macro-filas",
            "Exten": "s",
            "Priority": "10",
            "Uniqueid": "1668187694.3",
            "Linkedid": "1668187694.3",
            "Queue": "Queue_1",
            "Position": "1",
            "Count": "0"
        }
        self.manager.update(event_received)
        self.assertEqual(0, queue_group.calls_waiting.count())