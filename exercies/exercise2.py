import csv
import os
# Main list of employees
employees = []
# Trash bin for deleted ones
trash_bin = []
# Undo and Redo stacks
undo_stack = []
redo_stack = []
# Function to save current state for Undo
def save_state(action, data=None):
    state = {
        'action': action,
        'employees': employees.copy(),
        'trash_bin': trash_bin.copy(),
        'data': data
    }
    undo_stack.append(state)
    redo_stack.clear() # When a new operation is performed, Redo is cleared
# Undo function
def undo():
    if not undo_stack:
        print("There is no operation to Undo.")
        return
    last_state = undo_stack.pop()
    global employees, trash_bin
    employees = last_state['employees'].copy()
    trash_bin = last_state['trash_bin'].copy()
    redo_stack.append(last_state)
    print("Undo operation performed.")
# Redo function
def redo():
    if not redo_stack:
        print("There is no operation to Redo.")
        return
    next_state = redo_stack.pop()
    global employees, trash_bin
    employees = next_state['employees'].copy()
    trash_bin = next_state['trash_bin'].copy()
    undo_stack.append(next_state)
    print("Redo operation performed.")
# Function to enter information
def add_employee():
    save_state('add') # Save state before adding
    while True:
        emp_id = input("Employee ID (-1 to exit): ")
        if emp_id == '-1':
            break
        name = input("Name: ")
        hours = float(input("Monthly working hours: "))
        rate = float(input("Hourly rate: "))
        employee = {'id': emp_id, 'name': name, 'hours': hours, 'rate': rate}
        employees.append(employee)
        print("Information added.")
# Function to display information
def display_employees(search_term=None):
    if not employees:
        print("No employees exist.")
        return []
    filtered = []
    for i, emp in enumerate(employees):
        if search_term is None or search_term in emp['id'] or search_term.lower() in emp['name'].lower():
            filtered.append((i, emp))
    if not filtered:
        print("No results found.")
        return []
    for idx, (i, emp) in enumerate(filtered):
        print(f"{idx}: Employee ID: {emp['id']}, Name: {emp['name']}, Hours: {emp['hours']}, Rate: {emp['rate']}")
    return filtered
# Function to edit information
def edit_employee():
    search = input("Employee ID or part of name for search: ")
    filtered = display_employees(search)
    if not filtered:
        return
    row_num = int(input("Row number to edit: "))
    if 0 <= row_num < len(filtered):
        i, emp = filtered[row_num]
        print("Edit information:")
        emp['id'] = input(f"New Employee ID ({emp['id']}): ") or emp['id']
        emp['name'] = input(f"New Name ({emp['name']}): ") or emp['name']
        emp['hours'] = float(input(f"New Hours ({emp['hours']}): ") or emp['hours'])
        emp['rate'] = float(input(f"New Rate ({emp['rate']}): ") or emp['rate'])
        print("Information edited.")
    else:
        print("Invalid row number.")
# Logical delete function
def delete_employee():
    search = input("Employee ID or part of name for search: ")
    filtered = display_employees(search)
    if not filtered:
        return
    row_num = int(input("Row number to delete: "))
    if 0 <= row_num < len(filtered):
        save_state('delete', data=filtered[row_num][1]) # Save state and deleted data
        i, emp = filtered[row_num]
        trash_bin.append(employees.pop(i))
        print("Employee moved to trash bin.")
    else:
        print("Invalid row number.")
# Function to calculate salary for one person
def calculate_salary():
    search = input("Employee ID or part of name: ")
    filtered = display_employees(search)
    if not filtered:
        return
    row_num = int(input("Row number: "))
    if 0 <= row_num < len(filtered):
        emp = filtered[row_num][1]
        gross = emp['hours'] * emp['rate']
        tax = gross * 0.05
        net = gross - tax
        print(f"Gross salary: {gross}, Tax: {tax}, Net salary: {net}")
    else:
        print("Invalid row number.")
# Function to calculate total salaries and taxes
def total_salaries():
    total_gross = 0
    total_tax = 0
    for emp in employees:
        gross = emp['hours'] * emp['rate']
        tax = gross * 0.05
        total_gross += gross
        total_tax += tax
    print(f"Total gross salaries: {total_gross}, Total taxes: {total_tax}")
