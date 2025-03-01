INSERT INTO Genres
       (name)  
values
       ('Pop'),
       ('Rap'),
       ('Rock'),
       ('Soul');

INSERT INTO Artists
       (name) 
values
       ('Dynoro'),
       ('ModjoHead'),
       ('Warm Ice'),
       ('Tears of the heart');

INSERT INTO Albums
       (name, year) 
values
       ('In My Mind', 2018),
       ('HeadShot', 2019),
       ('Ice Planet', 2019),
       ('My soul', 2020);

INSERT INTO Tracks
       (name, album_id, duratation) 
VALUES 
       ('In My Mind', 1, 3.07),
       ('HeadShot', 2, 2.25),
       ('Ice Planet', 3, 3.5),
       ('Frozen dream', 3, 4.2),
       ('Two broken hearts', 4, 4.05),
       ('Space', 4, 3.15),
       ('My soul', 4, 5.05);

INSERT INTO Collections
       (name, track_id, year) 
VALUES 
       ('FM hits 2019', 1, 2019),
       ('FM hits 2019', 2, 2019),
       ('Summer hits 2019', 3, 2019),
       ('FM hits 2020', 6, 2020),
       ('Summer hits 2019', 7, 2020);
       
INSERT INTO Genre_Artist
       (genre_id, artist_id) 
VALUES 
       (1, 1),
       (2, 2),
       (3, 1),
       (4, 4);

INSERT INTO Artist_Album
       (artist_id, album_id)
VALUES 
       (1, 1),
       (2, 2),
       (3, 3),
       (4, 4);
       
INSERT INTO Album_Track
       (album_id, track_id)
VALUES 
       (1, 1),
       (2, 2),
       (3, 3),
       (3, 4),
       (4, 5),
       (4, 6),
       (4, 7);