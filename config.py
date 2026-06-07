import json
import os
from objects.Filter import Filter
from typing import Self


class Config:
    filters: list[Filter]

    def to_dict(self):
        return {"filters": [f.to_dict() for f in self.filters]}

    @classmethod
    def from_dict(cls, d: dict) -> Self:
        c = Config()
        c.filters = [Filter.from_dict(f) for f in d["filters"]]
        return c


# helper methods
def read_config() -> Self:
    candidates = [
        os.path.join(os.getcwd(), ".llfrc"),
        os.path.join(os.path.expanduser("~"), ".llfrc"),
    ]
    found = False
    for path in candidates:
        if os.path.isfile(path):
            found = True
            with open(path, "r") as f:
                return Config.from_dict(json.load(f))
    if not found:
        write_blank_config(os.path.join(os.path.expanduser("~"), ".llfrc"))
        with open(os.path.join(os.path.expanduser("~"), ".llfrc")) as f:
            return Config.from_dict(json.load(f))
    raise RuntimeError("unreachable")  # this is so dumb


def update_config(config):
    candidates = [
        os.path.join(os.getcwd(), ".llfrc"),
        os.path.join(os.path.expanduser("~"), ".llfrc"),
    ]
    found = False
    for path in candidates:
        if os.path.isfile(path):
            found = True
            with open(path, "w") as f:
                json.dump(config.to_dict(), f)


def write_blank_config(path) -> None:
    with open(path, "x") as file:
        cfg = Config()
        cfg.filters = [Filter("allow-all", ".*")]
        json.dump(cfg.to_dict(), file)
