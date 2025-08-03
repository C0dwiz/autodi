# 🛠️ Contributing to AutoDI

We welcome contributions from the community! Here's how you can help improve AutoDI.

## 🚀 First-Time Contributors

Start with these **good first issues**:
```bash
git clone https://github.com/C0dwiz/autodi.git
cd autodi
pip install -e .[dev]
```

### Recommended Workflow
1. Fork the repository
2. Create a feature branch (`git checkout -b feature/your-feature`)
3. Commit your changes (`git commit -am 'Add some feature'`)
4. Push to the branch (`git push origin feature/your-feature`)
5. Open a Pull Request

## 🧪 Testing Standards

### Running Tests
```bash
pytest tests/ --cov=autodi --cov-report=html
```

### Test Coverage
- Maintain ≥90% coverage for new code
- Include both unit and integration tests
- Mark slow tests with `@pytest.mark.slow`

## 📝 Code Style Guide

### General Rules
- Follow [PEP 8](https://peps.python.org/pep-0008/) with Black formatting
- Type hint all public APIs
- Keep functions under 25 lines
- Document all public methods with Google-style docstrings

### Example Contribution
```python
def register(
    self,
    interface: Type[T],
    implementation: Optional[InjectionTarget[T]] = None,
    *,
    is_singleton: bool = False
) -> None:
    """Registers a dependency in the container.

    Args:
        interface: Abstract type to register
        implementation: Concrete implementation (defaults to interface)
        is_singleton: Whether to reuse instances

    Raises:
        ConfigurationError: If invalid types are provided
    """
    ...
```

## 🐛 Issue Reporting

### Bug Report Template
```markdown
## Description
[Clearly describe the issue]

## Reproduction Steps
1. ...
2. ...
3. ...

## Expected vs Actual
- Expected: [expected behavior]
- Actual: [observed behavior]

## Environment
- AutoDI version: [version]
- Python version: [version]
- OS: [e.g. Windows/Linux/macOS]
```

## 🎁 Feature Proposals

### Proposal Structure
1. **Use Case**: Real-world scenario
2. **API Design**: Proposed interface
3. **Alternatives**: Other approaches considered
4. **Performance Impact**: Benchmarks if applicable

## 🏷️ Release Process

### Versioning Scheme
- `MAJOR`: Breaking changes
- `MINOR`: Backwards-compatible features
- `PATCH`: Backwards-compatible fixes

### Cutting a Release
1. Update `__version__` in `__init__.py`
2. Update CHANGELOG.md
3. Tag the release (`git tag v1.2.3`)
4. Push tags (`git push --tags`)

## 💬 Community

Join our discussion channels:
- [GitHub Discussions](https://github.com/yourusername/autodi/discussions)
- Discord: [#autodi](https://discord.gg/invitecode)

[← Back to Documentation](README.md)