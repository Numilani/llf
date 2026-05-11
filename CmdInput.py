from textual.app import ComposeResult
from textual.widgets import Input
from textual.message import Message
from textual.reactive import reactive


class CmdInput(Input):

    def __init__(self) -> None:
        super().__init__()

