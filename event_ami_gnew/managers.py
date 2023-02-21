from typing import List
from event_ami_gnew.events import Event
from event_ami_gnew.entities import Endpoint, QueueGroup


class EndpointsManager:
    _data = {}

    class DoesExists(Exception):
        ...
    
    def get_state(self, event: Event) -> str:
        return event.data['State']

    def validate_data(self, device: str) -> None:
        if not self.exists(device):
            raise EndpointsManager.DoesExists()

    def count(self) -> int:
        return len(self._data)
            
    def exists(self, device: str) -> bool:
        return device in self._data   

    def all(self) -> List[Endpoint]:
        return [self._data[key] for key in self._data]
    
    def create(self, event: Event) -> Endpoint:
        state = self.get_state(event)
        endpoint = Endpoint(event.key, state)
        self._data[event.key] = endpoint
        del state
        return endpoint
    
    def get(self, device: str) -> Endpoint:
        self.validate_data(device)
        return self._data[device]
    
    def update(self, event: Event) -> Endpoint:
        state = self.get_state(event)

        if not self.exists(event.key):
            return self.create(event)
        
        endpoint = self.get(event.key)
        endpoint.state = state
        del state
        return endpoint
    
    def delete(self, device: str) -> None:
        self.validate_data(device)
        del self._data[device]


class QueuesGroupManager:
    _data = {}

    class DoesExists(Exception):
        ...

    def exists(self, key: str) -> bool:
        return key in self._data
    
    def validate_data(self, queuename: str) -> None:
        if not self.exists(queuename):
            raise QueuesGroupManager.DoesExists()
    
    def all(self) -> List[QueueGroup]:
        return [self._data[key] for key in self._data]
    
    def create(self, queuename: str) -> QueueGroup:
        queue_group = QueueGroup(
            queuename=queuename
        )
        self._data[queuename] = queue_group
        return queue_group
    
    def get(self, queuename: str) -> QueueGroup:
        self.validate_data(queuename)
        return self._data[queuename]
    
    def get_or_create(self, queuename: str) -> QueueGroup:
        if self.exists(queuename):
            return self.get(queuename)
        
        return self.create(queuename)

    def update(self, device: str, state: str, queuename: str, paused: bool) -> QueueGroup:
        queue_group = self.get_or_create(queuename)
        queue_group.update(device, state, paused)
        return queue_group
    
    def delete(self, queuename: str) -> None:
        self.validate_data(queuename)
        del self._data[queuename]

        
class GnewManagerAMIEvents:
    endpoints = EndpointsManager()
    queues = QueuesGroupManager()
    _updated_objects = []

    def _add_updated_objects(self, obj: object) -> None:
        if obj not in self._updated_objects:
            self._updated_objects.append(obj)
    
    def get_updated_objects(self) -> List[object]:
        updated_objects = self._updated_objects
        self._updated_objects = []
        return updated_objects

    def _update_queue_event(self, device: str, state: str, queuename: str, paused: bool) -> None:
        queue_group = self.queues.update(
            device=device, 
            state=state,
            queuename=queuename,
            paused=paused
        )
        self._add_updated_objects(queue_group)
    
    def _update_endpoint_queues(self, endpoint: Endpoint) -> None:
        for queue in endpoint.queues.all():
            self._update_queue_event(
                endpoint.device,
                endpoint.state,
                queue.queuename,
                queue.paused
            )

    def _update_device_event(self, event: Event) -> None:
        if event.type == 'DeviceStateChange' and 'SIP/' in event.key:
            endpoint = self.endpoints.update(event)
            self._update_endpoint_queues(endpoint)
            self._add_updated_objects(endpoint)
            
    def _update_queue_member_event(self, event: Event) -> None:
        if event.type == 'QueueMemberStatus':
            if self.endpoints.exists(event.key):
                endpoint = self.endpoints.get(event.key)
                queue = endpoint.queues.update(event)
                self._update_queue_event(
                    endpoint.device,
                    endpoint.state,
                    queue.queuename,
                    queue.paused
                )
                self._add_updated_objects(endpoint)
    
    def _update_queue_calls_event(self, event: Event) -> None:
        if event.type in ['QueueCallerJoin', 'QueueCallerLeave']:
            queue_group = self.queues.get_or_create(event.data['Queue'])
            queue_group.calls_waiting.update(event)
            self._add_updated_objects(queue_group)
    
    def _update_endpoint_calls_event(self, event: Event) -> None:
        if event.type in ['BridgeEnter', 'BridgeLeave']:
            endpoint = self.endpoints.get(event.key)
            endpoint.calls.update(event)
            self._add_updated_objects(endpoint)

    def update(self, event_received: dict) -> None:
        event = Event(event_received)
        self._update_device_event(event)
        self._update_queue_member_event(event)
        self._update_queue_calls_event(event)
        self._update_endpoint_calls_event(event)
        del event