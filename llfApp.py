from uuid import UUID

from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, SelectionList
from textual.reactive import reactive
from textual.suggester import Suggester, SuggestFromList

from components.FileLog import FileLog
from components.CreateFilterScreen import CreateFilterScreen
from components.SelectFiltersScreen import SelectFiltersScreen
from components.LayoutTest import LayoutTest
from objects.Filter import Filter
import uuid
import os
import json

import config
from config import Config


class llfApp(App):

    CSS_PATH = "style.tcss"
    BINDINGS = [
        ("n", "new_filter", "Create New Filter"),
        ("f", "select_filters", "Toggle Filters"),
        # ("t", "test_layout", "(DBG) test layout"),
    ]

    def __init__(self, filename: str) -> None:
        super().__init__()
        self.filename = filename
        self.config: Config = config.read_config()
        self.filters: list[Filter] = self.config.filters

    def compose(self) -> ComposeResult:
        yield Header()
        yield FileLog(self.filename)
        yield Footer()
    
    # def on_input_submitted(self, event: Input.Submitted):
    #     self.query_one(FileLog).write_line(event.value)

    def action_new_filter(self) -> None:
        def add_filter(filter: Filter) -> None:
            self.filters.append(filter)
            config.update_config(self.config)

        self.push_screen(CreateFilterScreen(), add_filter)  # type: ignore[call-overload]

    def action_select_filters(self) -> None:
        def update_active_filters(filters: list[UUID]) -> None:
            for f in self.filters:
                f.enabled = f.uuid in filters
            active_filters = [filter for filter in self.filters if filter.enabled]
            self.query_one(FileLog).filters = active_filters
            self.query_one(FileLog).refilter_log()

        options = []
        for f in self.filters:
            options.append((f.name, f.uuid, f.enabled))
        self.push_screen(SelectFiltersScreen(options), update_active_filters)  # type: ignore[call-overload]

    # def action_test_layout(self) -> None:
    #     self.push_screen(LayoutTest())
