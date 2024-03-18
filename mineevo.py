LOG_CHAT    = -10012345678
WORKER_CHAT = -10012345678


from pyrogram import filters, errors
from utils import (
    Cmd, get_group, code, b, bq,
    helplist, Module, Argument as Arg, Feature, Command,
    plural, parse_amout,
    ModifyPyrogramClient as Client,
    make_request
)
import asyncio
from bs4 import BeautifulSoup

cmd = Cmd(G:=get_group())

helplist.add_module(
    Module(
        "MineEvo",
        description="Модуль для игры @mine_evo_bot",
        author="@RimMirK & @kotcananacom",
        version='3.1.0'
    ).add_command(
        Command(['mine'], [], 'Вывести сводку')
    ).add_command(
        Command(['mdig'], [], 'начинает копать')
    ).add_command(
        Command(['mstopdig', 'mnodig', 'mundig'], [], 'перестает копать')
    ).add_command(
        Command(['evo'], [Arg('запрос/команда')], 'отправляет запрос/команду в робочий чат и выводит ответ. Пример: .evo время')
    ).add_command(
        Command(['bevo'], [Arg('запрос/команда')], 'отправляет запрос/команду боту в ЛС и выводит ответ. Пример: .evo время')
    ).add_command(
        Command(['mprof', 'мпроф'], [], 'Выводит профиль')
    ).add_command(
        Command(['mstat', 'ms', 'mstats', 'мстата', 'мстат', 'мстатистика'], [],'Выводит статистику')
    ).add_command(
        Command(['mcases', 'мк', 'мкейсы'], [], 'выводит твои кейсы')
    ).add_command(
        Command(["mopen", "mcase", 'мо', 'мотк', 'моткрыть'], [Arg('([тип кейса] [количество]), ..')],'открывает кейсы без лимитов. Можно открывать сразу несколько типов кейсов Примеры: .отк к 36 | .отк кт 27 ркт 6 к 3 ')
    ).add_command(
        Command(['моткл', 'mopenlim'], [Arg('кол-во')],'Установить лимит открытия кейсов за раз')
    ).add_command(
        Command(['mdelay'],    [Arg('сек')], 'Установить заддержку на копку')
    ).add_command(
        Command(['matcdelay'], [Arg('сек')], 'Установить заддержку на атаку босса')
    ).add_feature(
        Feature('Авто-выборка шахты', 'автоматическая выборка шахты при увеличении уровня')
    ).add_feature(
        Feature('Log', 'Отчет по найденным кейсам, найденным бустерам, убитым боссам')
    ).add_feature(
        Feature('Авто атака', 'Само начинает и перестает атаковать босса при его выборе')
    ).add_feature(
        Feature('Авто авто-бур', 'Сам качает топливо и заправляет бур')
    )
)

M = 'MineEVO'

plural_raz = ["раз", "раза", "раз"]


# при запуске
@Client.on_ready(group=get_group())
async def _on_ready(app, *_):
    ev = asyncio.get_event_loop()

    ev.create_task(digger(app)) # копалка
    ev.create_task(start_autobur(app)) # автобур



# сводка
@cmd(['mine'])  
async def _mine(app, msg):
    c = await app.db.get(M, 'c', 0)
    all_c = await app.db.get(M, 'all_c', 0)
    await msg.edit(
        "Копаю: " + b(
            'Да <emoji id="5359300921123683281">✅</emoji>'
            if await app.db.get(M, 'work', False)
            else 'Нет <emoji id="5359457318062798459">❌</emoji>', False
        ) + '\n'
        f"Вскопал: " + b(f"{c} {plural(c, plural_raz)}") + '\n'
        f"Всего вскопал: " + b(f"{all_c} {plural(all_c, plural_raz)}") + '\n'
    )


# копатель
async def digger(app):
    while True:
        if await app.db.get(M, 'work', False) == True:
            app.print('коп')

            try: await app.send_message('mine_EVO_gold_bot', "⛏ Копать")
            except errors.flood_420.FloodWait as s:
                try: await asyncio.sleep(s)
                except: await asyncio.sleep(1)
                await app.send_message('mine_EVO_gold_bot', "⛏ Копать")
            await asyncio.sleep(await app.db.get(M, 'delay', 3)) 
        else: return

