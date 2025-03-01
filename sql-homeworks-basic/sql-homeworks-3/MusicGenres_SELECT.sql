-- Задание 2
-- 1. Название и продолжительность самого длительного трека.
SELECT name, duratation FROM tracks
WHERE duratation = (SELECT MAX(duratation) FROM tracks);

-- 2. Название треков, продолжительность которых не менее 3,5 минут.
SELECT name, duratation FROM Tracks
WHERE duratation >= 3.5;

-- 3. Названия сборников, вышедших в период с 2018 по 2020 год включительно.
SELECT DISTINCT name FROM Collections
WHERE year BETWEEN 2018 AND 2020;

-- 4. Исполнители, чьё имя состоит из одного слова.
SELECT name FROM Artists
WHERE name NOT LIKE '% %';

--5. Название треков, которые содержат слово «мой» или «my».
SELECT name FROM Tracks
WHERE name ILIKE '%my%' OR name ILIKE '%мой%';

-- Задание 3
--1. Количество исполнителей в каждом жанре.
SELECT g.name, COUNT(g_a.Genre_id) FROM Genres g
LEFT JOIN Genre_Artist g_a ON g.id = g_a.Genre_id
GROUP BY g.name;

--2. Количество треков, вошедших в альбомы 2019–2020 годов.
SELECT COUNT(a_t.track_id) FROM Albums a
LEFT JOIN Album_Track a_t ON a.id = a_t.album_id
WHERE a.year BETWEEN 2019 AND 2020;

--3. Средняя продолжительность треков по каждому альбому.
SELECT a.name, AVG(t.duratation) FROM Tracks t
RIGHT JOIN Albums a ON a.id = t.album_id
GROUP BY a.name;

--4. Все исполнители, которые не выпустили альбомы в 2020 году.
SELECT ar.name FROM Albums al
LEFT JOIN Artist_Album a_a ON al.id = a_a.album_id
LEFT JOIN Artists ar ON ar.id = a_a.artist_id
WHERE al.year <> 2020;

--5. Названия сборников, в которых присутствует конкретный исполнитель (выберите его сами).
SELECT c.name FROM Collections c
LEFT JOIN Album_Track a_t ON c.track_id = a_t.track_id
LEFT JOIN Artist_Album a_a ON a_t.id = a_a.artist_id
LEFT JOIN Artists a ON a.id = a_a.artist_id
WHERE a.name = 'ModjoHead';

-- Задание 4
-- 1. Названия альбомов, в которых присутствуют исполнители более чем одного жанра.
SELECT c.name  FROM Collections c
JOIN Album_Track a_t ON c.track_id = a_t.track_id
JOIN Tracks t ON t.id = a_t.track_id
JOIN Artist_Album a_a ON a_a.album_id = a_t.album_id
JOIN Genre_Artist g_a ON a_a.artist_id = g_a.artist_id
GROUP BY c.name
HAVING COUNT(g_a.genre_id) > 1;

--2. Наименования треков, которые не входят в сборники.
SELECT t.name FROM Collections c
FULL JOIN Tracks t ON t.id = c.track_id
WHERE t.id NOT IN (SELECT track_id FROM Collections);

--3. Исполнитель или исполнители, написавшие самый короткий по продолжительности трек, — теоретически таких треков может быть несколько.
SELECT ar.name FROM Artists ar
JOIN Artist_Album a_a ON a_a.artist_id = ar.id
JOIN Albums al ON al.id = a_a.album_id
JOIN Tracks t ON t.album_id = a_a.album_id
WHERE t.duratation = (SELECT MIN(duratation) FROM Tracks);

--4. Названия альбомов, содержащих наименьшее количество треков.
SELECT name FROM (
SELECT al.name, COUNT(al.name) as cnt FROM Albums al
JOIN Tracks t ON t.album_id = al.id
group by al.name)
WHERE cnt = (SELECT MIN(cnt) FROM (
SELECT COUNT(al.name) as cnt FROM Albums al
JOIN Tracks t ON t.album_id = al.id
group by al.name));