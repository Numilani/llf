import asyncio
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

import config
import os
import signal
from config import Config
from components.ConfirmDelete import ConfirmDelete
from resource_path import resource_path
from components.DebugFileLog import DebugFileLog

class llfApp(App):

    REFRESH_RATE = 10
    CSS_PATH = resource_path("tcss/style.tcss")
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
        # yield FileLog(self.filename)
        yield DebugFileLog(self.filename)
        yield Footer()

    # def on_input_submitted(self, event: Input.Submitted):
    #     self.query_one(FileLog).write_line(event.value)

    def action_new_filter(self) -> None:
        def add_filter(filter: Filter) -> None:
            self.filters.append(filter)
            config.update_config(self.config)

        self.push_screen(CreateFilterScreen(None), add_filter)  # type: ignore[call-overload]

    def action_select_filters(self) -> None:
        def update_active_filters(filters: list[UUID]) -> None:
            for f in self.filters:
                f.enabled = f.uuid in filters
            active_filters = [filter for filter in self.filters if filter.enabled]
            # self.query_one(FileLog).filters = active_filters
            # asyncio.ensure_future(self.query_one(FileLog).refilter_log())
            self.query_one(DebugFileLog).filters = active_filters
            asyncio.ensure_future(self.query_one(DebugFileLog).refilter_log())

        options = []
        for f in self.filters:
            options.append((f.name, f.uuid, f.enabled))
        self.push_screen(SelectFiltersScreen(options, self.config), update_active_filters)  # type: ignore[call-overload]

    def on_select_filters_screen_delete_filter_request(self, event: SelectFiltersScreen.DeleteFilterRequest):
        def delete(v: str):
            if v == "No":
                pass
            else:
                target = next((f for f in self.filters if f.uuid == event.uuid), None)
                if target is None:
                    return # maybe throw err msg here? is this even possible?
                else:
                    self.config.filters.remove(target)
                    config.update_config(self.config)
                    self.filters = self.config.filters
            self.action_select_filters()

        self.pop_screen()
        self.push_screen(ConfirmDelete(), delete)  # type: ignore[call-overload]


    def on_select_filters_screen_edit_filter_request(self, event: SelectFiltersScreen.EditFilterRequest):
        def update_filter(filter: Filter):
            target = next((f for f in self.filters if f.uuid == event.uuid), None)
            if target is None:
                return # maybe throw err msg here? is this even possible?
            else:
                filter.uuid = target.uuid
                filter.enabled = False
                self.config.filters.remove(target)
                self.config.filters.append(filter)
                config.update_config(self.config)
                self.filters = self.config.filters
                self.action_select_filters()

        self.pop_screen()
        target = next((f for f in self.filters if f.uuid == event.uuid), None)
        if target is None:
            return # maybe throw err msg here? is this even possible?
        else:
            self.push_screen(CreateFilterScreen(target), update_filter)  # type: ignore[call-overload]

    def on_unmount(self):
        try:
            pgid = os.getpgrp()
            os.killpg(pgid, signal.SIGTERM)
        except:
            pass
        finally:
            self.exit()


    # def action_test_layout(self) -> None:
    #     self.push_screen(LayoutTest())
