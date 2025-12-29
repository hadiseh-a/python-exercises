class Task:
    def __init__(self, title, description, assignee, deadline, status="ToDo"):
        self.title = title.strip()
        self.description = description.strip()
        self.assignee = assignee.strip()
        self.deadline = deadline      
        self.status = status

    def change_status(self, new_status):
        self.status = new_status

    def change_assignee(self, new_assignee):
        self.assignee = new_assignee

    def __str__(self):
        return f"{self.title} | {self.description} | {self.assignee} | {self.deadline} | {self.status}"