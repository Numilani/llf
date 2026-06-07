import re

from textual.app import ComposeResult
from textual.widgets import Log
from textual.reactive import reactive
import asyncio
import sys

from objects.Filter import Filter


class FileLog(Log):
    log_lines: reactive[list[str]] = reactive(list)

    def __init__(self, filename) -> None:
        super().__init__()
        self.file = open(filename, "rb", buffering=0)
        self.filters: list[Filter] = []

    def compose(self) -> ComposeResult:
        yield Log()

    async def watch_log_lines(self, lines):
        if len(lines) == 0:
            return
        await self.apply_filters(lines[-1])

    async def read_lines(self):
        while True:
            line = await asyncio.to_thread(self.file.readline)
            if line == b"":
                await asyncio.sleep(0.1)
            self.app.call_from_thread(self.log_lines.append, line.decode("utf-8"))
            self.app.call_from_thread(self.mutate_reactive, FileLog.log_lines)
            # self.log_lines.append(line.decode("utf-8"))
            # self.mutate_reactive(FileLog.log_lines)
    
    async def apply_filters(self, line):
        already_printed = False
        if len(self.filters) == 0:
            self.write_line(line)
        else:
            for filter in self.filters:
                if already_printed:
                    continue
                matches: bool = await asyncio.to_thread(filter.regex_compiled.match(line))
                if matches:
                    self.write_line(line)
                    already_printed = True

    async def refilter_log(self):
        self.clear()

        if len(self.filters) == 0:
            self.write_lines(self.log_lines)
            return

        for line in self.log_lines:
            await self.apply_filters(line)

    async def on_mount(self) -> None:
        self.run_worker(self.read_lines(), exclusive=True, thread=True)
