INSERT INTO Users
       (name)  
values
       ('Begemot_for_user_bot');
              
INSERT INTO Words
       (ru_word, en1_word, en2_word)
values
       ('мир', 'peace', 'world'),
       ('замок', 'lock', 'castle'),
       ('нос', 'nose', NULL),
       ('слово', 'word', NULL),
       ('красный', 'red', NULL),
       ('море', 'sea', NULL),
       ('кто', 'who', NULL),
       ('чёрный', 'black', NULL),
       ('почему', 'why', NULL),
       ('два', 'two', NULL);

INSERT INTO Users_Words
       (id_user, id_word)
VALUES 
       (1, 1),
       (1, 2),
       (1, 3),
       (1, 4),
       (1, 5),
       (1, 6),
       (1, 7),
       (1, 8),
       (1, 9),
       (1, 10);