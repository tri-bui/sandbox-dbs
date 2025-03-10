/*	Employees with a `dept_employees.to_date` are no longer with the company
	Employees born between 1952 and 1955 will begin to retire
	Only employees hired between 1985 and 1988 are eligible for the retirement package */
	
	
-- Eligible retiring employees

DROP TABLE IF EXISTS retiring_emp CASCADE;

SELECT *
INTO retiring_emp
FROM employees
WHERE (emp_no IN ( -- filter for current employees
		SELECT emp_no 
		FROM dept_employees 
		WHERE DATE_PART('year', to_date) = 9999))
	AND (DATE_PART('year', birth_date) BETWEEN 1952 AND 1955)
	AND (DATE_PART('year', hire_date) BETWEEN 1985 AND 1988);
	
SELECT * FROM retiring_emp;


-- Full info on retiring employees

DROP TABLE IF EXISTS retiring_info CASCADE;

WITH s AS (
	SELECT emp_no, salary, from_date AS salary_from, to_date AS salary_to
	FROM (SELECT *, ROW_NUMBER() OVER(PARTITION BY emp_no 
									  ORDER BY to_date DESC, from_date DESC) AS rn
		  FROM salaries) AS sr
	WHERE rn = 1
), tt AS (
	SELECT emp_no, title, from_date AS title_from, to_date AS title_to
	FROM (SELECT *, ROW_NUMBER() OVER(PARTITION BY emp_no 
									  ORDER BY to_date DESC, from_date DESC) AS rn
		  FROM titles) AS tr
	WHERE rn = 1
), de AS (
	SELECT emp_no, dept_no, from_date AS dept_from, to_date AS dept_to
	FROM (SELECT *, ROW_NUMBER() OVER(PARTITION BY emp_no 
									  ORDER BY to_date DESC, from_date DESC) AS rn
		  FROM dept_employees) AS der
	WHERE rn = 1
)
SELECT 
	re.emp_no, re.first_name, re.last_name, re.gender, re.birth_date, re.hire_date,
	tt.title, tt.title_from, tt.title_to,
	s.salary, s.salary_from, s.salary_to,
	d.dept_no, d.dept_name, de.dept_from, de.dept_to
INTO retiring_info
FROM retiring_emp AS re
	JOIN s ON re.emp_no = s.emp_no
	JOIN tt ON re.emp_no = tt.emp_no
	JOIN de ON re.emp_no = de.emp_no
	JOIN departments AS d ON de.dept_no = d.dept_no;

SELECT * FROM retiring_full;
		

-- Number of retiring employees by department

DROP TABLE IF EXISTS retiring_dept CASCADE;

SELECT dept_no, dept_name, COUNT(*)
INTO retiring_dept
FROM retiring_info
GROUP BY dept_no, dept_name
ORDER BY 3 DESC;

SELECT * FROM retiring_dept;
		

-- Number of retiring employees by position

DROP TABLE IF EXISTS retiring_pos CASCADE;

SELECT title, COUNT(*)
INTO retiring_pos
FROM retiring_info
GROUP BY title
ORDER BY 2 DESC;

SELECT * FROM retiring_pos;


-- Info on each department's manager

DROP TABLE IF EXISTS manager_info CASCADE;

WITH curr_managers AS (
	SELECT dm.*, d.dept_name
	FROM (SELECT *, ROW_NUMBER() OVER(PARTITION BY dept_no 
									  ORDER BY to_date DESC) AS rn
		  FROM dept_managers) AS dm
		JOIN departments AS d ON dm.dept_no = d.dept_no
	WHERE dm.rn = 1
)
SELECT 
	cm.dept_no, cm.dept_name, e.emp_no, e.first_name, e.last_name, e.gender, 
	e.birth_date, e.hire_date, cm.from_date AS manager_from, cm.to_date AS manager_to
INTO manager_info
FROM curr_managers AS cm
	JOIN employees AS e ON cm.emp_no = e.emp_no;

SELECT * FROM manager_info;