from autodi import Container, inject

container = Container()


class Database:
    def get_data(self):
        return ["data1", "data2"]


@inject(container)
class DataService:
    def __init__(self, db: Database):
        self.db = db

    def fetch_data(self):
        return self.db.get_data()


service = container.resolve(DataService)
print(service.fetch_data())  # ['data1', 'data2']