# Filter and sort function
def filter_sort():
    print("Filter by:")
    min_hours = float(input("Minimum hours (or -1 to skip): ") or -1)
    max_hours = float(input("Maximum hours (or -1 to skip): ") or -1)
    min_salary = float(input("Minimum salary (or -1 to skip): ") or -1)
    max_salary = float(input("Maximum salary (or -1 to skip): ") or -1)
   
    filtered = []
    for emp in employees:
        gross = emp['hours'] * emp['rate']
        if (min_hours == -1 or emp['hours'] >= min_hours) and \
           (max_hours == -1 or emp['hours'] <= max_hours) and \
           (min_salary == -1 or gross >= min_salary) and \
           (max_salary == -1 or gross <= max_salary):
            filtered.append(emp)
   
    valid_fields = ['id', 'name', 'hours', 'rate', 'salary']
    
    field = input("Sort by (id/name/hours/rate/salary): ")
    if field not in valid_fields:
        print("Invalid field! Only id, name, hours, rate, salary allowed.")
        return
    reverse = input("Descending? (y/n): ").lower() == 'y'
   
    if field == 'salary':
        filtered.sort(key=lambda e: e['hours'] * e['rate'], reverse=reverse)
    elif field in ['id', 'name', 'hours', 'rate']:
        filtered.sort(key=lambda e: e[field], reverse=reverse)
   
    for emp in filtered:
        gross = emp['hours'] * emp['rate']
        print(f"ID: {emp['id']}, Name: {emp['name']}, Hours: {emp['hours']}, Rate: {emp['rate']}, Salary: {gross}")
# Function to recover from trash bin
def recover_employee():
    if not trash_bin:
        print("Trash bin is empty.")
        return
    for i, emp in enumerate(trash_bin):
        print(f"{i}: ID: {emp['id']}, Name: {emp['name']}")
    row_num = int(input("Row number to recover: "))
    if 0 <= row_num < len(trash_bin):
        recovered = trash_bin.pop(row_num)
        employees.append(recovered)
        print("Employee recovered.")
    else:
        print("Invalid row number.")
# Function to export to file
def export_to_file():
    format_type = input("Format (txt/csv): ").lower()
    filename = input("File name: ")
   
    try:
        if format_type == 'txt':
            with open(filename, 'w', encoding='utf-8') as f:
                for emp in employees:
                    f.write("<< Employee >>\n")
                    f.write(f"{emp['id']} {emp['name']} {emp['rate']} {emp['hours']}\n")
        elif format_type == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['Employee ID', 'Name', 'Hourly Rate', 'Monthly Hours'])
                for emp in employees:
                    writer.writerow([emp['id'], emp['name'], emp['rate'], emp['hours']])
        print("Export successful.")
    except Exception as e:
        print(f"Error: {e}")
        if 'f' in locals():
            f.close()
# Sample data (for quick testing)
def add_sample_data():
    sample_employees = [
        {'id': '1001', 'name': 'Ali Rezaei', 'hours': 160, 'rate': 120000},
        {'id': '1002', 'name': 'Sara Mohammadi', 'hours': 175, 'rate': 130000},
        {'id': '1003', 'name': 'Mohammad Hosseini', 'hours': 168, 'rate': 140000},
        {'id': '1004', 'name': 'Fatemeh Ahmadi', 'hours': 155, 'rate': 115000},
        {'id': '1005', 'name': 'Reza Karimi', 'hours': 180, 'rate': 135000},
        {'id': '1006', 'name': 'Narges Sharifi', 'hours': 162, 'rate': 125000},
        {'id': '1007', 'name': 'Hossein Moradi', 'hours': 170, 'rate': 138000},
        {'id': '1008', 'name': 'Zahra Ghasemi', 'hours': 158, 'rate': 118000},
        {'id': '1009', 'name': 'Amirhossein Taheri', 'hours': 190, 'rate': 150000},
        {'id': '1010', 'name': 'Maryam Sadeghi', 'hours': 165, 'rate': 128000},
    ]
    employees.extend(sample_employees)
    print("10 sample employees added successfully!")
# Main menu
def main_menu():
    while True:
        print("\nMenu:")
        print("0. Exit")
        print("1. Enter information")
        print("2. Display information")
        print("3. Edit information")
        print("4. Logical delete")
        print("5. Calculate salary for one person")
        print("6. Calculate total salaries and taxes")
        print("7. Filter and sort")
        print("8. Recover deleted")
        print("9. Export to file")
        print("10. Undo")
        print("11. Redo") # Adding option for Redo
       
        choice = input("Choice: ")
        if choice == '0':
            break
        elif choice == '1':
            add_employee()
        elif choice == '2':
            search = input("Employee ID or part of name (empty for all): ") or None
            display_employees(search)
        elif choice == '3':
            edit_employee()
        elif choice == '4':
            delete_employee()
        elif choice == '5':
            calculate_salary()
        elif choice == '6':
            total_salaries()
        elif choice == '7':
            filter_sort()
        elif choice == '8':
            recover_employee()
        elif choice == '9':
            export_to_file()
        elif choice == '10':
            undo()
        elif choice == '11':
            redo()
        else:
            print("Invalid choice.")
if __name__ == "__main__":
    add_sample_data()
    main_menu()
