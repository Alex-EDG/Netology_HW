CREATE TABLE IF NOT EXISTS Genre (
	Genre_id SERIAL PRIMARY KEY,
	Genre_name VARCHAR(60) UNIQUE NOT NULL	
);

CREATE TABLE IF NOT EXISTS Artist (
	Artist_id SERIAL PRIMARY KEY,
	Artist_name VARCHAR(60) NOT NULL	
);

CREATE TABLE IF NOT EXISTS Album (
	Album_id SERIAL PRIMARY KEY,
	Album_name VARCHAR(60) NOT NULL,
	Album_year INTEGER NOT NULL	
);

CREATE TABLE IF NOT EXISTS Track (
	Track_id SERIAL PRIMARY KEY,
	Track_name VARCHAR(60) NOT NULL,
	Track_duratation NUMERIC(4,2) NOT NULL	
);

CREATE TABLE IF NOT EXISTS Collection (
	Collection_id SERIAL PRIMARY KEY,
	Track_id INTEGER NOT NULL REFERENCES Track(Track_id),
	Collection_name VARCHAR(60) NOT NULL,
	Collection_year INTEGER NOT NULL	
);

CREATE TABLE IF NOT EXISTS GenreArtist (
	GenreArtist_id SERIAL PRIMARY KEY,
	Genre_id INTEGER NOT NULL REFERENCES Genre(Genre_id),
	Artist_id INTEGER NOT NULL REFERENCES Artist(Artist_id)
);

CREATE TABLE IF NOT EXISTS ArtistAlbum (
	ArtistAlbum_id SERIAL PRIMARY KEY,
	Artist_id INTEGER NOT NULL REFERENCES Artist(Artist_id),
	Album_id INTEGER NOT NULL REFERENCES Album(Album_id)
);

CREATE TABLE IF NOT EXISTS AlbumTrack (
	AlbumTrack_id SERIAL PRIMARY KEY,
	Album_id INTEGER NOT NULL REFERENCES Album(Album_id),
	Track_id INTEGER NOT NULL REFERENCES Track(Track_id)
);