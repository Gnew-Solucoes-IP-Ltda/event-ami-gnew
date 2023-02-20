class Endpoint:
    
    def __init__(self, device: str, state: str):
        self.device = device
        self.state = state

    @property
    def data(self) -> dict:
        return {
            'device': self.device,
            'state': self.state
        }


class Objects:

    _data = {}

    class DoesExists(Exception):
        ...

    def validate_data(self, device: str) -> None:
        if not self.exists(device):
            raise Objects.DoesExists()

    def count(self) -> int:
        return len(self._data)
            
    def exists(self, device: str) -> bool:
        return device in self._data      
    
    def create(self, event: dict) -> Endpoint:
        endpoint = Endpoint(
            event['Device'],
            event['State']
        )
        self._data[event['Device']] = endpoint
        return endpoint
    
    def get(self, device: str) -> Endpoint:
        self.validate_data(device)
        return self._data[device]
    
    def update(self, event: dict) -> Endpoint:
        if not self.exists(event['Device']):
            return self.create(event)
        
        endpoint = self.get(event['Device'])
        endpoint.state = event['State']
        return endpoint
    
    def delete(self, device: str) -> None:
        self.validate_data(device)
        del self._data[device]


class Endpoints:
    objects = Objects()