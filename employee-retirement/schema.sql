/* Uncomment this code block to drop tables before recreating them
-- Drop all tables
DROP TABLE titles CASCADE;
DROP TABLE salaries CASCADE;
DROP TABLE dept_employees CASCADE;
DROP TABLE dept_managers CASCADE;
DROP TABLE employees CASCADE;
DROP TABLE departments CASCADE;
*/


-- Create tables

CREATE TABLE departments (
	dept_no CHAR(4) NOT NULL,
	dept_name VARCHAR(40) NOT NULL,
	PRIMARY KEY (dept_no),
	UNIQUE (dept_no)
);

CREATE TABLE employees (
	emp_no INT NOT NULL,
	birth_date DATE NOT NULL,
	first_name VARCHAR(40) NOT NULL,
	last_name VARCHAR(40) NOT NULL,
	gender CHAR(1) NOT NULL,
	hire_date DATE NOt NULL,
	PRIMARY KEY (emp_no),
	UNIQUE (emp_no)
);

CREATE TABLE dept_managers (
	dept_no CHAR(4) NOT NULL,
	emp_no INT NOT NULL,
	from_date DATE NOT NULL,
	to_date DATE NOT NULL,
	FOREIGN KEY (dept_no) REFERENCES departments (dept_no),
	FOREIGN KEY (emp_no) REFERENCES employees (emp_no),
	PRIMARY KEY (dept_no, emp_no, from_date)
);

CREATE TABLE dept_employees (
	emp_no INT NOT NULL,
	dept_no CHAR(4) NOT NULL,
	from_date DATE NOT NULL,
	to_date DATE NOT NULL,
	FOREIGN KEY (emp_no) REFERENCES employees (emp_no),
	FOREIGN KEY (dept_no) REFERENCES departments (dept_no),
	PRIMARY KEY (emp_no, dept_no, from_date)
);

CREATE TABLE salaries (
	emp_no INT NOT NULL,
	salary INT NOT NULL,
	from_date DATE NOT NULL,
	to_date DATE NOT NULL,
	FOREIGN KEY (emp_no) REFERENCES employees (emp_no),
	PRIMARY KEY (emp_no, salary, from_date)
);

CREATE TABLE titles (
	emp_no INT NOT NULL,
	title VARCHAR(40) NOT NULL,
	from_date DATE NOT NULL,
	to_date DATE NOT NULL,
	PRIMARY KEY (emp_no, title, from_date)
);


-- Show tables
SELECT table_name FROM information_schema.tables WHERE table_schema = 'public';