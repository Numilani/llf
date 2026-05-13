from uuid import UUID

from textual.app import ComposeResult
from textual.screen import Screen, ModalScreen
from textual.containers import Grid
from textual.message import Message
from textual.widgets import Label, SelectionList, Footer

from objects.Filter import Filter
from config import Config
from components.CreateFilterScreen import CreateFilterScreen


class SelectFiltersScreen(ModalScreen[list[UUID]]):
    class EditFilterRequest(Message):
        def __init__(self, uuid) -> None:
            super().__init__()
            self.uuid = uuid

    class DeleteFilterRequest(Message):
        def __init__(self, uuid) -> None:
            super().__init__()
            self.uuid = uuid

    CSS_PATH = "modal.tcss"
    BINDINGS = [
        ("escape", "app.pop_screen", "Back"),
        ("ctrl+s", "save", "Save Filters"),
        ("delete", "delete", "Delete Filter"),
        ("ctrl+e", "edit", "Edit Filter"),
    ]

    def __init__(self, options: list[tuple[str, UUID, bool]], cfg: Config):
        super().__init__()
        self.options = options
        self.app_config = cfg

    def compose(self) -> ComposeResult:
        yield Grid(Label("Select Active Filters:"), SelectionList[UUID](*self.options))
        yield Footer()

    def action_save(self):
        self.dismiss(self.query_one(SelectionList).selected)

    def action_edit(self):
        list = self.query_one(SelectionList)
        if list.highlighted is None:
            raise RuntimeError("should be unreachable")
        option = list.get_option_at_index(list.highlighted)
        self.post_message(SelectFiltersScreen.EditFilterRequest(option.value))

    def action_delete(self):
        list = self.query_one(SelectionList)
        if list.highlighted is None:
            raise RuntimeError("should be unreachable")
        option = list.get_option_at_index(list.highlighted)
        self.post_message(SelectFiltersScreen.DeleteFilterRequest(option.value))
