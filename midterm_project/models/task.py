class Task:
    def __init__(self, title, description, assignee, deadline, status="ToDo"):
        self.title = title.strip()
        self.description = description.strip()
        self.assignee = assignee.strip()
        self.deadline = deadline      
        self.status = status