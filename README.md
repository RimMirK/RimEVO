# RimEVO
Модуль для моего юзербота RimTUB для игры в @mine_evo_bot (telegram)

- [Установка](#установка)
- [Первоначальная настройка](#первоначальная-настройка)
- [Команды](#команды)
  + [**Легенда**](#легенда)
  + [копка](#копка)
  + [команды](#команды-1)
  + [быстрый доступ](#быстрый-доступ)
  + [кейсы](#кейсы)
  + [Боссы](#боссы)
  + [лимиты](#лимиты)
  + [Прочее](#прочее)
- [Возможности](#возможности)
- [Контакт](#контакт)

## Установка

1.  Установи юзербот [RimTUB](http://t.me/RimTUB).
2.  Скачай* файл **mineevo.py** в папку **plugins**
3.  Если скачиваешь впервые - также скачай* **mineevo_config.py** и тоже закинь в папку **plugins**
4.  Готово!

\* \- Чтобы скачать файл - жми эту кнопку

![image](https://i.imgur.com/V9XzwIf.png)

## Первоначальная настройка

1.  Создай два чата (группы).  
    Один будет Лог - туда будут отправляться отчёты по найденным кейсам, убитых боссах, и тп.  
    Второй - рабочий чат. В него ЮБ будет отправлять команды.
2.  Добавь в эти чаты все свои аккаунты (твинки) которые играют в Mine EVO
3.  Добавь `@mine_evo_bot` во второй чат (робочий) и дай ему права администратора (назначь админом)
4.  С помощью команды `cid` или любым другим способом узнай **id** этих чатов
5.  Открой на редактирование файл **mineevo_config.py**
6.  В начале кода внеси айди чатов вместо ноликов, где **`LOG_CHAT`** это первый чат, а `WORKER_CHAT` это рабочий чат с ботом.
7.  Если хочешь, можешь поменять и бота, в котором ты будешь копать изменив параметр `DIG_BOT`

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

#### копка
*   `mine` - Выводит небольшую сводку про копании
*   `mdig` - начинает копать
*   `mnodig`, mstopdig, mundig - завершает копать
*   `mdelay` \<сек\> - устанавливает заддержку между копанием. Пример: `.mdelay 3.5` | `.mdelay 3`
#### команды
*   `evo` \<запрос/команда\> - отправляет запрос/команду в рабочий чат и выводит ответ. Пример: `.evo время`
*   `bevo` \<запрос/команда\> - отправляет запрос/команду боту в ЛС и выводит ответ. Пример: `.bevo кач`
#### быстрый доступ
*   `мк`, `mcases` \- выводит твои кейсы
*   `мпроф`, `mprof` \- выводит профиль
*   `мстат`, `mstat` \- выводит статистику
#### кейсы
*   `mopen`, `mcase`, `мо`, `мотк`, `моткрыть` (\[тип кейса\] \[количество\]), ... - открывает кейсы без лимитов. Можно открывать сразу несколько типов кейсов Примеры: `.мотк к 36`, `.мотк кт 27 ркт 6 к 3`
*   `mopenlim`, `моткл` \- Установить лимит открытия кейсов за раз
#### Боссы
*   `matcdelay` \- Установить заддержку на атаку босса
#### лимиты
*   `mlsend` \< ник чела в боте \> \< сколько раз \> \< сумма \> \- Отправить лимиты
*   `mli` \- Информация о текущей отправке
*   `mlp` \- Поставить отправку на паузу
*   `mlr` \- Возобновить отправку (убрать с паузы)
*   `mls` \- Остановить отправку (на совсем)
*   `mldelay` \[ заддержка в секундах \] \- Установить заддержку на отправку лимитов
*   `mlv`, `mlvalue` \[ значение \] \- Установить новый лимит / посмотреть текущий
*   `mla`, `mlautovalue` \[ значение / 0 для выключения\] - установить период авто-лимита
#### Прочее
*  `ab`, `аб`, `бур`, `автобур`, `кач` - Качать топливо и заправить бур

## Возможности

*   автоматическая выборка шахты при увеличении уровня
*   Отчет по найденным кейсам, найденным бустерам, убитым боссам
*   авто авто-бур: Сам качает топливо и заправляет бур
*   Авто атака босса: Когда ты выбираешь босса, скрипт сам начинает атаковать босса, и потом сам заканчивает
*   авто Ежедневный Бонус: сам забирает Ежедневный Бонус каждый день
*   авто Промо
*   авто thx

## Контакт

Разработчик: [**@RimMirK**](http://t.me/RimMirK)
Канал: [**@RimEVO**](http://t.me/RimEVO)

