class Event:

    def __init__(self, event: dict) -> None:
        self.data = event
        self.type = event['Event']
        self.key: str = self.get_key()

    def get_key(self) -> str:
        if 'QueueMemberStatus' == self.data['Event']:
            return self.data['Interface']
            
        return self.data['Device']
    