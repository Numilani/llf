from textual.app import ComposeResult
from textual.screen import Screen
from textual.containers import Grid
from textual.widgets import Label, Input, Footer, Static


class CreateFilterScreen(Screen):

    CSS_PATH = "createfilter.tcss"
    BINDINGS = [
        ("escape", "app.pop_screen", "Cancel"),
        ("ctrl+s", "submit", "Save Filter"),
    ]
    
    def compose(self) -> ComposeResult:
        yield Grid(
            Static(classes="full-row"),
            Static(),
            Label("Create New Filter", classes="center-wide"),
            Static(),
            Static(),
            Input(placeholder="Name", id="name", classes="center-wide"),
            Static(),
            Static(),
            Input(placeholder="Regex", id="regex", classes="center-wide"),
            Static(),
            Static(classes="full-row"),
        )
        yield Footer()

    def action_submit(self):
        self.dismiss((self.query_one("#name", Input).value, self.query_one("#regex", Input).value, False))
