from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Grid
from textual.widgets import Label, SelectionList, Footer, Static
from resource_path import resource_path

class LayoutTest(Screen):
    CSS_PATH = resource_path("tcss/modal.tcss")
    BINDINGS = [
        ("escape", "", "Back"),
        ("ctrl+s", "save", "Save Filters"),
    ]

    def compose(self) -> ComposeResult:
        yield Grid(
            Static(classes="full-row"),
            Static(),
            Static(classes="center-wide test-box"),
            Static(),
            Static(),
            Static(classes="test-box"),
            Static(classes="test-box"),
            Static(),
            Static(classes="full-row")
        )
        yield Footer()
