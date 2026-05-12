import re

from textual.app import ComposeResult
from textual.widgets import Log
from textual.reactive import reactive
import asyncio
import sys

from objects.Filter import Filter


class FileLog(Log):
    log_lines: reactive[list[str]] = reactive(list, recompose=True)

    def __init__(self, filename) -> None:
        super().__init__()
        self.file = open(filename, "rb", buffering=0)
        self.filters: list[Filter] = []

    def compose(self) -> ComposeResult:
        yield Log()

    def watch_log_lines(self, lines):
        if len(lines) == 0:
            return
        self.apply_filters(lines[-1])

    async def read_lines(self):
        while True:
            line = await asyncio.to_thread(self.file.readline)
            self.log_lines.append(line.decode("utf-8"))
            self.mutate_reactive(FileLog.log_lines)
            # self.write_line(line.decode("utf-8"))
            # TODO: does format need to be configurable?
            # TODO: does there need to be a break condition?

    def apply_filters(self, line):
        already_printed = False
        if len(self.filters) == 0:
            self.write_line(line)
        else:
            for filter in self.filters:
                if already_printed:
                    continue
                if filter.regex_compiled.match(line) is not None:
                    self.write_line(line)
                    already_printed = True

    def refilter_log(self):
        self.clear()

        for line in self.log_lines:
            self.apply_filters(line)

    async def on_mount(self) -> None:
        self.run_worker(self.read_lines(), exclusive=True)
