from __future__ import annotations
from importlib import import_module
from pathlib import Path
from typing import Type, Any

import yaml

from ..scopes import Scope


class DIConfig:
    """Loads dependency configurations from a YAML file."""

    def __init__(self, container: Any):
        """Initializes the DIConfig.

        Args:
            container: The container instance to register dependencies with.
        """
        self._container = container

    def load_from_yaml(self, file_path: str | Path) -> None:
        """Loads and registers dependencies from a YAML configuration file.

        Args:
            file_path: The path to the YAML file.

        Raises:
            FileNotFoundError: If the configuration file does not exist.
            ValueError: If the YAML file is malformed or contains errors.
        """
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found at: {path}")

        try:
            config = yaml.safe_load(path.read_text())
        except yaml.YAMLError as e:
            raise ValueError(f"Failed to parse YAML file: {e}") from e

        if not isinstance(config, dict) or "dependencies" not in config:
            return

        for interface_path, params in config["dependencies"].items():
            try:
                interface = self._import_class(interface_path)
                implementation_path = params.get("implementation")
                implementation = (
                    self._import_class(implementation_path)
                    if implementation_path
                    else None
                )

                self._container.register(
                    interface=interface,
                    implementation=implementation,
                    scope=params.get("scope", Scope.APP),
                    init_hook=params.get("init_hook"),
                    destroy_hook=params.get("destroy_hook"),
                )
            except (KeyError, ImportError, TypeError) as e:
                raise ValueError(
                    f"Error processing dependency '{interface_path}': {e}"
                ) from e

    def _import_class(self, class_path: str) -> Type[Any]:
        """Dynamically imports a class from a string path.

        Args:
            class_path: The full path to the class (e.g., 'my_module.MyClass').

        Returns:
            The imported class.

        Raises:
            ImportError: If the class cannot be imported.
        """
        try:
            module_path, class_name = class_path.rsplit(".", 1)
            module = import_module(module_path)
            return getattr(module, class_name)
        except (ImportError, AttributeError, ValueError) as e:
            raise ImportError(f"Failed to import class '{class_path}': {e}") from e
