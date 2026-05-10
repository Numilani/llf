import sys
import os
import threading
from textual.app import App, ComposeResult
from textual.widgets import RichLog, Header, Footer

class StreamingApp(App):

    def compose(self) -> ComposeResult:
        yield Header()
        yield RichLog(id="log", highlight=True, markup=True)
        yield Footer()

    def on_mount(self) -> None:
        thread = threading.Thread(target=self._read_stream, daemon=True)
        thread.start()

    def _read_stream(self) -> None:
        try:
            for line in self.stream:
                self.call_from_thread(self._handle_line, line.rstrip("\n"))
        finally:
            self.call_from_thread(self._handle_done)

    def _handle_line(self, line: str) -> None:
        self.query_one("#log", RichLog).write(line)

    def _handle_done(self) -> None:
        self.query_one("#log", RichLog).write("[bold yellow]--- EOF ---[/bold yellow]")

def main():
    sys.stdin.close()
    sys.__stdin__ = open("/dev/tty", "r")
    StreamingApp().run(inline=True)

if __name__ == "__main__":
    main()
