# Hi, this is a project management and task system for the programming exercise.
# I tried to keep it simple and use classes to organize it.
# Using lists to store data.
# Handling dates with datetime.

import datetime
import sys

# Class for team member
class TeamMember:
    def __init__(self, name, role, email):
        self.name = name
        self.role = role
        self.email = email

# Class for project
class Project:
    def __init__(self, name, description, manager, start_date, end_date):
        self.name = name
        self.description = description
        self.manager = manager  # Should be the name of a team member
        self.start_date = start_date  # datetime.date
        self.end_date = end_date
        self.tasks = []  # List of tasks for this project

# Class for task
class Task:
    def __init__(self, title, description, assignee, deadline, status="ToDo"):
        self.title = title
        self.description = description
        self.assignee = assignee  # Name of team member
        self.deadline = deadline  # datetime.date
        self.status = status  # "ToDo", "In Progress", "Done"

# Main lists
team_members = []  # List of team members
projects = []  # List of projects

# Function for main menu
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1. Team Member Management")
        print("2. Project Management")
        print("3. Task Management")
        print("4. Reports")
        print("5. Exit")
        choice = input("Choose: ")
        
        if choice == "1":
            team_management_menu()
        elif choice == "2":
            projects_management_menu()
        elif choice == "3":
            task_management()
        elif choice == "4":
            reports()
        elif choice == "5":
            sys.exit("Goodbye!")
        else:
            print("Invalid choice!")

# Team management
def team_management_menu():
    while True:
        print("\n--- Team Management ---")
        print("1. Add member")
        print("2. Display all members")
        print("3. Back to main menu")
        choice = input("Enter: ").strip()

        if choice == '1':
            add_team_member()
        elif choice == '2':
            display_team_members()
        elif choice == '3':
            break
        else:
            print("Invalid choice")

def add_team_member():
    print("\n--- Add Team Member ---")
    name = input("Name: ").strip()
    role = input("Role: ").strip()
    email = input("Email: ").strip()

    team_members.append(TeamMember(name, role, email))
    print("Member added successfully!")

def display_team_members():
    print("\n--- List of Team Members ---")
    if not team_members:
        print("No members yet.")
        return
    for idx, member in enumerate(team_members, start=1):
        print(f"{idx}. Name: {member.name}")
        print(f"   Role: {member.role}")
        print(f"   Email: {member.email}")
        print("   " + "-"*20)

def projects_management_menu():
    while True:
        print("\n--- Project Management ---")
        print("1. Create new project")
        print("2. Display all projects")
        print("3. Back to main menu")
        choice = input("Enter: ").strip()

        if choice == '1':
            add_project()
        elif choice == '2':
            display_projects()
        elif choice == '3':
            break
        else:
            print("Invalid choice")

def add_project():
    print("\n--- Create New Project ---")
    name = input("Project name: ").strip()
    description = input("Description: ").strip()

    if not team_members:
        print("Error: You must add at least one team member first!")
        return

    print("The manager must be one of these:")
    for idx, member in enumerate(team_members, start=1):
        print(f"   {idx}. {member.name} ({member.role})")

    manager = input("Name of manager: ").strip()

    if not any(member.name == manager for member in team_members):
        print("Manager not found!")
        return

    start_date_str = input("Start date (YYYY-MM-DD): ").strip()
    end_date_str = input("End date (YYYY-MM-DD): ").strip()

    try:
        start_date = datetime.date.fromisoformat(start_date_str)
        end_date = datetime.date.fromisoformat(end_date_str)
        if start_date > end_date:
            print("Start date cannot be after end date!")
            return
    except ValueError:
        print("Invalid date format!")
        return

    projects.append(Project(name, description, manager, start_date, end_date))
    print("Project created successfully!")

def display_projects():
    print("\n--- List of Projects ---")
    if not projects:
        print("No projects yet.")
        return

    for idx, project in enumerate(projects, start=1):
        print(f"{idx}. Project name: {project.name}")
        print(f"   Description: {project.description}")
        print(f"   Manager: {project.manager}")
        print(f"   Start date: {project.start_date}")
        print(f"   End date: {project.end_date}")
        print("   " + "-"*30)