# атака
async def attacker(app):
    while True:
        if await app.db.get(M, 'atc', False):
            app.print('атк')

            try: await app.send_message('mine_EVO_bot', "атк")
            except errors.flood_420.FloodWait as s:
                try: await asyncio.sleep(s)
                except: await asyncio.sleep(1)
                await app.send_message('mine_EVO_bot', "атк")
            await asyncio.sleep(await app.db.get(M, 'atc_delay', 3)) 
        else: return

# кол-во топлива в буре
async def check_fuel(app):
    for _ in range(10):
        bur_msg = await make_request(app, "бур", "mine_evo_bot", startswith='🚧 Автобур игрока', timeout=10)
        if bur_msg is None:
            await asyncio.sleep(10)
            continue
        st = bur_msg.text.split()
        return int(st[ st.index('складе:') + 1 ])
    
# авто авто-бур
async def start_autobur(app):
    app.print("Пополняю бур каждые 12 часов")
    while True:
        if await check_fuel(app) == 0:
            for _ in range(10):
                new_fuel_msg = await make_request(app, "кач", "mine_evo_bot", startswith='🛢 Бочка топлива', timeout=10)
                if new_fuel_msg is None:
                    await asyncio.sleep(10)
                    continue
                if new_fuel_msg.text.startswith('❗️В месторождении кончилась нефть!'):
                    break
            
        bur_msg = await make_request(app, "бур", "mine_evo_bot", timeout=10)
        if bur_msg is None:
            await asyncio.sleep(10)
            continue
        await app.request_callback_answer(
            bur_msg.chat.id, bur_msg.id,
            callback_data=f"am_refuel:am_refuel:{app.me.id}"
        )
        await asyncio.sleep(60*60*12)


# начать копать
@cmd(['mdig'])
async def _dig(app, msg):
    if await app.db.get(M, 'work', False):
        await msg.edit("❎ Я и так копаю")
        return
    
    await app.db.set(M, 'work', True)

    await msg.edit("✅ копаю")
    await digger(app)
    
# закончить копать
@cmd(['mstopdig', 'mnodig', 'mundig'])
async def _stopdig(app, msg):
    if not await app.db.get(M, 'work', False):
        return await msg.edit(f'❎ а я и не копаю')

    await app.db.set(M, 'work', False)

    c = await app.db.get(M, 'c', 0)
    await msg.edit(f'❎ не копаю. Успел копнуть {b(c)} {b(plural(c, plural_raz))}')

    await app.db.set(M, 'c', 0)
    await app.db.delete(M, 'stats')

# заддержка на копку
@cmd(['mdelay'])
async def _mdelay(app, msg):
    try:
        delay = float(msg.text.split(maxsplit=1)[-1])
        await app.db.set(M, 'delay', delay)
        await msg.edit(
            f"Заддержка установлена на {delay}\n"
            f"Таким темпом\n"
            f"за {b('час')} ты вскопаешь {b(f'{60*60/delay:,.0f}')} раз\n"
            f"за {b(f'день {  60*60*24  /delay:,.0f}'    )} раз\n"
            f"за {b(f'неделю {60*60*24*7/delay:,.0f}')} раз\n"
        )
    except:
        await msg.edit('ошибка')

# заддержка на атаку
@cmd(['matcdelay'])
async def _matcdelay(app, msg):
    try:
        delay = float(msg.text.split(maxsplit=1)[-1])
        await app.db.set(M, 'atc_delay', delay)
        await msg.edit(
            f"Заддержка установлена на атаку: {delay}\n"
        )
    except:
        await msg.edit('ошибка')

# префиксы денег
pref = {
    'K':  10**(3*1),
    'M':  10**(3*2),
    'B':  10**(3*3),
    'T':  10**(3*4),
    'Qa': 10**(3*5),
    'Qi': 10**(3*6),
    'Sx': 10**(3*7),
    'Sp': 10**(3*8),
    'O':  10**(3*9),
    'N':  10**(3*10),
    'D':  10**(3*11),
    "Aa": 10**(3*12),
    "Bb": 10**(3*13),
    "Cc": 10**(3*14),
    "Dd": 10**(3*15),
    "Ee": 10**(3*16),
    "Ff": 10**(3*17),
    "Gg": 10**(3*18),
    "Hh": 10**(3*19),
    "Ii": 10**(3*20),
    "Jj": 10**(3*21),
    "Kk": 10**(3*22),
    "Ll": 10**(3*23),
    "Mm": 10**(3*24),
    "Nn": 10**(3*25),
    "Oo": 10**(3*26),
    "Pp": 10**(3*27),
    "Qq": 10**(3*28),
    "Rr": 10**(3*29),
    "Ss": 10**(3*30),
    "Tt": 10**(3*31),
    "Uu": 10**(3*32),
    "Vv": 10**(3*33),
    "Ww": 10**(3*34),
    "Xx": 10**(3*35),
    "Yy": 10**(3*36),
    "Zz": 10**(3*37)
}


