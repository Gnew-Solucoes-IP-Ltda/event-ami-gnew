from typing import List
from event_ami_gnew.events import Event


class Queue:
    
    def __init__(
        self, 
        queuename: str,
        calls_taken: int, 
        paused_reason: str, 
        paused: bool, 
        penalty: int, 
        last_call: str) -> None:

        self.queuename = queuename
        self.calls_taken = calls_taken
        self.paused_reason = paused_reason
        self.paused = paused
        self.penalty = penalty
        self.last_call = last_call
        self.key = queuename
    
    def update_pause_event(self, paused: bool, paused_reason: str="") -> bool:
        self.paused = paused
        self.paused_reason = paused_reason
        return True
    
    def update_penalty_event(self, penalty: int) -> bool:
        self.penalty = penalty
        return True
    
    def update_calls_event(self, calls_taken: int, last_call: str) -> bool:
        self.calls_taken = calls_taken
        self.last_call = last_call
        return True
    
    @property
    def data(self) -> dict:
        return {
            'queuename': self.queuename,
            'calls_taken': self.calls_taken,
            'paused_reason': self.paused_reason,
            'paused': self.paused,
            'penalty': self.penalty,
            'last_call': self.last_call
        }


class QueueGroup:

    def __init__(self, queuename: str) -> None:
        self.queuename = queuename
        self.unavailable_members = []
        self.idle_members = []
        self.busy_members = []
        self.paused_members = []
        self.ringing_members = []
        self.members = []
        self.key = queuename
        self._unavailable_state = ['UNKNOWN', 'INVALID', 'UNAVAILABLE']
        self._idle_state = ['NOT_INUSE']
        self._busy_state = ['INUSE', 'BUSY', 'ONHOLD']
        self._ringing_state = ['RINGING', 'RINGINUSE']
        
    
    def _count_paused_members(self, device: str, paused: bool) -> bool:
        if paused:
            if device not in self.paused_members:
                self.paused_members.append(device)
                return True
        
        else:
            if device in self.paused_members:
                self.paused_members.remove(device)
                return True
        
        return False
    
    def _count_members(self, device: str) -> bool:
        if device not in self.members:
            self.members.append(device)
            return True

        return False
    
    def get_states_list(self):
        return [
            'unavailable_members',
            'idle_members',
            'busy_members',
            'ringing_members'
        ]
    
    def _review_other_states(self, device: str, states_list_review: list) -> None:
        for state_attr in states_list_review:
            state_list = getattr(self, state_attr)

            if device in state_list:
                state_list.remove(device)
    
    def _count_idle_members(self, device: str, state: str) -> bool:
        if state in self._idle_state:
            if device not in self.idle_members:
                self.idle_members.append(device)
                states_list = self.get_states_list()
                states_list.remove('idle_members')
                self._review_other_states(device, states_list)
                return True
        
        return False

    def _count_busy_members(self, device: str, state: str) -> bool:
        if state in self._busy_state:
            if device not in self.busy_members:
                self.busy_members.append(device)
                states_list = self.get_states_list()
                states_list.remove('busy_members')
                self._review_other_states(device, states_list)
                return True
        
        return False

    def _count_unavailable_members(self, device: str, state: str) -> bool:
        if state in self._unavailable_state:
            if device not in self.unavailable_members:
                self.unavailable_members.append(device)
                states_list = self.get_states_list()
                states_list.remove('unavailable_members')
                self._review_other_states(device, states_list)
                return True
        
        return False

    def _count_ringing_members(self, device: str, state: str) -> bool:
        if state in self._ringing_state:
            if device not in self.ringing_members:
                self.ringing_members.append(device)
                states_list = self.get_states_list()
                states_list.remove('ringing_members')
                self._review_other_states(device, states_list)
                return True
        
        return False
    
    def update(self, device: str, state: str, paused: bool) -> None:
        self._count_members(device)
        self._count_paused_members(device, paused)
        self._count_idle_members(device, state)
        self._count_busy_members(device, state)
        self._count_unavailable_members(device, state)
        self._count_ringing_members(device, state)
    
    @property
    def data(self) -> dict:
        return {
            "queuename": self.queuename,
            "unavailable_members": self.unavailable_members,
            "idle_members": self.idle_members,
            "busy_members": self.busy_members,
            "paused_members": self.paused_members,
            "ringing_members": self.ringing_members,
            "members": self.members,
        }
    
    
class EndpointQueues:

    class DoesExists(Exception):
        ...

    def __init__(self):
        self._data = {}
    
    def str2int(self, value: str) -> int:
        return int(value)
    
    def str2bool(self, value: str) -> bool:
        return not value == '0'
    
    def get_key(self, event: Event) -> str:
        return event.data['Queue']
    
    def all(self, serialized: bool=False) -> List[Queue]:
        
        if serialized:
            return [self._data[queuename].data for queuename in self._data]

        return [self._data[queuename] for queuename in self._data]
    
    def count(self) -> int:
        return len(self._data)
    
    def exists(self, queuename: str) -> bool:
        return queuename in self._data
    
    def validate_data(self, queuename: str) -> None:
        if not self.exists(queuename):
            raise EndpointQueues.DoesExists()
    
    def get(self, queuename: str) -> Queue:
        self.validate_data(queuename)
        return self._data[queuename]
    
    def create(self, event: Event) -> Queue:
        key = self.get_key(event)
        queue = Queue(
            queuename=key,
            calls_taken=self.str2int(event.data['CallsTaken']),
            paused_reason=event.data['PausedReason'],
            paused=self.str2bool(event.data['Paused']),
            penalty=self.str2int(event.data['Penalty']),
            last_call=event.data['LastCall']
        )
        self._data[key] = queue
        return queue
    
    def update(self, event: Event) -> Queue:
        if not self.exists(event.key):
            return self.create(event)
        
        queue = self.get(event.key)
        queue.update_pause_event(
            paused=self.str2bool(event.data['Paused']), 
            paused_reason=event.data['PausedReason']
        )
        queue.update_penalty_event(
            penalty=self.str2int(event.data['Penalty'])
        )
        queue.update_calls_event(
            calls_taken = event.data['CallsTaken'],
            last_call = event.data['LastCall']
        )
        return queue


class Endpoint:
    
    def __init__(self, device: str, state: str):
        self.device = device
        self.state = state
        self.queues = EndpointQueues()

    @property
    def data(self) -> dict:
        return {
            'device': self.device,
            'state': self.state,
            'queues': self.queues.all(serialized=True)
        }