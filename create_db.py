import sqlite3
conn = sqlite3.connect('company.db')
cursor = conn.cursor()
cursor.execute("DROP TABLE IF EXISTS employee_projects;")
cursor.execute("DROP TABLE IF EXISTS employees;")
cursor.execute("DROP TABLE IF EXISTS projects;")
cursor.execute("DROP TABLE IF EXISTS departments;")

cursor.execute('''
CREATE TABLE IF NOT EXISTS departments (
    department_id INTEGER PRIMARY KEY,
    department_name TEXT NOT NULL UNIQUE
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS projects (
    project_id INTEGER PRIMARY KEY,
    project_name TEXT NOT NULL UNIQUE,
    start_date DATE,
    deadline DATE,
    budget REAL
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS employees (
    employee_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL,
    position TEXT,
    salary REAL,
    hire_date DATE,
    department_id INTEGER,
    manager_id INTEGER, -- Self-referencing key to another employee
    FOREIGN KEY (department_id) REFERENCES departments (department_id),
    FOREIGN KEY (manager_id) REFERENCES employees (employee_id)
)
''')
cursor.execute('''
CREATE TABLE IF NOT EXISTS employee_projects (
    assignment_id INTEGER PRIMARY KEY,
    employee_id INTEGER,
    project_id INTEGER,
    role TEXT, -- Role of the employee in that specific project
    FOREIGN KEY (employee_id) REFERENCES employees (employee_id),
    FOREIGN KEY (project_id) REFERENCES projects (project_id)
)
''')

departments_data = [
    (1, 'Engineering'),
    (2, 'Sales'),
    (3, 'Human Resources'),
    (4, 'Marketing')
]
cursor.executemany("INSERT INTO departments VALUES (?, ?)", departments_data)
employees_data = [
    (101, 'Bob Williams', 'Lead Engineer', 120000, '2021-01-15', 1, 000),
    (102, 'Alice Johnson', 'Software Engineer', 95000, '2022-03-10', 1, 101),
    (103, 'Frank Miller', 'Junior Engineer', 75000, '2023-07-20', 1, 101),
    (104, 'Charlie Davis', 'Sales Manager', 110000, '2020-05-01', 2, 000),
    (105, 'Diana Miller', 'Sales Associate', 78000, '2022-08-15', 2, 104),
    (106, 'Eve Brown', 'HR Specialist', 72000, '2021-11-30', 3, 000),
    (107, 'Grace Lee', 'Marketing Director', 115000, '2019-10-01', 4, 000),
    (108, 'Henry Wilson', 'Marketing Analyst', 82000, '2023-02-22', 4, 107)
]
cursor.executemany("INSERT INTO employees VALUES (?, ?, ?, ?, ?, ?, ?)", employees_data)
projects_data = [
    (1, 'Project Phoenix', '2024-01-01', '2025-06-30', 500000),
    (2, 'Project Titan', '2023-09-15', '2024-12-31', 750000),
    (3, 'Q4 Sales Campaign', '2024-10-01', '2024-12-20', 120000)
]
cursor.executemany("INSERT INTO projects VALUES (?, ?, ?, ?, ?)", projects_data)
employee_projects_data = [
    (1, 101, 1, 'Project Lead'),
    (2, 102, 1, 'Lead Developer'),
    (3, 103, 1, 'Developer'),
    (4, 108, 1, 'Marketing Support'),
    
    (5, 102, 2, 'Senior Developer'),
    (6, 105, 2, 'Sales Consultant'),
    
    (7, 104, 3, 'Campaign Manager'),
    (8, 105, 3, 'Lead Associate'),
    (9, 107, 3, 'Marketing Lead')
]
cursor.executemany("INSERT INTO employee_projects VALUES (?, ?, ?, ?)", employee_projects_data)


conn.commit()
conn.close()

print("✅ Database 'company.db' created successfully with interlinked tables.")