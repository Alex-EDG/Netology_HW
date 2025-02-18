-- один ко многим

CREATE TABLE IF NOT EXISTS Employee (
	Employee_id SERIAL PRIMARY KEY,
	Employee_name VARCHAR(60) NOT NULL,
	Department_name VARCHAR(60) NOT NULL,
	Department_head VARCHAR(60) NOT NULL
);

CREATE TABLE IF NOT EXISTS Department (
	Department_id SERIAL PRIMARY KEY,
	Employee_id INTEGER NOT NULL REFERENCES Employee(Employee_id),
	Department_name VARCHAR(60) UNIQUE NOT NULL,
	Department_head VARCHAR(60) NOT NULL
);