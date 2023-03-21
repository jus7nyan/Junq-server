class User:
    def __init__(self, nick, socket, status, pub_key="") -> None:
        self.nick = nick
        self.socket = socket
        self.status = status
        self.pub_key = pub_key