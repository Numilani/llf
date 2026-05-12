from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Grid
from textual.widgets import Label, Input, Footer


class CreateFilterScreen(Screen):

    BINDINGS = [
        ("escape", "app.pop_screen", "Cancel"),
        ("ctrl+s", "submit", "Save Filter"),
    ]

    def compose(self) -> ComposeResult:
        yield Grid(Label("Create New Filter"), Input(placeholder="Name", id="name"), Input(placeholder="Regex", id="regex"))
        yield Footer()

    def action_submit(self):
        self.dismiss((self.query_one("#name", Input).value, self.query_one("#regex", Input).value))
