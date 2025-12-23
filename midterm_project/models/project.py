class Project:
    def __init__(self, name, description, manager, start_date, end_date):
        self.name = name
        self.description = description
        self.manager = manager
        self.start_date = start_date
        self.end_date = end_date
        self.tasks = []

    def to_dict(self):
        return {
            "name": self.name,
            "description": self.description,
            "manager": self.manager,
            "start_date": self.start_date,
            "end_date": self.end_date
        }