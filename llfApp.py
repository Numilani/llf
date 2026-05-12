from textual.app import App, ComposeResult
from textual.widgets import Footer, Header, Input, SelectionList
from textual.reactive import reactive
from textual.suggester import Suggester, SuggestFromList

from components.FileLog import FileLog
from components.CreateFilterScreen import CreateFilterScreen
from components.SelectFiltersScreen import SelectFiltersScreen


class llfApp(App):
    log_lines: reactive[list[str]] = reactive([])

    CSS_PATH = "style.tcss"
    BINDINGS = [
        ('n', 'new_filter', "Create New Filter"),
        ('f', 'select_filters', "Toggle Filters")
                ]

    def __init__(self, filename) -> None:
        super().__init__()
        self.filename = filename

    def compose(self) -> ComposeResult:
        yield Header()
        yield FileLog(self.filename)
        yield Footer()

    # def on_input_submitted(self, event: Input.Submitted):
    #     self.query_one(FileLog).write_line(event.value)

    def action_new_filter(self) -> None:
        self.push_screen(CreateFilterScreen())

    def action_select_filters(self) -> None:
        self.push_screen(SelectFiltersScreen())


