import csv
import os

# لیست اصلی کارکنان
employees = []

# سطل زباله برای حذف‌شده‌ها
trash_bin = []

# پشته‌های Undo و Redo
undo_stack = []
redo_stack = []

# تابع برای ذخیره وضعیت فعلی برای Undo
def save_state(action, data=None):
    state = {
        'action': action,
        'employees': employees.copy(),
        'trash_bin': trash_bin.copy(),
        'data': data
    }
    undo_stack.append(state)
    redo_stack.clear()  # وقتی عملیات جدیدی انجام می‌شود، Redo پاک می‌شود

# تابع Undo
def undo():
    if not undo_stack:
        print("هیچ عملیاتی برای Undo وجود ندارد.")
        return
    last_state = undo_stack.pop()
    global employees, trash_bin
    employees = last_state['employees'].copy()
    trash_bin = last_state['trash_bin'].copy()
    redo_stack.append(last_state)
    print("عملیات Undo انجام شد.")

# تابع Redo
def redo():
    if not redo_stack:
        print("هیچ عملیاتی برای Redo وجود ندارد.")
        return
    next_state = redo_stack.pop()
    global employees, trash_bin
    employees = next_state['employees'].copy()
    trash_bin = next_state['trash_bin'].copy()
    undo_stack.append(next_state)
    print("عملیات Redo انجام شد.")

# تابع ورود اطلاعات
def add_employee():
    save_state('add')  # ذخیره وضعیت قبل از افزودن
    while True:
        emp_id = input("شماره پرسنلی (-1 برای خروج): ")
        if emp_id == '-1':
            break
        name = input("نام: ")
        hours = float(input("ساعت کارکرد ماهیانه: "))
        rate = float(input("حق الزحمه یک ساعت: "))
        employee = {'id': emp_id, 'name': name, 'hours': hours, 'rate': rate}
        employees.append(employee)
        print("اطلاعات اضافه شد.")

# تابع نمایش اطلاعات
def display_employees(search_term=None):
    if not employees:
        print("هیچ کارمندی وجود ندارد.")
        return []
    filtered = []
    for i, emp in enumerate(employees):
        if search_term is None or search_term in emp['id'] or search_term.lower() in emp['name'].lower():
            filtered.append((i, emp))
    if not filtered:
        print("هیچ نتیجه‌ای یافت نشد.")
        return []
    for idx, (i, emp) in enumerate(filtered):
        print(f"{idx}: شماره پرسنلی: {emp['id']}, نام: {emp['name']}, ساعت: {emp['hours']}, حق الزحمه: {emp['rate']}")
    return filtered

# تابع ویرایش اطلاعات
def edit_employee():
    search = input("شماره پرسنلی یا بخشی از نام برای جستجو: ")
    filtered = display_employees(search)
    if not filtered:
        return
    row_num = int(input("شماره ردیف برای ویرایش: "))
    if 0 <= row_num < len(filtered):
        i, emp = filtered[row_num]
        print("ویرایش اطلاعات:")
        emp['id'] = input(f"شماره پرسنلی جدید ({emp['id']}): ") or emp['id']
        emp['name'] = input(f"نام جدید ({emp['name']}): ") or emp['name']
        emp['hours'] = float(input(f"ساعت جدید ({emp['hours']}): ") or emp['hours'])
        emp['rate'] = float(input(f"حق الزحمه جدید ({emp['rate']}): ") or emp['rate'])
        print("اطلاعات ویرایش شد.")
    else:
        print("شماره ردیف نامعتبر.")

# تابع حذف منطقی
def delete_employee():
    search = input("شماره پرسنلی یا بخشی از نام برای جستجو: ")
    filtered = display_employees(search)
    if not filtered:
        return
    row_num = int(input("شماره ردیف برای حذف: "))
    if 0 <= row_num < len(filtered):
        save_state('delete', data=filtered[row_num][1])  # ذخیره وضعیت و داده حذف‌شده
        i, emp = filtered[row_num]
        trash_bin.append(employees.pop(i))
        print("کارمند به سطل زباله منتقل شد.")
    else:
        print("شماره ردیف نامعتبر.")

# تابع محاسبه حقوق یک نفر
def calculate_salary():
    search = input("شماره پرسنلی یا بخشی از نام: ")
    filtered = display_employees(search)
    if not filtered:
        return
    row_num = int(input("شماره ردیف: "))
    if 0 <= row_num < len(filtered):
        emp = filtered[row_num][1]
        gross = emp['hours'] * emp['rate']
        tax = gross * 0.05
        net = gross - tax
        print(f"حقوق ناخالص: {gross}, مالیات: {tax}, حقوق خالص: {net}")
    else:
        print("شماره ردیف نامعتبر.")

# تابع محاسبه جمع حقوق و مالیات
def total_salaries():
    total_gross = 0
    total_tax = 0
    for emp in employees:
        gross = emp['hours'] * emp['rate']
        tax = gross * 0.05
        total_gross += gross
        total_tax += tax
    print(f"جمع حقوق ناخالص: {total_gross}, جمع مالیات: {total_tax}")

