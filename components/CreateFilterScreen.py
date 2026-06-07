from textual.app import ComposeResult
from textual.screen import Screen, ModalScreen
from textual.containers import Grid
from textual.widgets import Label, Input, Footer, Static
from objects.Filter import Filter
from resource_path import resource_path

class CreateFilterScreen(ModalScreen[Filter]):

    CSS_PATH = resource_path("tcss/createfilter.tcss")
    BINDINGS = [
        ("escape", "app.pop_screen", "Cancel"),
        ("ctrl+s", "submit", "Save Filter"),
    ]

    def __init__(self, supplied_filter: Filter | None = None): 
        super().__init__()
        self.filter_name = getattr(supplied_filter, 'name', None) 
        self.regex = getattr(supplied_filter, 'regex_string', None) 

    
    def compose(self) -> ComposeResult:
        yield Grid(
            Static(classes="full-row"),
            Static(),
            Label("Create New Filter", classes="center-wide"),
            Static(),
            Static(),
            Input(placeholder="Name", id="name", classes="center-wide", value=self.filter_name),
            Static(),
            Static(),
            Input(placeholder="Regex", id="regex", classes="center-wide", value=self.regex),
            Static(),
            Static(classes="full-row"),
        )
        yield Footer()

    def action_submit(self):
        self.dismiss(Filter(self.query_one("#name", Input).value, self.query_one("#regex", Input).value))
