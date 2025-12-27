from pymongo import MongoClient
from datetime import date
from models import TeamMember, Project, Task

MONGO_URI = "mongodb+srv://hadisea82:jwtDaLN2SUBpKLt@cluster0.vmincra.mongodb.net/" 

client = MongoClient(MONGO_URI)
db = client["project_db"]            
members_col = db["members"]
projects_col = db["projects"]
tasks_col = db["tasks"]

def load_data():
    """
    همه داده‌ها رو از MongoDB لود می‌کنه و به صورت شیءهای مدل برمی‌گردونه
    """
    members = []
    projects = []

    # لود اعضای تیم
    for doc in members_col.find({}, {"_id": 0}):
        members.append(TeamMember(
            name=doc["name"],
            role=doc["role"],
            email=doc["email"]
        ))

    # لود پروژه‌ها
    for proj_doc in projects_col.find({}, {"_id": 0}):
        project = Project(
            name=proj_doc["name"],
            description=proj_doc["description"],
            manager=proj_doc["manager"],
            start_date=date.fromisoformat(proj_doc["start_date"]),
            end_date=date.fromisoformat(proj_doc["end_date"])
        )

        # لود تسک‌های مربوط به این پروژه
        for task_doc in tasks_col.find({"project_name": project.name}, {"_id": 0}):
            task = Task(
                title=task_doc["title"],
                description=task_doc["description"],
                assignee=task_doc["assignee"],
                deadline=date.fromisoformat(task_doc["deadline"]),
                status=task_doc.get("status", "ToDo")
            )
            project.tasks.append(task)

        projects.append(project)

    return members, projects

def save_member(member: TeamMember):
    """عضو جدید رو در دیتابیس ذخیره می‌کنه"""
    members_col.insert_one(member.to_dict())

def save_project(project: Project):
    """پروژه جدید رو در دیتابیس ذخیره می‌کنه"""
    projects_col.insert_one({
        "name": project.name,
        "description": project.description,
        "manager": project.manager,
        "start_date": project.start_date.isoformat(),
        "end_date": project.end_date.isoformat()
    })

def save_task(task: Task, project_name: str):
    """تسک جدید رو در دیتابیس ذخیره می‌کنه"""
    tasks_col.insert_one({
        "project_name": project_name,
        "title": task.title,
        "description": task.description,
        "assignee": task.assignee,
        "deadline": task.deadline.isoformat(),
        "status": task.status
    })

def update_task_status(project_name: str, task_title: str, new_status: str):
    """وضعیت یک تسک رو آپدیت می‌کنه"""
    tasks_col.update_one(
        {"project_name": project_name, "title": task_title},
        {"$set": {"status": new_status}}
    )

def update_task_assignee(project_name: str, task_title: str, new_assignee: str):
    """مسئول یک تسک رو تغییر می‌ده"""
    tasks_col.update_one(
        {"project_name": project_name, "title": task_title},
        {"$set": {"assignee": new_assignee}}
    )
