from typing import BinaryIO

from textual.app import App, ComposeResult
from textual.widgets import RichLog, Log, Footer, Header, Input
from textual.reactive import reactive
import asyncio
import sys
from asyncio import Queue


class llfApp(App):

    log_lines: reactive[list[str]] = reactive([])

    def __init__(self, filename) -> None:
        super().__init__()
        self.file = open(filename, "rb", buffering=0)

    def compose(self) -> ComposeResult:
        yield Header()
        yield Log()
        yield Input()
        yield Footer()

    async def read_lines(self):
        while True:
            line = await asyncio.to_thread(self.file.readline)
            if line == "":
                return
            self.log_lines.append(str(line))

    def 


    async def on_mount(self) -> None:

        read_task = asyncio.create_task(self.read_lines())
        write_task = asyncio.create_task(self.write_log(ttyout))
        await read_task
        await write_task
