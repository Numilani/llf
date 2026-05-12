from uuid import UUID

from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Grid
from textual.widgets import Label, SelectionList, Footer


class SelectFiltersScreen(Screen[list[UUID]]):

    CSS_PATH = "modal.tcss"
    BINDINGS = [
        ("escape", "", "Back"),
        ("ctrl+s", "save", "Save Filters"),
    ]

    def __init__(self, options):
        super().__init__()
        self.options = options

    def compose(self) -> ComposeResult:
        yield Grid(Label("Select Active Filters:"), SelectionList[UUID](*self.options))
        yield Footer()

    def action_save(self):
        self.dismiss(self.query_one(SelectionList).selected)
