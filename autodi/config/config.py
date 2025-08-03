from typing import Type
import yaml
from pathlib import Path


class DIConfig:
    def __init__(self, container):
        self._container = container

    def load_from_yaml(self, file_path: str) -> None:
        config = yaml.safe_load(Path(file_path).read_text())

        for interface, params in config.get("dependencies", {}).items():
            impl = self._import_class(params["implementation"])
            self._container.register(
                interface=self._import_class(interface),
                implementation=impl,
                is_singleton=params.get("singleton", False),
            )

    def _import_class(self, class_path: str) -> Type:
        module_path, class_name = class_path.rsplit(".", 1)
        module = __import__(module_path, fromlist=[class_name])
        return getattr(module, class_name)
