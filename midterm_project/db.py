from pymongo import MongoClient
from models import TeamMember, Project, Task

# ←←← لینک MongoDB خودت رو اینجا عوض کن ←←←
MONGO_URI = "mongodb+srv://<username>:<password>@cluster0.xxxxx.mongodb.net/"  # یا "mongodb://localhost:27017/"

client = MongoClient(MONGO_URI)
db = client["project_db"]
members_col = db["members"]
projects_col = db["projects"]
tasks_col = db["tasks"]

def load_data():
    members = []
    projects = []

    # لود اعضا
    for doc in members_col.find({}, {"_id": 0}):
        members.append(TeamMember(doc["name"], doc["role"], doc["email"]))

    # لود پروژه‌ها
    for proj_doc in projects_col.find({}, {"_id": 0}):
        proj = Project(
            proj_doc["name"],
            proj_doc["description"],
            proj_doc["manager"],
            proj_doc["start_date"],
            proj_doc["end_date"]
        )
        # لود تسک‌ها
        for task_doc in tasks_col.find({"project_name": proj.name}, {"_id": 0}):
            task = Task(
                task_doc["title"],
                task_doc["description"],
                task_doc["assignee"],
                task_doc["deadline"],
                task_doc.get("status", "ToDo")
            )
            proj.tasks.append(task)
        projects.append(proj)

    return members, projects

def save_member(member: TeamMember):
    members_col.insert_one(member.to_dict())

def save_project(project: Project):
    projects_col.insert_one(project.to_dict())

def save_task(task: Task, project_name: str):
    task_dict = task.to_dict()
    task_dict["project_name"] = project_name
    tasks_col.insert_one(task_dict)

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