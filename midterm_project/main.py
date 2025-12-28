import datetime
from models import TeamMember, Project, Task
from db import (
    load_data, save_member, save_project, save_task,
    update_task_status, update_task_assignee
)

TODAY = datetime.date.today().strftime("%Y-%m-%d")

team_members, projects = load_data()


def input_non_empty(message):
    text = input(message).strip()
    if text == "":
        return None
    return text


def input_date(message):
    d = input(message).strip()
    if len(d) != 10:
        return None
    return d


def choose_from_list(items, title, show_item_func):
    if not items:
        print("List is empty.")
        return None

    print("\n" + title)
    for i, item in enumerate(items, start=1):
        print(f"{i}. {show_item_func(item)}")

    choice = input("Enter number: ").strip()
    if not choice.isdigit():
        print("Invalid input.")
        return None

    idx = int(choice)
    if idx < 1 or idx > len(items):
        print("Invalid number.")
        return None

    return items[idx - 1]


def find_project_by_name(name):
    for p in projects:
        if p.name == name:
            return p
    return None

#Zeynab Nezami

def main_menu():
    while True:
        print("\n" + "=" * 40)
        print("   PROJECT MANAGEMENT SYSTEM")
        print("=" * 40)
        print("1) Team members")
        print("2) Projects")
        print("3) Tasks")
        print("4) Reports")
        print("5) Exit")

        choice = input("Choose: ").strip()

        if choice == "1":
            team_menu()
        elif choice == "2":
            projects_menu()
        elif choice == "3":
            tasks_menu()
        elif choice == "4":
            reports_menu()
        elif choice == "5":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")