# Task management
def task_management():
    while True:
        print("\nTask Management:")
        print("1. Create New Task")
        print("2. Change Task Status")
        print("3. Change Task Assignee")
        print("4. Display Tasks for a Project")
        print("5. Display Tasks for a Member")
        print("6. Back")
        choice = input("Choose: ")
        
        if choice == "1":
            proj_name = input("Project Name: ")
            proj = next((p for p in projects if p.name == proj_name), None)
            if not proj:
                print("Project not found!")
                continue
            title = input("Task Title: ")
            description = input("Short Description: ")
            assignee = input("Assignee (Member Name): ")
            if not any(m.name == assignee for m in team_members):
                print("Member not found!")
                continue
            deadline_str = input("Deadline (YYYY-MM-DD): ")
            try:
                deadline = datetime.date.fromisoformat(deadline_str)
            except ValueError:
                print("Invalid date!")
                continue
            status = input("Status (ToDo/In Progress/Done): ") or "ToDo"
            if status not in ["ToDo", "In Progress", "Done"]:
                print("Invalid status!")
                continue
            task = Task(title, description, assignee, deadline, status)
            proj.tasks.append(task)
            print("Task created.")
        elif choice == "2":
            proj_name = input("Project Name: ")
            proj = next((p for p in projects if p.name == proj_name), None)
            if not proj:
                print("Project not found!")
                continue
            title = input("Task Title: ")
            task = next((t for t in proj.tasks if t.title == title), None)
            if not task:
                print("Task not found!")
                continue
            new_status = input("New Status (ToDo/In Progress/Done): ")
            if new_status in ["ToDo", "In Progress", "Done"]:
                task.status = new_status
                print("Status changed.")
            else:
                print("Invalid status!")
        elif choice == "3":
            proj_name = input("Project Name: ")
            proj = next((p for p in projects if p.name == proj_name), None)
            if not proj:
                print("Project not found!")
                continue
            title = input("Task Title: ")
            task = next((t for t in proj.tasks if t.title == title), None)
            if not task:
                print("Task not found!")
                continue
            new_assignee = input("New Assignee (Member Name): ")
            if any(m.name == new_assignee for m in team_members):
                task.assignee = new_assignee
                print("Assignee changed.")
            else:
                print("Member not found!")
        elif choice == "4":
            proj_name = input("Project Name: ")
            proj = next((p for p in projects if p.name == proj_name), None)
            if not proj:
                print("Project not found!")
                continue
            if not proj.tasks:
                print("No tasks.")
            else:
                for task in proj.tasks:
                    print(f"Title: {task.title}, Description: {task.description}, Assignee: {task.assignee}, Deadline: {task.deadline}, Status: {task.status}")
        elif choice == "5":
            member_name = input("Member Name: ")
            found = False
            for proj in projects:
                for task in proj.tasks:
                    if task.assignee == member_name:
                        print(f"Project: {proj.name}, Title: {task.title}, Deadline: {task.deadline}, Status: {task.status}")
                        found = True
            if not found:
                print("No tasks for this member.")
        elif choice == "6":
            return
        else:
            print("Invalid choice!")

# Reports
def reports():
    today = datetime.date.today()
    while True:
        print("\nReports:")
        print("1. Display Overdue Tasks")
        print("2. Display Member Status Summary")
        print("3. Display Project Status Summary")
        print("4. Display Tasks with Near Deadlines")
        print("5. Generate Report File")
        print("6. Back")
        choice = input("Choose: ")
        
        if choice == "1":
            found = False
            for proj in projects:
                for task in proj.tasks:
                    if task.deadline < today and task.status != "Done":
                        print(f"Project: {proj.name}, Title: {task.title}, Assignee: {task.assignee}, Deadline: {task.deadline}")
                        found = True
            if not found:
                print("No overdue tasks.")
        elif choice == "2":
            member_name = input("Member Name: ")
            todo = 0
            in_progress = 0
            done = 0
            for proj in projects:
                for task in proj.tasks:
                    if task.assignee == member_name:
                        if task.status == "ToDo":
                            todo += 1
                        elif task.status == "In Progress":
                            in_progress += 1
                        elif task.status == "Done":
                            done += 1
            print(f"{member_name}: ToDo: {todo}, In Progress: {in_progress}, Done: {done}")
        elif choice == "3":
            for proj in projects:
                todo = sum(1 for t in proj.tasks if t.status == "ToDo")
                in_progress = sum(1 for t in proj.tasks if t.status == "In Progress")
                done = sum(1 for t in proj.tasks if t.status == "Done")
                print(f"Project {proj.name}: ToDo: {todo}, In Progress: {in_progress}, Done: {done}")
        elif choice == "4":
            near_deadline = today + datetime.timedelta(days=3)  # Next 3 days
            found = False
            for proj in projects:
                for task in proj.tasks:
                    if today < task.deadline <= near_deadline and task.status != "Done":
                        print(f"Project: {proj.name}, Title: {task.title}, Assignee: {task.assignee}, Deadline: {task.deadline}")
                        found = True
            if not found:
                print("No tasks with near deadlines.")
        elif choice == "5":
            with open("report.txt", "w", encoding="utf-8") as f:
                f.write("Project Status Summary:\n")
                for proj in projects:
                    todo = sum(1 for t in proj.tasks if t.status == "ToDo")
                    in_progress = sum(1 for t in proj.tasks if t.status == "In Progress")
                    done = sum(1 for t in proj.tasks if t.status == "Done")
                    f.write(f"Project {proj.name}: ToDo: {todo}, In Progress: {in_progress}, Done: {done}\n")
                
                f.write("\nOverdue Tasks List:\n")
                for proj in projects:
                    for task in proj.tasks:
                        if task.deadline < today and task.status != "Done":
                            f.write(f"Project: {proj.name}, Title: {task.title}, Assignee: {task.assignee}, Deadline: {task.deadline}\n")
                
                f.write("\nMember Status:\n")
                for member in team_members:
                    active = 0
                    for proj in projects:
                        for task in proj.tasks:
                            if task.assignee == member.name and task.status != "Done":
                                active += 1
                    f.write(f"{member.name}: Active Tasks: {active}\n")
            print("report.txt file generated successfully.")
        elif choice == "6":
            return
        else:
            print("Invalid choice!")

# Start the program
if __name__ == "__main__":
    main_menu()