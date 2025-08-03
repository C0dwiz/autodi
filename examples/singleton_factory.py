from autodi import Container, inject

container = Container()


@inject(container, is_singleton=True)
class ConfigService:
    def __init__(self):
        self.theme = "dark"
        self.debug = True


def create_connection():
    return {"status": "connected"}


container.register(dict, create_connection)

config1 = container.resolve(ConfigService)
config2 = container.resolve(ConfigService)
print(config1 is config2)  # True

connection = container.resolve(dict)
print(connection)  # {'status': 'connected'}
