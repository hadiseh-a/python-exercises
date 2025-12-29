from pymongo import MongoClient
from models import TeamMember, Project, Task

MONGO_URI = "mongodb+srv://hadisea82:jwtDaLN2SUBpKLt@cluster0.vmincra.mongodb.net/" 

client = MongoClient(MONGO_URI)
db = client["midterm_project"]
members_col = db["members"]
projects_col = db["projects"]
tasks_col = db["tasks"]


def load_data():
    members = []
    projects = []
    tasks=[]

    for doc in members_col.find():
        members.append(TeamMember(
            name=doc["name"],
            role=doc["role"],
            email=doc["email"]
        ))

    for proj_doc in projects_col.find():
        project = Project(
            name=proj_doc["name"],
            description=proj_doc["description"],
            manager=proj_doc["manager"],
            start_date=proj_doc["start_date"],   
            end_date=proj_doc["end_date"]      
        )

        for task_doc in tasks_col.find({"project_name": project.name}):
            task = Task(
                title=task_doc["title"],
                description=task_doc["description"],
                assignee=task_doc["assignee"],
                deadline=task_doc["deadline"],
                status=task_doc.get("status", "ToDo")
            )
            project.tasks.append(task)
            tasks.append(task)

        projects.append(project)

    return members, projects,tasks


def save_member(member: TeamMember):
    members_col.insert_one({
        "name": member.name,
        "role":member.role,
        "email": member.email
        })


def save_project(project: Project):
    projects_col.insert_one({
        "name": project.name,
        "description": project.description,
        "manager": project.manager,
        "start_date": project.start_date,
        "end_date": project.end_date
    })


def save_task(task: Task, project_name: str):
    tasks_col.insert_one({
        "project_name": project_name,
        "title": task.title,
        "description": task.description,
        "assignee": task.assignee,
        "deadline": task.deadline,
        "status": task.status
    })


def update_task_status(project_name: str, task_title: str, new_status: str):
    tasks_col.update_one(
        {"project_name": project_name, "title": task_title},
        {"$set": {"status": new_status}}
    )


def update_task_assignee(project_name: str, task_title: str, new_assignee: str):
    tasks_col.update_one(
        {"project_name": project_name, "title": task_title},
        {"$set": {"assignee": new_assignee}}
    )