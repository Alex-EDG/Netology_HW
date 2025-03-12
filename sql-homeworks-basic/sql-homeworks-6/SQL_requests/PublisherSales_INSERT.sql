INSERT INTO Publisher
       (name)  
values
       ('O’Reilly'),
       ('Pearson'),
       ('Microsoft Press'),
       ('No starch press');
       
INSERT INTO Shop
       (name)  
values
       ('Labirint'),
       ('OZON'),
       ('Amazon');

INSERT INTO Book
       (title, id_publisher) 
VALUES 
       ('Programming Python, 4th Edition', 1),
       ('Learning Python, 4th Edition', 1),
       ('Natural Language Processing with Python', 1),
       ('Hacking: The Art of Exploitation', 4),
       ('Modern Operating Systems', 2),
       ('Code Complete: Second Edition', 3);

INSERT INTO Stock
       (id_shop, id_book, count) 
VALUES 
       (1, 1, 34),
       (1, 2, 30),
       (1, 3, 0),
       (2, 5, 40),
       (2, 6, 50),
       (3, 4, 10),
       (3, 6, 10),
       (2, 1, 10),
       (3, 1, 10);
       
INSERT INTO Sale
       (id_stock, price, date_sale, count) 
VALUES 
       (1, 50.05, '2018-10-25T09:45:24.552Z', 16),
       (3, 50.05, '2018-10-25T09:51:04.113Z', 10),
       (6, 10.50, '2018-10-25T09:52:22.194Z', 9),
       (5, 16.00, '2018-10-25T10:59:56.230Z', 5),
       (9, 16.00, '2018-10-25T10:59:56.230Z', 5),
       (4, 16.00, '2018-10-25T10:59:56.230Z', 1);
       