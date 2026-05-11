from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input
from textual.reactive import reactive
from FileLog import FileLog
from CmdInput import CmdInput


class llfApp(App):
    log_lines: reactive[list[str]] = reactive([])

    def __init__(self, filename) -> None:
        super().__init__()
        self.filename = filename

    def compose(self) -> ComposeResult:
        yield Header()
        yield FileLog(self.filename)
        yield CmdInput()
        yield Footer()

    def on_input_submitted(self, event: Input.Submitted):
        self.query_one(FileLog).write_line(event.value)
