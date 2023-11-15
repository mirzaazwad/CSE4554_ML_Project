    def __init__(
            self,
            type: str,
            client_conn: connections.ClientConnection,
            server_conn: connections.ServerConnection,
            live: bool=None
    ) -> None:
        self.type = type
        self.id = str(uuid.uuid4())
        self.client_conn = client_conn
        self.server_conn = server_conn
        self.live = live

        self.error = None  # type: typing.Optional[Error]
        self.intercepted = False  # type: bool
        self._backup = None  # type: typing.Optional[Flow]
        self.reply = None  # type: typing.Optional[controller.Reply]
        self.marked = False  # type: bool
        self.metadata = dict()  # type: typing.Dict[str, str]