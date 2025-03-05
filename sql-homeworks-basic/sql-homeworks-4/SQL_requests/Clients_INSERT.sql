INSERT INTO Emails
       (email)  
values
       ('user_01@mail.ru'),
       ('user_02@mail.ru'),
       ('user_03@mail.ru'),
       ('user_04@mail.ru'),
       ('user_05@mail.ru');

INSERT INTO Clients
       (email_id, name, surname) 
VALUES 
       (1, 'Иван', 'Иванов'),
       (2, 'Петр', 'Петров'),
       (3, 'Сидр', 'Сидоров'),
       (4, 'Федор', 'Федоров'),
       (5, 'Степан', 'Степанов');

INSERT INTO Phones
       (client_id, phone_number) 
VALUES 
       (1, '+79881111111'),
       (2, '+79882222222'),
       (3, '+79883333333'),
       (3, '+79884444444'),
       (4, ''),
       (5, '');