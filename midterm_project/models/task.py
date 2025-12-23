class Task:
    def __init__(self, title, description, assignee, deadline, status="ToDo"):
        self.title = title
        self.description = description
        self.assignee = assignee
        self.deadline = deadline
        self.status = status

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "assignee": self.assignee,
            "deadline": self.deadline,
            "status": self.status
        }