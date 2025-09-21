
--Käyttäjätaulu. Ideat pöllitty enimmäkseen Stravasta. Sekundäärisiä taulutarpeita ainakin
-- -- Kaupungit -- voi tulla myös käyttäjältä
-- -- Alueet -- voi tulla myös käyttäjältä
-- -- Kaupungit ja alueet voi periaatteessa olla myös vapaatekstikenttiä.
-- -- Lajit

-- -- Kommentit - tauluun voi hakea inspiraatiota Githubista.


create table users (
	id INTEGER PRIMARY KEY,
	username TEXT UNIQUE,
	password_hash TEXT,
	first_name TEXT, 
	last_name TEXT,
	date_of_birth TEXT, 
	date_of_death TEXT,
	weight NUMERIC, 
	height NUMERIC, 
	fav_sport_id INTEGER REFERENCES sports(sport_id), 
	max_heart_rate INTEGER,	
	ftp_cycling INTEGER,
	city_id INTEGER REFERENCES cities(city_id)
);


create table sports (
	sport_id INTEGER PRIMARY KEY, 
	sport_name TEXT
);


create table workouts (
	workout_id INTEGER PRIMARY KEY, 
	sport_id INTEGER, 
	begin_time TEXT, 
	end_time TEXT, 
	user_id INTEGER
);


create table cities (
		city_id INTEGER PRIMARY KEY, 
		city TEXT, 
		region TEXT, 
		country TEXT
);


create table comments (
	id INTEGER PRIMARY KEY,
	user_id INTEGER REFERENCES users(id),
	timestamp TEXT,
	content TEXT
);



create table replies (
	id INTEGER PRIMARY KEY,
	comment_id INTEGER REFERENCES comments(id),
	user_id INTEGER REFERENCES users(id),
	timestamp TEXT,
	content TEXT
);
