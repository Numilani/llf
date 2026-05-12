from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, SelectionList
from textual.reactive import reactive
from textual.suggester import Suggester, SuggestFromList

from components.FileLog import FileLog
from components.CreateFilterScreen import CreateFilterScreen
from components.SelectFiltersScreen import SelectFiltersScreen
from components.LayoutTest import LayoutTest


class llfApp(App):
    log_lines: reactive[list[str]] = reactive([])

    CSS_PATH = "style.tcss"
    BINDINGS = [
        ("n", "new_filter", "Create New Filter"),
        ("f", "select_filters", "Toggle Filters"),
        ("t", "test_layout", "(DBG) test layout"),
    ]

    def __init__(self, filename: str) -> None:
        super().__init__()
        self.filename = filename
        self.filters: list[tuple[str, str, bool]] = []

    def compose(self) -> ComposeResult:
        yield Header()
        yield FileLog(self.filename)
        yield Footer()

    # def on_input_submitted(self, event: Input.Submitted):
    #     self.query_one(FileLog).write_line(event.value)

    def action_new_filter(self) -> None:
        def add_filter(filter: tuple[str, str, bool]) -> None:
            self.filters.append(filter)

        self.push_screen(CreateFilterScreen(), add_filter)

    def action_select_filters(self) -> None:
        def update_active_filters(filters: list[tuple[str, str, bool]]) -> None:
            self.filters = filters

        self.push_screen(SelectFiltersScreen(self.filters), update_active_filters)

    def action_test_layout(self) -> None:
        self.push_screen(LayoutTest())