def team_menu():
    while True:
        print("\n--- Team Members ---")
        print("1) Add member")
        print("2) Show members")
        print("3) Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_member()
        elif choice == "2":
            show_members()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def add_member():
    name = input_non_empty("Name: ")
    if name is None:
        print("Name is required.")
        return

    role = input("Role: ").strip()
    if role == "":
        role = "Not specified"

    email = input("Email: ").strip()

    member = TeamMember(name, role, email)
    save_member(member)
    team_members.append(member)

    print("Member added.")


def show_members():
    if not team_members:
        print("No members found.")
        return

    for i, m in enumerate(team_members, start=1):
        print(f"{i}.name: {m.name} |role: {m.role} |email: {m.email}")


def projects_menu():
    while True:
        print("\n--- Projects ---")
        print("1) Create project")
        print("2) Show projects")
        print("3) Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            create_project()
        elif choice == "2":
            show_projects()
        elif choice == "3":
            break
        else:
            print("Invalid choice.")


def create_project():
    if not team_members:
        print("Add a team member first.")
        return

    pname = input_non_empty("Project name: ")
    if pname is None:
        print("Project name is required.")
        return

    desc = input("Description: ").strip()
    if desc == "":
        desc = "(no description)"

    manager = choose_from_list(
        team_members,
        "Select project manager:",
        lambda m: f"{m.name} ({m.role})"
    )
    if manager is None:
        return

    start = input_date("Start date (YYYY-MM-DD): ")
    end = input_date("End date (YYYY-MM-DD): ")
    if start is None or end is None or start > end:
        print("Invalid date.")
        return

    project = Project(pname, desc, manager.name, start, end)
    save_project(project)
    projects.append(project)

    print("Project created.")


def show_projects():
    if not projects:
        print("No projects found.")
        return

    for i, p in enumerate(projects, start=1):
        print(f"{i}.name: {p.name} | Manager: {p.manager}")
        print(f"description:  {p.description}")
        print(f"deadline:  {p.start_date} -> {p.end_date}")

#Narges

def tasks_menu():
    while True:
        print("\n--- Tasks ---")
        print("1) Add task")
        print("2) Change status")
        print("3) Reassign task")
        print("4) Project tasks")
        print("5) Member tasks")
        print("6) Back")

        choice = input("Choose: ").strip()

        if choice == "1":
            add_task()
        elif choice == "2":
            change_task_status()
        elif choice == "3":
            reassign_task()
        elif choice == "4":
            show_tasks_for_project()
        elif choice == "5":
            show_tasks_for_member()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


def add_task():
    project = choose_from_list(projects, "Select project:", lambda p: p.name)
    if project is None:
        return

    title = input_non_empty("Task title: ")
    if title is None:
        print("Task title is required.")
        return

    desc = input("Description: ").strip()
    if desc == "":
        desc = "None"

    assignee = choose_from_list(team_members, "Select assignee:", lambda m: m.name)
    if assignee is None:
        return

    deadline = input_date("Deadline (YYYY-MM-DD): ")
    if deadline is None:
        print("Invalid date.")
        return

    status = input("Status [ToDo]: ").strip()
    if status not in ["ToDo", "In Progress", "Done"]:
        status = "ToDo"

    task = Task(title, desc, assignee.name, deadline, status)
    save_task(task, project.name)
    project.tasks.append(task)

    print("Task added.")


def pick_task():
    project = choose_from_list(projects, "Select project:", lambda p: p.name)
    if project is None or not project.tasks:
        return None, None

    task = choose_from_list(
        project.tasks,
        "Select task:",
        lambda t: f"title: {t.title} |assignee: {t.assignee} |status: {t.status}"
    )
    return project, task


def change_task_status():
    project, task = pick_task()
    if project is None:
        return

    status = input("New status: ToDo, In Progress, Done ").strip()
    if status not in ["ToDo", "In Progress", "Done"]:
        print("Invalid status.")
        return

    task.status = status
    update_task_status(project.name, task.title, status)

    print("Status updated.")


def reassign_task():
    project, task = pick_task()
    if project is None:
        return

    member = choose_from_list(team_members, "Select new assignee:", lambda m: m.name)
    if member is None:
        return

    task.assignee = member.name
    update_task_assignee(project.name, task.title, member.name)

    print("Task reassigned.")


def show_tasks_for_project():
    project = choose_from_list(projects, "Select project:", lambda p: p.name)
    if project is None:
        return

    if not project.tasks:
        print("No tasks found.")
        return

    for t in project.tasks:
        print(f"title: {t.title} |assignee: {t.assignee} |deadline: {t.deadline} |status: {t.status}")


def show_tasks_for_member():
    member = choose_from_list(team_members, "Select member:", lambda m: m.name)
    if member is None:
        return

    found = False
    for p in projects:
        for t in p.tasks:
            if t.assignee == member.name:
                print(f"[project name: {p.name}] task title: {t.title} |task deadline: {t.deadline} |task status: {t.status}")
                found = True

    if not found:
        print("No tasks found.")

#Setayesh Mokhtari
 
def reports_menu():
    while True:
        print("\n--- Reports ---")
        print("1) Overdue task")
        print("2) About Members")
        print("3) Projects status")
        print("4) Upcoming task")
        print("5) print report")
        print("6) Back")

        choice = input("Choose: ").strip()   #حذف فاصله ها با استریپ

        if choice == "1":
            overdue_task()
        elif choice =="2":
            About_members()
        elif choice == "3":
            Projects_status()
        elif choice == "4":
            Upcoming_task()
        elif choice =="5":
            print_report()
        elif choice == "6":
            break
        else:
            print("Invalid choice.")


def overdue_task():  #گزارش تسک های عقب مانده
    found = False
    for p in projects:
        for t in p.tasks:
            if t.deadline <TODAY and t.status !="Done":
                print(f"project name:{p.name} -> task title: {t.title} (deadline: {t.deadline})")
                found = True
    if not found:
        print("No overdue tasks.")


def About_members(): #اطلاعات ممبر
    member = choose_from_list(team_members, "Select member:", lambda m: m.name) #خط ۲۷ تیم ممبرز
    if member is None:
        return

    todo=0
    inprog=0
    done=0
    for p in projects:
        for t in p.tasks:
            if t.assignee ==member.name:
                if t.status == "ToDo":
                    todo += 1
                elif t.status == "In Progress":
                    inprog += 1
                else:
                    done += 1

    print(f"ToDo:{todo}, task In Progress:{inprog}, Done:{done}")




def Projects_status():
    for p in projects:
        total =len(p.tasks)
        done = 0
        for t in p.tasks:
            if t.status =="Done":
                done +=1

        print(f"{p.name}:\n done: {done} \n total:{total}")


def Upcoming_task():
    today = datetime.date.today()
    limit = today + datetime.timedelta(days=3)

    found = False
    for p in projects:
        for t in p.tasks:
            if today <= t.deadline <= limit and t.status != "Done":
                print(f"name: {p.name} , \ntitle of project: {t.title} , \ndeadline:{t.deadline}")
                found = True

    if not found:
        print("no tasks to do between these dates.")



def print_report():
    with open("report.txt", "w", encoding="utf-8") as f: #انکدینگ برای ساپورت کردن هرنوع تکستی
        f.write(f"Report for this date {TODAY}\n\n")
        for p in projects:
            total = len(p.tasks)
            done = sum(1 for t in p.tasks if t.status == "Done")
            f.write(f"{p.name}:\n done: {done} \n total:{total}")

    print("report is saved.")

main_menu()
