class Project:
    def __init__(self, name, description, manager, start_date, end_date):
        self.name = name.strip()
        self.description = description.strip()
        self.manager = manager.strip()
        self.start_date = start_date  
        self.end_date = end_date      
        self.tasks = []