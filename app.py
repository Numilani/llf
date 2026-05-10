from textual.app import App, ComposeResult
from textual.widgets import RichLog, Log, Footer, Header, Input
import asyncio
import sys
from asyncio import Queue

class llfApp(App):

    log_lines = []
    queue: asyncio.Queue = asyncio.Queue()

    def __init__(self, stream):
        super().__init__()
        self.stream = stream

    def compose(self) -> ComposeResult:
        yield Header()
        # yield Log()
        # yield Input()
        yield Footer()

    # async def read_lines(self):
    #     while True:
    #         line = await asyncio.to_thread(sys.stdin.readline)
    #         if line == "":
    #             return
    #         await self.queue.put(line)
    #
    #
    # async def write_log(self, ttyout):
    #     while True:
    #         new_line = await self.queue.get()
    #         if new_line is None:
    #             return
    #         self.log_lines.append(new_line)
    #         for line in self.log_lines[-16:]:
    #             ttyout.write(line)
    #             ttyout.flush()
    #

    # async def on_mount(self) -> None:
    #     ttyin = open("/dev/tty", "r")
    #     ttyout = open("/dev/tty", "w")
    #
    #     read_task = asyncio.create_task(self.read_lines())
    #     write_task = asyncio.create_task(self.write_log(ttyout))
    #     await read_task
    #     await write_task


if __name__ == "__main__":
    sys.stdin.close()
    sys.__stdin__ = open("/dev/tty")
    app = llfApp()
    app.run()
