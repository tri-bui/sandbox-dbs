/*	Employees with a `dept_employees.to_date` are no longer with the company
	Employees born between 1952 and 1955 will begin to retire
	Only employees hired between 1985 and 1988 are eligible for the retirement package */
	
	
-- -- Drop retiring_emp table
-- DROP TABLE retiring_emp CASCADE;

-- Filter for eligible retiring employees
WITH curr_employees AS (
	SELECT emp_no, MAX(to_date)
	FROM dept_employees
	GROUP BY emp_no
	HAVING DATE_PART('year', MAX(to_date)) = 9999
)
SELECT e.*
INTO retiring_emp -- save query results into table
FROM curr_employees AS ce
	JOIN employees AS e ON ce.emp_no = e.emp_no
WHERE (DATE_PART('year', e.birth_date) BETWEEN 1952 AND 1955)
	AND (DATE_PART('year', e.hire_date) BETWEEN 1985 AND 1988);
	
-- Test query
SELECT * FROM retiring_emp;


-- -- Drop retiring_full table
-- DROP TABLE retiring_full CASCADE;

-- Get full info on retiring employees
SELECT 
	re.emp_no, re.first_name, re.last_name, re.gender, re.birth_date, re.hire_date,
	tt.title, tt.title_from, tt.title_to,
	s.salary, s.salary_from, s.salary_to,
	d.dept_no, d.dept_name, de.dept_from, de.dept_to
INTO retiring_full -- save query results into table
FROM retiring_emp AS re
	JOIN (
		SELECT emp_no, salary, from_date AS salary_from, to_date AS salary_to
		FROM (SELECT *, ROW_NUMBER() OVER(PARTITION BY emp_no ORDER BY to_date DESC, from_date DESC) AS rn
			  FROM salaries) AS sr
		WHERE rn = 1
	) AS s ON re.emp_no = s.emp_no
	JOIN (
		SELECT emp_no, title, from_date AS title_from, to_date AS title_to
		FROM (SELECT *, ROW_NUMBER() OVER(PARTITION BY emp_no ORDER BY to_date DESC, from_date DESC) AS rn
			  FROM titles) AS tr
		WHERE rn = 1
	) AS tt ON re.emp_no = tt.emp_no
	JOIN (
		SELECT emp_no, dept_no, from_date AS dept_from, to_date AS dept_to
		FROM (SELECT *, ROW_NUMBER() OVER(PARTITION BY emp_no ORDER BY to_date DESC, from_date DESC) AS rn
			  FROM dept_employees) AS der
		WHERE rn = 1
	) AS de ON re.emp_no = de.emp_no
	JOIN departments AS d ON de.dept_no = d.dept_no;

-- Test query
SELECT * FROM retiring_full;
		

-- -- Drop retiring_dept table
-- DROP TABLE retiring_dept CASCADE;

-- Count retiring employees by department
SELECT dept_no, dept_name, COUNT(*)
INTO retiring_dept -- save query results into table
FROM retiring_full
GROUP BY dept_no, dept_name
ORDER BY 3 DESC;

-- Test query
SELECT * FROM retiring_dept;


-- -- Drop dept_info table
-- DROP TABLE manager_info CASCADE;

-- Get info on each department's manager
WITH curr_managers AS (
	SELECT dm.*, d.dept_name
	FROM (SELECT *, ROW_NUMBER() OVER(PARTITION BY dept_no ORDER BY to_date DESC) AS rn
		FROM dept_managers) AS dm JOIN departments AS d ON dm.dept_no = d.dept_no
	WHERE dm.rn = 1
)
SELECT cm.dept_no, cm.dept_name, e.emp_no, e.first_name, e.last_name, e.gender, 
	e.birth_date, e.hire_date, cm.from_date AS manager_from, cm.to_date AS manager_to
INTO manager_info -- save query results into table
FROM curr_managers AS cm
	JOIN employees AS e ON cm.emp_no = e.emp_no;

-- Test query
SELECT * FROM manager_info;