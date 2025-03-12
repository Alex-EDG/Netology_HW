-- 1. Вывести факты покупки книг (book.title, shop.name, sale.price, sale.date_sale(date = %DD-%MM-%YYYY))
--    выбранного издателя (например O’Reilly ).

SELECT b.title, sh.name, sl.price, TO_CHAR(sl.date_sale, 'DD-MM-YYYY') FROM Sale sl
LEFT JOIN Stock st ON sl.id_stock = st.id
LEFT JOIN Shop sh ON st.id_shop = sh.id
LEFT JOIN Book b ON st.id_book = b.id
LEFT JOIN Publisher p ON b.id_publisher = p.id
WHERE p.name = 'O’Reilly';