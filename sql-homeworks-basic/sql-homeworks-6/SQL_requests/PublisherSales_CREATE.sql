CREATE TABLE IF NOT EXISTS Publisher (
	id SERIAL PRIMARY KEY,
	name VARCHAR(96) NOT NULL UNIQUE CHECK(name !='')	
);

CREATE TABLE IF NOT EXISTS Shop (
	id SERIAL PRIMARY KEY,
	name VARCHAR(96) NOT NULL UNIQUE CHECK(name !='')	
);

CREATE TABLE IF NOT EXISTS Book (
	id SERIAL PRIMARY KEY,
	id_publisher INTEGER NOT NULL REFERENCES Publisher (id) ON DELETE CASCADE,
	title VARCHAR(128) NOT NULL	UNIQUE
);

CREATE TABLE IF NOT EXISTS Stock (
	id SERIAL PRIMARY KEY,
	id_book INTEGER NOT NULL REFERENCES Book (id) ON DELETE CASCADE,
	id_shop INTEGER NOT NULL REFERENCES Shop (id) ON DELETE CASCADE,
	count SMALLINT NOT NULL	
);

CREATE TABLE IF NOT EXISTS Sale (
	id SERIAL PRIMARY KEY,
	id_stock INTEGER NOT NULL REFERENCES Stock (id) ON DELETE CASCADE,
	price NUMERIC(10,2) NOT NULL,
	date_sale TIMESTAMP WITH TIME ZONE NOT NULL,
	count SMALLINT NOT NULL
);