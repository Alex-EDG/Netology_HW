## Курсовая работа «Резервное копирование»

### Неронов Алексей группа <span style="color:green">**FPY-120**</span>

Смотри *.py файлы.

Необходимые для работы программы зависимости указаны в файле requirements.txt

Необходимые для работы данные внесите в соответствующие разделы файла settings.ini:

[vk]

API_version = 5.199 - версия используемого VK API

access_token = ...... - токен доступа для приложение осуществляющего запросы от имени пользователя
(можно плучить по ссылке https://oauth.vk.com/authorize?client_id=..your_App_ID...&display=page&redirect_uri=https://example.com/callback&scope=friends&response_type=token&v=5.199&state=123456)

[yandexdisk]

access_token = ...... - токен доступа для Yandex Disk на который будут сохраняться файлы

[googledisk]

access_token = ...... - токен доступа для Google Drive на который будут сохраняться файлы

Результыты копирования (имя сскопированного файла и его размер) в файле result.json

Логирование процесса в файле Logs.log