# отпрака лимитов
# @cmd(['send'])
async def _send(app, msg):
    _, nickname, count, val = msg.text.split(maxsplit=3)
    count = int(count)
    to_send = parse_amout(val, pref) / (1 - .1), 2
    await msg.edit(
        f"💲 перевод игроку {code(nickname)}\n"
        f"{code(count)} раз по {code(val)}.\n"
        f"С у чётом комисии: {code(round(to_send, 2))}\n"
        f"Время отправки: {b(count * 2)} с.\n"
        f"или {b(round(count * 2 / 60, 2))} м.\n"
        f"или {b(round(count * 2 / 60 / 60, 2))} ч."
    )

# открывание кейсов
@cmd(["mopen", "mcase", 'мо', 'мотк', 'моткрыть'])
async def _open(app, msg):
    try:
        _, *values = msg.text.split()

        if len(values) % 2 != 0:
            raise ValueError()

        await msg.edit(f"📤 открываю {f', '.join([f'{values[i]} {values[i + 1]}' for i in range(0, len(values), 2)])}")

        for amout, case_type in [(values[i], values[i + 1]) for i in range(0, len(values), 2)]:
            await asyncio.sleep(2)

            try: amout = int(amout)
            except ValueError:
                amout, case_type = case_type, amout
                amout = int(amout)

            caselim = await app.db.get(M, 'caselim', 20)

            groups = [*[caselim]*(amout//caselim), amout%caselim]
            try: groups.remove(0)
            except: pass

            for am in groups:
                await asyncio.sleep(2)
                await app.send_message(msg.chat.id, f"открыть {case_type} {am}")

    except (IndexError, ValueError) as e: 
        print(e)
        await msg.edit(
            f"Неверный ввод данных!"
        )

# установить лимит на открытие кейсов за раз
@cmd(['моткл', 'mopenlim'])
async def _mopenlim(app, msg):
    try:
        lim = int(msg.text.split(maxsplit=1)[-1])
        await app.db.set(M, 'caselim', lim)
        await msg.edit(b("Готово!"))
    except IndexError:
        return await msg.edit(b('Неверный ввод данных!'))

# доп функция. Режет строку до определенного символа
split_to = lambda text, to=None: text if to is None else (text+' ')[:text.find(to)]

# емодзи
SAD = '<emoji id=5319007148565341481>☹️</emoji>'
LOADING = '<emoji id=5821116867309210830>⏳</emoji>'

# шаблон для .evo и .bevo
layout = (''
    + b("Запрос:") + "\n"
    + bq('{0}') + "\n"
    + b("Ответ Бота:") + "\n"
    + bq('{1}')
)

# запрос боту
@cmd('evo')
async def _evo(app, msg):
    await msg.edit(f'{LOADING} Загрузка...')
    query = msg.text.split(maxsplit=1)[1]
    answer = await make_request(app, query, WORKER_CHAT, timeout=10)
    await msg.edit(f"{SAD} Бот не ответил" if answer is None else layout.format(query, answer.text.html),
        disable_web_page_preview=True
    )

# запрос боту в ЛС
@cmd('bevo')
async def _bevo(app, msg):
    await msg.edit(f'{LOADING} Загрузка...')
    query = msg.text.split(maxsplit=1)[1]
    answer = await make_request(app, query, 'mine_evo_bot', timeout=10)
    await msg.edit(f"{SAD} Бот не ответил" if answer is None else layout.format(query, answer.text.html),
        disable_web_page_preview=True
    )

# показать кейсы
@cmd(['mcases', 'мк', 'мкейсы'])
async def _cases(app, msg):
    await msg.edit(f'{LOADING} Загрузка...')
    answer = await make_request(app, 'кейсы', WORKER_CHAT, '📦 Кейсы игрока', 10)
    await msg.edit(
        f"{SAD} Бот не ответил" if answer is None else split_to(split_to(answer.text.html, '🔥'), 'Открыть'),
        disable_web_page_preview=True
    )

# показать профиль
@cmd(['mprof', 'mp', 'мп', 'мпроф', 'мпрофиль'])
async def _prof(app, msg):
    await msg.edit(f'{LOADING} Загрузка...')
    answer = await make_request(app, 'профиль', WORKER_CHAT, 'Профиль пользователя', 10)
    await msg.edit(f"{SAD} Бот не ответил" if answer is None else split_to(answer.text.html, '🔥'),
        disable_web_page_preview=True
    )

# показать стату
@cmd(['mstat', 'ms', 'mstats', 'мстата', 'мстат', 'мстатистика'])
async def _stat(app, msg):    
    await msg.edit(f'{LOADING} Загрузка...')
    answer = await make_request(app, 'стата', WORKER_CHAT, 'Статистика пользователя', 10)
    await msg.edit(f"{SAD} Бот не ответил" if answer is None else answer.text.html,
        disable_web_page_preview=True
    )


# авто атака босса
@Client.on_message(
    filters.chat('mine_evo_bot') &
    filters.user('mine_evo_bot') &
    filters.regex('🔶 Ты выбрал босса: .*')
)
async def _boss(app, _):    
    await app.send_message(LOG_CHAT, "Бью боссиков")
    
    await app.db.set(M, 'atc', True)
    
    await attacker(app)
      
# остановка автоатаки  
@Client.on_message(
    filters.chat('mine_evo_bot') &
    filters.user('mine_evo_bot') &
    filters.regex(".*для атаки выбери босса\!.*")
)       
async def _stopboss(app, _):
    await app.db.set(M, 'atc', False)
    await app.send_message(LOG_CHAT, "Закончил бить босса")

# обновление шахты
@Client.on_message(
    filters.chat('mine_evo_bot') &
    filters.user('mine_evo_bot') &
    filters.regex('🔓 Открыта новая шахта')
    ,
    group=get_group()
)
async def _new_cave(app, msg):
    await app.send_message('mine_evo_bot', msg.text[23:])

# обработка копки
@Client.on_message(
    filters.chat(['mine_evo_bot', 'mine_evo_gold_bot']) &
    filters.user(['mine_evo_bot', 'mine_evo_gold_bot']) &
    filters.regex("Руда на уровень")
    , group=get_group()
)
async def _dig_ore(app, msg):
    t, th = msg.text, msg.text.html
    """
    🎆  <b><i>Плазма +1</i></b> 

    ⛏ <b>Материя II</b>  +<b>16.60Qi ед.</b> 
    <b><i>Руда на уровень :  100%  /  100%</i></b>
    """
    plasma, ore_type, ore_count = 0, '', 0
    s = BeautifulSoup(th, 'html.parser')
    if "Плазма" in t:
        plasma = int(s.find('i').text[8:])

    ore_type = s.find_all('b')[-3].text
    ore_str_count = s.find_all('b')[-2].text
    ore_count = int(parse_amout(ore_str_count, pref))
    
    # app.print(f"выокопал {plasma = } | {ore_type = } | {ore_str_count = } | {ore_count = }")

    d = await app.db.get(M, 'stats', {})

    # app.print('Всего' + str(d))

    ores = d.get('ores', {})
    ores[ore_type] = ores.get(ore_type, 0) + ore_count

    await app.db.set(M, 'stats', dict(
        plasma = d.get('plasma', 0) + plasma,
        ores = ores
    ))


    d = await app.db.get(M, 'stats_all', {})

    # app.print('Всего вообще ' + str(d))

    ores = d.get('ores', {})
    ores[ore_type] = ores.get(ore_type, 0) + ore_count

    await app.db.set(M, 'stats_all', dict(
        plasma = d.get('plasma', 0) + plasma,
        ores = ores
    ))


    await app.db.set(M, 'c',
        (await app.db.get(M, 'c', 0)) + 1
    )

    await app.db.set(M, 'all_c',
        (await app.db.get(M, 'all_c', 0)) + 1
    )
    
# лог кейсов, боссов
@Client.on_message(
    filters.chat(['mine_evo_bot', 'mine_evo_gold_bot']) &
    filters.user(['mine_evo_bot', 'mine_evo_gold_bot']) & (
        filters.regex('[✨|😄|📦|🧧|✉️|🌌|💼|👜|🗳|🕋|💎|🎲].*Найден.*') |
        filters.regex('⚡️.*нашел\(ла\).*') |
        filters.regex('🎉 Босс')
    ),
    group=get_group()
)
async def _find_cases(_, msg):
    await msg.copy(LOG_CHAT)
