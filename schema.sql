create table users (
	id INTEGER PRIMARY KEY,
	username TEXT UNIQUE,
	password_hash TEXT,
	first_name TEXT, 
	last_name TEXT,
	date_of_birth TEXT, 
	weight NUMERIC, 
	height NUMERIC, 
	fav_sport_id INTEGER REFERENCES sports(sport_id), 
	max_heart_rate INTEGER,	
	ftp_cycling INTEGER,
	city_id INTEGER REFERENCES cities(city_id)
);


create table sports (
	sport_id INTEGER PRIMARY KEY, 
	sport_name TEXT,
	sport_type TEXT
);

create table exercises (
	exercise_id INTEGER PRIMARY KEY,
	exercise_name TEXT
);

create table exercise_purposes (
	purpose_id INTEGER PRIMARY KEY,
	purpose_name TEXT
);

create table exercises_and_sports (
	id INTEGER PRIMARY KEY,
	exercise_id INTEGER REFERENCES exercises(exercise_id),
	sport_id INTEGER REFERENCES sports(sport_id)
);


CREATE TABLE exercises_and_purposes (
	id INTEGER PRIMARY KEY,
	exercise_id INTEGER REFERENCES exercises(exercise_id),
	purpose_id INTEGER REFERENCES exercise_purposes(purpose_id)
);

--User can add multiple excercises in one workout
	--make this a long data so that multiple
	--excercises can take place under one workout
create table workouts (
	id INTEGER PRIMARY KEY, 
	workout_id TEXT UNIQUE,
	sport_id INTEGER REFERENCES sports(sport_id), 
	begin_time TEXT, 
	end_time TEXT, 
	user_id INTEGER,
	exercise_id INTEGER REFERENCES exercises(exercise_id),
	purpose_id INTEGER REFERENCES exercise_purposes(purpose_id),
	sets INTEGER,
	reps INTEGER,
	weight INTEGER,
	comments TEXT,
	avg_hr INTEGER
	--maybe time on hr-zone 1-5 
	--categorizing of excercise needs to be revised
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
	workout_id TEXT REFERENCES workouts(workout_id),
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
