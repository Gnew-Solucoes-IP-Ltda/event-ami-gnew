from unittest import TestCase
from event_ami_gnew.managers import GnewManagerAMIEvents


class EndpointCallsEventReceivedTestCase(TestCase):

    def setUp(self) -> None:
        self.manager = GnewManagerAMIEvents()
        return super().setUp()

    def test_endpoint_call_received(self):
        event_received = {
            "Event": "DeviceStateChange",
            "Privilege": "call,all",
            "Device": "SIP/IP100",
            "State": "INUSE"
        }
        self.manager.update(event_received)
        event_received = {
            "Event": "BridgeEnter",
            "Privilege": "call,all",
            "BridgeUniqueid": "15d70f0b-5ad0-4235-a4eb-fca0c29a5797",
            "BridgeType": "basic",
            "BridgeTechnology": "simple_bridge",
            "BridgeCreator": "<unknown>",
            "BridgeName": "<unknown>",
            "BridgeNumChannels": "1",
            "BridgeVideoSourceMode": "none",
            "Channel": "SIP/IP100-00000003",
            "ChannelState": "6",
            "ChannelStateDesc": "Up",
            "CallerIDNum": "100",
            "CallerIDName": "100",
            "ConnectedLineNum": "7340",
            "ConnectedLineName": "Tatianno",
            "Language": "pt_BR",
            "AccountCode": "",
            "Context": "CONTEXT_1",
            "Exten": "IPEu91w",
            "Priority": "1",
            "Uniqueid": "1668187695.4",
            "Linkedid": "1668187694.3"
        }
        self.manager.update(event_received)
        endpoint = self.manager.endpoints.get('SIP/IP100')
        self.assertEqual(1, endpoint.calls.count())
        expect_data = {
            "callerid": {
                "num": "100", 
                "name": "100"
            }, 
            "uniqueid": "1668187695.4", 
            "linkedid": "1668187694.3", 
            "position": None, 
            "count": None
        }
        self.assertDictEqual(endpoint.calls.get('1668187695.4').data, expect_data)
        event_received = {
            "Event": "BridgeLeave",
            "Privilege": "call,all",
            "BridgeUniqueid": "15d70f0b-5ad0-4235-a4eb-fca0c29a5797",
            "BridgeType": "basic",
            "BridgeTechnology": "simple_bridge",
            "BridgeCreator": "<unknown>",
            "BridgeName": "<unknown>",
            "BridgeNumChannels": "1",
            "BridgeVideoSourceMode": "none",
            "Channel": "SIP/IP100-00000003",
            "ChannelState": "6",
            "ChannelStateDesc": "Up",
            "CallerIDNum": "100",
            "CallerIDName": "100",
            "ConnectedLineNum": "7340",
            "ConnectedLineName": "Tatianno",
            "Language": "pt_BR",
            "AccountCode": "",
            "Context": "CONTEXT_1",
            "Exten": "IPEu91w",
            "Priority": "1",
            "Uniqueid": "1668187695.4",
            "Linkedid": "1668187694.3"
        }
        self.manager.update(event_received)
        self.assertEqual(0, endpoint.calls.count())