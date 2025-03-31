-- 1. Вывести число слов базе у текущего пользователя (например 'Begemot_for_user_bot').

SELECT u.name, COUNT(u_w.id_word) FROM Users_Words u_w
LEFT JOIN Users u ON u_w.id_user = u.id
LEFT JOIN Words w ON u_w.id_word = w.id
WHERE u.name = 'Begemot_for_user_bot'
GROUP BY u.name;

-- 2. Вывести случайных 4 словa (с переводом) изучаемых текущим пользователем (например 'Begemot_for_user_bot').

SELECT w.ru_word, w.en1_word, w.en2_word FROM Users_Words u_w
LEFT JOIN Users u ON u_w.id_user = u.id
LEFT JOIN Words w ON u_w.id_word = w.id
WHERE u.name = 'Begemot_for_user_bot'
ORDER BY RANDOM () LIMIT 4;