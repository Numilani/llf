from textual.app import ComposeResult
from textual.widgets import Log
from textual.reactive import reactive
import asyncio
import sys


class FileLog(Log):
    log_lines: reactive[list[str]] = reactive([])

    def __init__(self, filename) -> None:
        super().__init__()
        self.file = open(filename, "rb", buffering=0)

    def compose(self) -> ComposeResult:
        yield Log()

    async def read_lines(self):
        while True:
            line = await asyncio.to_thread(self.file.readline)
            self.write_line(line.decode("utf-8"))
            # TODO: does format need to be configurable?
            # TODO: does there need to be a break condition?

    async def on_mount(self) -> None:
        self.run_worker(self.read_lines(), exclusive=True)
