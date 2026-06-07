from textual.app import ComposeResult
from textual.screen import Screen, ModalScreen
from textual.containers import Grid
from textual.widgets import Label, Input, Footer, Static, Button
from objects.Filter import Filter
from resource_path import resource_path

class ConfirmDelete(ModalScreen[str]):

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
            Label("Are you sure you wish to delete this filter?", classes="center-wide"),
            Static(),
            Static(),
            Button.success(label="Yes", id="yes"),
            Button.error(label="No", id="no"),
            Static(),
            Static(),
            Static(),
            Static(classes="full-row"),
        )
        yield Footer()

    def on_button_pressed(self, event: Button.Pressed) -> None:
        self.dismiss(str(event.button.label))

