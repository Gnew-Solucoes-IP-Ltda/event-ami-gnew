class Event:

    def __init__(self, event: dict) -> None:
        self.data = event
        self.type = event['Event']
        self.key: str = self.get_key()
    
    def channel2device(self, channel: str) -> str:
        posicao = channel.rfind('-')
        return channel[:posicao]

    def get_key(self) -> str:
        if 'QueueMemberStatus' == self.data['Event']:
            return self.data['Interface']

        elif self.data['Event'] in ['QueueCallerJoin', 'QueueCallerLeave']:
            return self.data['Queue']

        elif self.data['Event'] in ['BridgeEnter', 'BridgeLeave']:
            device = self.channel2device(self.data['Channel'])
            return device
        
        return self.data['Device']
    