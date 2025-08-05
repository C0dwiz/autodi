# 🛠️ Contributing to AutoDI

We welcome contributions from the community! Here's how you can help improve AutoDI.

## 🚀 Getting Started

1.  **Fork the repository** on GitHub.
2.  **Clone your fork** locally:
    ```bash
    git clone https://github.com/YOUR_USERNAME/autodi.git
    cd autodi
    ```
3.  **Install the development dependencies**:
    ```bash
    pip install -e .[dev]
    ```

### Recommended Workflow

1.  Create a feature branch (`git checkout -b feature/your-awesome-feature`).
2.  Make your changes and add tests.
3.  Commit your changes (`git commit -am 'Add some awesome feature'`).
4.  Push to the branch (`git push origin feature/your-awesome-feature`).
5.  Open a Pull Request.

## 🧪 Testing Standards

-   All new features must be accompanied by tests.
-   Run the full test suite to ensure your changes don't break existing functionality.

### Running Tests

```bash
pytest
```

## 📝 Code Style Guide

-   We use **Black** for code formatting. Please run `black .` before committing.
-   All public methods and functions should have **Google-style docstrings**.
-   Use **type hints** for all function signatures.

### Example Contribution

```python
from .scopes import ScopeType

def my_new_function(name: str, scope: ScopeType) -> str:
    """This function does something amazing.

    Args:
        name: The name of the thing.
        scope: The scope to use.

    Returns:
        An amazing string.
    """
    # ... implementation ...
```

## 🐛 Reporting Issues

If you find a bug, please open an issue on GitHub. Include:

-   A clear and concise description of the issue.
-   A minimal, reproducible example.
-   The expected behavior and the actual behavior.
-   Your Python version and `autodi` version.

## 🎁 Proposing Features

We love to hear ideas for new features! Please open an issue to start a discussion. Describe the use case and your proposed API design.

[← Back to Documentation](README.md)
