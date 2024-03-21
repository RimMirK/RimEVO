# RimEVO
Модуль для моего юзербота RimTUB для игры в @mine_evo_bot (telegram)

*   [Установка](#установка)
*   [Первоначальная настройка](#Первоначальная-настройка)
*   [Команды](#Команды)
*   [Возможности](#Возможности)
*   [Контакт](#Контакт)

## Установка

1.  Установи юзербот [RimTUB](http://t.me/RimTUB).
2.  Закнь файл **mineevo.py** в папку **plugins**
3.  Готово!

## Первоначальная настройка

**Обязятельно запусти бота `@mine_evo_glod_bot` перед запуском скрипта !!**

2.  Создай два чата (группы).  
    Один будет Лог - туда будут отправляться отчёты по найденным кейсам, убитых боссах, и тп.  
    Второй - рабочий чат. В него ЮБ будет отправлять команды.
3.  Добавь в эти чаты все свои аккаунты (твинки) которые играют в Mine EVO
4.  Добавь `@mine_evo_bot` во второй чат (робочий) и дай ему права администратора (назначь админом)
5.  С помощью команды `cid или любым другим способом`узнай **id** этих чатов
6.  Открой на редактирование файл **mineevo.py**
7.  В начале кода внеси айди чатов вместо ноликов, где **`LOG_CHAT`** это первый чат, а `WORKER_CHAT` это рабочий чат с ботом.

Должно получится вот так:
```py
LOG_CHAT = -1245678
WORKER_CHAT = -87654321
```

## Команды

### Легенда: 
   `< >` – обязательный аргумент \
   `[ ]` – необязательный аргумент. \
   ` / ` – или

*   `mine` - Выводит небольшую сводку про копании
*   `mdig` - начинает копать
*   `mnodig`, mstopdig, mundig - завершает копать
*   `evo` \<запрос/команда\> - отправляет запрос/команду в рабочий чат и выводит ответ. Пример: `.evo время`
*   `bevo` \<запрос/команда\> - отправляет запрос/команду боту в ЛС и выводит ответ. Пример: `.bevo кач`
*   `мк`, `mcases` \- выводит твои кейсы
*   `мпроф`, `mprof` \- выводит профиль
*   `мстат`, `mstat` \- выводит статистику
*   `mopen`, `mcase`, `мо`, `мотк`, `моткрыть` (\[тип кейса\] \[количество\]), ... - открывает кейсы без лимитов. Можно открывать сразу несколько типов кейсов Примеры: `.мотк к 36`, `.мотк кт 27 ркт 6 к 3`
*   `mopenlim`, `моткл` \- Установить лимит открытия кейсов за раз
*   `mdelay` \<сек\> - устанавливает заддержку между копанием. Пример: `.mdelay 3.5` | `.mdelay 3`
*   `matcdelay` \- Установить заддержку на атаку босса
*   `mlsend` \< ник чела в боте \> \< сколько раз \> \< сумма \> \- Отправить лимиты
*   `mli` \- Информация о текущей отправке
*   `mlp` \- Поставить отправку на паузу
*   `mlr` \- Возобновить отправку (убрать с паузы)
*   `mls` \- Остановить отправку (на совсем)
*   `mldelay` \[ заддержка в секундах \] \- Установить заддержку на отправку лимитов

## Возможности

*   автоматическая выборка шахты при увеличении уровня
*   Отчет по найденным кейсам, найденным бустерам, убитым боссам
*   авто авто-бур: Сам качает топливо и заправляет бур
*   Авто атака босса: Когда ты выбираешь босса, скрипт сам начинает атаковать босса, и потом сам заканчивает
*   
*   авто Ежедневный Бонус (в разработке)
*   авто Промо (в разработке)
*   авто thx (в разработке)

## Контакт

Разработчик: [**@RimMirK**](http://t.me/RimMirK)
Канал: [**@RimEVO**](http://t.me/RimEVO)
