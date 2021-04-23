# Employee Retirement Analysis

A fictional company wants to do a review of their employees to get an idea of how many employees will be retiring. This way, the company can prepare retirement packages for retiring employees and recruiting of new hires to take their place. As a guideline, employees born between 1952 and 1955 will begin to retire and only employees hired between 1985 and 1988 are eligible for the retirement package. The data being used is fictional company data consisting of 6 datasets (described in the `Data` section below).

This miniproject explores creating a SQL database and tables using PostgreSQL. The following steps outline the workflow of this project:
1. Create an entity relationship diagram (ERD) with QuickDBD to visualize the data schema (all files in `data/raw/quickdbd/`)
2. Create a new database on pgAdmin
3. Create empty tables for each of the 6 datasets based on the schema (`schema.sql`)
4. Import the 6 data files (from `data/raw/`) into the corresponding table just created
5. Perform an analysis (described in the `Analysis` section below) on the data using SQL queries and save the results as new tables (`analysis.sql`)
6. Export new tables to CSV files


## Analysis

The analysis of retiring employees in `analysis.sql` consists of queries that output the results to a new table in the database, which is then exported as a CSV file to `data/analysis/`. The queries performed answer the following questions:
1. Which employees will be retiring and are eligible for the retirement package? `retiring_emp.csv`
2. What is the most current title and salary of these employees? `retiring_info.csv`
3. How many employees from each department will be retiring? `retiring_dept.csv`
4. What are the titles of the retiring employees and how many of each are there? `retiring_pos.csv`
5. Who are the current department managers? `manager_info.csv`

The CSV file after each question (all found in `data/analysis/`) contains the query results of that question.


## Data

![Data schema](data/raw/quickdbd/ERD.png)<br />
This ERD was created with [QuickDBD](https://www.quickdatabasediagrams.com/). All files in the `data/raw/quickdbd/` directory were exported from QuickDBD.

- `departments.csv` - all departments in the company
- `employees.csv` - general information for all company employees
- `dept_managers.csv` - department managers (departments recorded more than once have gotten a new manager at some point)
- `dept_employees.csv` - department employees (employees recorded more than once have worked for more than 1 department)
- `salaries.csv` - employee salaries (employees may be recorded more than once if their salary has changed)
- `titles.csv` - employee titles (employees may be recorded more than once if their title has changed)

These tables were created in the database with the code in `schema.sql`.


## Tools

- [QuickDBD](https://www.quickdatabasediagrams.com/) - a web application for creating ERDs
- [PostgreSQL 12](https://www.postgresql.org/) - one of the most popular relational database systems
- [pgAdmin 4](https://www.pgadmin.org/) - a database administration interface for PostgreSQL