# تابع فیلتر و مرتب‌سازی
def filter_sort():
    print("فیلتر بر اساس:")
    min_hours = float(input("حداقل ساعت (یا -1 برای رد): ") or -1)
    max_hours = float(input("حداکثر ساعت (یا -1 برای رد): ") or -1)
    min_salary = float(input("حداقل حقوق (یا -1 برای رد): ") or -1)
    max_salary = float(input("حداکثر حقوق (یا -1 برای رد): ") or -1)
    
    filtered = []
    for emp in employees:
        gross = emp['hours'] * emp['rate']
        if (min_hours == -1 or emp['hours'] >= min_hours) and \
           (max_hours == -1 or emp['hours'] <= max_hours) and \
           (min_salary == -1 or gross >= min_salary) and \
           (max_salary == -1 or gross <= max_salary):
            filtered.append(emp)
    
    valid_fields = ['id', 'name', 'hours', 'rate', 'salary']
     
    field = input("مرتب بر اساس (id/name/hours/rate/salary): ")
    if field not in valid_fields:
        print("فیلد نامعتبر! فقط id, name, hours, rate, salary مجاز است.")
        return

    reverse = input("نزولی؟ (y/n): ").lower() == 'y'
    
    if field == 'salary':
        filtered.sort(key=lambda e: e['hours'] * e['rate'], reverse=reverse)
    elif field in ['id', 'name', 'hours', 'rate']:
        filtered.sort(key=lambda e: e[field], reverse=reverse)
    
    for emp in filtered:
        gross = emp['hours'] * emp['rate']
        print(f"ID: {emp['id']}, Name: {emp['name']}, Hours: {emp['hours']}, Rate: {emp['rate']}, Salary: {gross}")

# تابع بازیابی از سطل زباله
def recover_employee():
    if not trash_bin:
        print("سطل زباله خالی است.")
        return
    for i, emp in enumerate(trash_bin):
        print(f"{i}: ID: {emp['id']}, Name: {emp['name']}")
    row_num = int(input("شماره ردیف برای بازیابی: "))
    if 0 <= row_num < len(trash_bin):
        recovered = trash_bin.pop(row_num)
        employees.append(recovered)
        print("کارمند بازیابی شد.")
    else:
        print("شماره ردیف نامعتبر.")

# تابع خروجی به فایل
def export_to_file():
    format_type = input("فرمت (txt/csv): ").lower()
    filename = input("نام فایل: ")
    
    try:
        if format_type == 'txt':
            with open(filename, 'w', encoding='utf-8') as f:
                for emp in employees:
                    f.write("<< Employee >>\n")
                    f.write(f"{emp['id']} {emp['name']} {emp['rate']} {emp['hours']}\n")
        elif format_type == 'csv':
            with open(filename, 'w', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow(['شماره پرسنلی', 'نام', 'حق الزحمه یک ساعت', 'ساعت کارکرد ماهیانه'])
                for emp in employees:
                    writer.writerow([emp['id'], emp['name'], emp['rate'], emp['hours']])
        print("خروجی با موفقیت گرفته شد.")
    except Exception as e:
        print(f"خطا: {e}")
        if 'f' in locals():
            f.close()

# داده‌های نمونه (برای تست سریع)
def add_sample_data():
    sample_employees = [
        {'id': '1001', 'name': 'علی رضایی',       'hours': 160, 'rate': 120000},
        {'id': '1002', 'name': 'سارا محمدی',       'hours': 175, 'rate': 130000},
        {'id': '1003', 'name': 'محمد حسینی',       'hours': 168, 'rate': 140000},
        {'id': '1004', 'name': 'فاطمه احمدی',       'hours': 155, 'rate': 115000},
        {'id': '1005', 'name': 'رضا کریمی',        'hours': 180, 'rate': 135000},
        {'id': '1006', 'name': 'نرگس شریفی',        'hours': 162, 'rate': 125000},
        {'id': '1007', 'name': 'حسین مرادی',       'hours': 170, 'rate': 138000},
        {'id': '1008', 'name': 'زهرا قاسمی',        'hours': 158, 'rate': 118000},
        {'id': '1009', 'name': 'امیرحسین طاهری',    'hours': 190, 'rate': 150000},
        {'id': '1010', 'name': 'مریم صادقی',       'hours': 165, 'rate': 128000},
    ]
    employees.extend(sample_employees)
    print("10 کارمند نمونه با موفقیت اضافه شدند!")

# منوی اصلی
def main_menu():
    while True:
        print("\nمنو:")
        print("0. خروج")
        print("1. ورود اطلاعات")
        print("2. نمایش اطلاعات")
        print("3. ویرایش اطلاعات")
        print("4. حذف منطقی")
        print("5. محاسبه حقوق یک نفر")
        print("6. محاسبه جمع حقوق و مالیات")
        print("7. فیلتر و مرتبسازی")
        print("8. بازیابی حذف‌شده‌ها")
        print("9. خروجی به فایل")
        print("10. Undo")
        print("11. Redo")  # اضافه کردن گزینه برای Redo
        
        choice = input("انتخاب: ")
        if choice == '0':
            break
        elif choice == '1':
            add_employee()
        elif choice == '2':
            search = input("شماره پرسنلی یا بخشی از نام (خالی برای همه): ") or None
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
            print("انتخاب نامعتبر.")

if __name__ == "__main__":
    add_sample_data()  
    main_menu()