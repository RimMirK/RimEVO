LOG_CHAT    = -10012345678
WORKER_CHAT = -10012345678



from pyrogram import filters, errors
from config.user_config import PREFIX
from utils import (
    Cmd, get_group, code, b, bq,
    helplist, Module, Argument as Arg, Feature, Command,
    plural, parse_amout,
    ModifyPyrogramClient as Client,
    make_request, get_answer
)
import asyncio
from bs4 import BeautifulSoup

from utils.scripts import pnum, sec_to_str

cmd = Cmd(G:=get_group())

helplist.add_module(
    Module(
        "MineEvo",
        description="Модуль для игры @mine_evo_bot\nКанал с обновлениями: @RimEVO",
        author="@RimMirK & @kotcananacom",
        version='3.7.1'
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
        Command(['mdelay'],    [Arg('заддержка в секундах', False)], 'Установить заддержку на копку / посмотреть заддержку')
    ).add_command(
        Command(['matcdelay'], [Arg('заддержка в секундах', False)], 'Установить заддержку на атаку босса / посмотреть заддержку')
    ).add_command(
        Command(['mlsend'], [Arg('ник чела в боте'), Arg('сколько раз'), Arg('сумма')], 'Отправить лимиты')
    ).add_command(
        Command(["ab", 'аб', 'бур', 'автобур', 'кач'], [], 'Качать топливо и заправить бур')
    ).add_command(
        Command(['mli'], [], 'Информация о текущей отправке')
    ).add_command(
        Command(['mlp'], [], 'Поставить отправку на паузу')
    ).add_command(
        Command(['mlr'], [], 'Возобновить отправку (убрать с паузы)')
    ).add_command(
        Command(['mls'], [], 'Остановить отправку (на совсем)')
    ).add_command(
        Command(['mldelay'], [Arg('заддержка в секундах', False)], 'Установить заддержку на отправку лимитов / посмотреть заддержку')
    ).add_command(
        Command(['mlv', 'mlvalue'], [Arg('значение', False)], 'Установить новый лимит / посмотреть текущий')
    ).add_feature(
        Feature('Авто-выборка шахты', 'автоматическая выборка шахты при увеличении уровня')
    ).add_feature(
        Feature('Log', 'Отчет по найденным кейсам, найденным бустерам, убитым боссам')
    ).add_feature(
        Feature('Авто атака', 'Само начинает и перестает атаковать босса при его выборе')
    ).add_feature(
        Feature('Авто авто-бур', 'Сам качает топливо и заправляет бур')
    ).add_feature(
        Feature('Авто Бонус', 'Сам качает получает Ежедневный Бонус каждый день')
    ).add_feature(
        Feature('Авто Thx', 'Сам вводит комманду thx')
    ).add_feature(
        Feature('Авто Промо', 'Сам смотрит доступные промо и активирует иъ')
    )
)

M = 'MineEVO'

plural_raz = ["раз", "раза", "раз"]


# при запуске
@Client.on_ready(group=get_group())
async def _on_ready(app, *_):
    ev = asyncio.get_event_loop()

    ev.create_task(digger(app)) # копалка
    ev.create_task(auto_thx(app)) # автo thx
    ev.create_task(start_autobonus(app)) # авто Бонус
    await asyncio.sleep(2)
    ev.create_task(start_autobur(app)) # автобур
    await asyncio.sleep(10)
    ev.create_task(start_limits(app)) # лимиты
    await asyncio.sleep(60*5)
    ev.create_task(auto_promo(app)) # авто промо




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

@cmd(["ab", 'аб', 'бур', 'автобур', 'кач'])
async def do_autobur(app, msg=None):
    if msg:
        await msg.edit("👌 Качаю и заправляю бур")
        
    while True:
        app.print("кач")
        new_fuel_msg = await make_request(app, "кач", "mine_evo_bot", timeout=10)
        if new_fuel_msg is None:
            await asyncio.sleep(10)
            continue
        if 'кончилась' in new_fuel_msg.text:
            app.print("нефть закончилась")
            break
        if 'Хранилище заполнено топливом!' in new_fuel_msg.text:
            app.print("Бак заполнен!")
            break
        if 'позже' in new_fuel_msg.text:
            app.print("Бура нет!")
            break
        await asyncio.sleep(2)
            
    app.print('бур')
    bur_msg = await make_request(app, "бур", "mine_evo_bot", timeout=10)
    if bur_msg is None: return
    
    await app.request_callback_answer(
        bur_msg.chat.id, bur_msg.id,
        callback_data=f"am_refuel:am_refuel:{app.me.id}"
    )

# авто авто-бур
async def start_autobur(app):
    app.print("Пополняю бур")
    while True:
        await do_autobur(app)
        await asyncio.sleep(60*60)

# авто Бонус
async def start_autobonus(app: Client):
    while True:
        await make_request(app, 'еб', WORKER_CHAT, timeout=10)
        await asyncio.sleep(60*60*24 +1)

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
            f"⏱ Заддержка установлена на {b(pnum(delay))} c\n"
            f"Таким темпом,\n"
            f"за {b('час')} ты вскопаешь {b(f'{60*60/delay:,.0f}')} раз\n"
            f"за {b(f'день {  60*60*24  /delay:,.0f}'    )} раз\n"
            f"за {b(f'неделю {60*60*24*7/delay:,.0f}')} раз\n"
        )
    except:
        delay = await app.db.get(M, "delay", 3)
        await msg.edit(
            
            f'⏱ Текущая заддержка на копку: {b(pnum(delay))}\n'
            f"Таким темпом,\n"
            f"за {b('час')} ты вскопаешь {b(f'{60*60/delay:,.0f}')} {plural(60*60     /delay, plural_raz)}\n"
            f"за {b(f'день {  60*60*24  /delay:,.0f}'    )} {        plural(60*60*24  /delay, plural_raz)}\n"
            f"за {b(f'неделю {60*60*24*7/delay:,.0f}')} {            plural(60*60*24*7/delay, plural_raz)}\n"
        )

# заддержка на атаку
@cmd(['matcdelay'])
async def _matcdelay(app, msg):
    try:
        delay = float(msg.text.split(maxsplit=1)[-1])
        await app.db.set(M, 'atc_delay', delay)
        await msg.edit(
            f"⏱ Заддержка на атаку установлена: {b(pnum(delay))}\n"
        )
    except:
        await msg.edit(
            f"⏱ Текущая заддержка на атаку: {b(pnum(await app.db.get(M, 'atc_delay', 3)))}"
        )

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


# Лимиты

plural_limit = ['лимит', 'лимита', 'лимитов']

# сама отправка
async def start_limits(app):
    while True:
        if await app.db.get(M, 'limits.status', 'stopped') == 'process':
            if (
                await app.db.get(M, 'limits.current', 0)
                ==
                await app.db.get(M, 'limits.count', 0)
            ): 
                await app.db.set(M, 'limits.status', 'Отправка завершена!')
                break
        
            nickname = await app.db.get(M, 'limits.nickname', '-')
            value = await app.db.get(M, 'limits.value', '-')
            app.print(f'перевести {nickname} {value}')
            m = await make_request(app, f'перевести {nickname} {value}', WORKER_CHAT, timeout=10, typing=False)
            
            if not m:
                app.print(f'перевести {nickname} {value} | Бот не ответил')
                await asyncio.sleep(20)
                continue
            
            if 'недостаточно денег' in m.text:
                app.print(f'перевести {nickname} {value} | Нет денег!')
                await app.send_message(LOG_CHAT, "❗️ Не могу перевести лимиты: денег нету!")
                await app.db.set(M, 'limits.status', "Денег нету!")
                break
            
            if f'перевел(а) игроку  {nickname}' in m.text:
                app.print(m.text)
                await app.db.set(M, 'limits.current', (await app.db.get(M, 'limits.current', 0)) + 1)
                
            await asyncio.sleep(await app.db.get(M, 'limits.delay', 5))
            
        else:
            break
    
# начать переводить
@cmd(['mlsend'])
async def _send(app, msg):
    status = await app.db.get(M, 'limits.status', 'stopped')
    if status == 'process':
        nickname = await app.db.get(M, 'limits.nickname', False)
        return await msg.edit(f"Я уже и так перевожу лимиты!\n{nickname = }")
    elif status == 'paused':
        return await msg.edit(f"Лимиты переводятся, но перевод на паузе")
    
    try: _, nickname, count, value = msg.text.split(maxsplit=3)
    except ValueError: return await msg.edit(f"<code>{PREFIX}{msg.command[0]}</code> < ник игрока > < сколько раз > < сумма > ")
    count = int(count)
    
    await app.db.set(M, 'limits.status', 'process')
    await app.db.set(M, 'limits.nickname', nickname)
    await app.db.set(M, 'limits.count', count)
    await app.db.set(M, 'limits.current', 0)
    await app.db.set(M, 'limits.value', value)
    
    delay = await app.db.get(M, 'limits.delay', 5)
    
    await msg.edit(
        f"💲 перевод игроку 🪪 {code(nickname)}\n"
        f"🎚 {b(count)} раз по 💵 {code(value)}.\n"
        f"Время отправки: ⏳ примерно {b(sec_to_str(count * delay))}\n"
    )
    
    await start_limits(app)

# инфо
@cmd(['mli'])
async def _mli(app, msg):
    delay = await app.db.get(M, 'limits.delay', 5)
    if nickname := await app.db.get(M, 'limits.nickname', False):
        
        status  = await app.db.get(M, 'limits.status', 'stopped')
        count   = await app.db.get(M, 'limits.count')
        current = await app.db.get(M, 'limits.current', 0)
        value   = await app.db.get(M, 'limits.value', '-')
        
        await msg.edit(
            b("Текущий перевод: \n\n") +
            f"ℹ️ {b('|')} Статус: {b(status)}\n"
            f"⏱ {b('|')} Заддержка: {b(sec_to_str(delay))}\n"
            f"🪪 {b('|')} Кому: {code(nickname)}\n"
            f"💵 {b('|')} Сколько: {code(value)}\n"
            f"🎚 {b('|')} Сколько раз: {b(count)} {plural(count, plural_raz)}\n"
            f"📟 {b('|')} уже отправилось: {b(current)} {plural(current, plural_limit)}\n"
            f"⏰ {b('|')} еще надо отправить: {b(count-current)} {plural(count-current, plural_limit)}\n"
            f"⏳ {b('|')} Примерно осталось: {b(sec_to_str((count-current)*delay))}"
        )
    else:
        return await msg.edit(f"Переводов нет!\n\nЗаддержка: {b(delay)}")
        
# остановить
@cmd(['mls'])
async def _mls(app, msg):
    await msg.edit("лимиты отменены!")
    await app.db.set(M, 'limits.status', 'stopped')
    await app.db.set(M, 'limits.nickname', '-')
    await app.db.set(M, 'limits.count', 0)
    await app.db.set(M, 'limits.current', 0)
    await app.db.set(M, 'limits.value', '-')

# поставить на паузу
@cmd(['mlp'])
async def _mlp(app, msg):
    await msg.edit("⏸ Лимиты поставлены на паузу!")
    await app.db.set(M, 'limits.status', 'paused')

    
# продолжить (убрать с паузы)
@cmd(['mlr'])
async def _mlr(app, msg):
    if await app.db.get(M, 'limits.status', 'stopped') not in ['paused', 'process']:
        return await msg.edit("Так ничего не паузе и не стоит!")
    await app.db.set(M, 'limits.status', 'process')
    
    await msg.edit("▶️ Возобновлено!")
    
    await start_limits(app)


# заддержка
@cmd(['mldelay'])
async def _mldelay(app, msg):
    try:
        delay = float(msg.text.split(maxsplit=1)[-1])
        await app.db.set(M, 'limits.delay', delay)
        await msg.edit(
            f"⏱ Заддержка на отправку лимитов установлена на {b(pnum(delay))}"
        )
    except:
        await msg.edit(
            f'⏱ Текущая заддержка на отправку лимитов: {b(pnum(await app.db.get(M, "limits.delay", 5)))}'
        )

@cmd(['mlv', 'mlvalue'])
async def _mlvalue(app, msg):
    try: _, value = msg.text.split(maxsplit=1)
    except ValueError: return await msg.edit(f"💵 Текущее значение: {code(await app.db.get(M, 'limits.value', '--'))}")
    await app.db.set(M, 'limits.value', value)
    await msg.edit(f"💵 Значение успешно установлено на {code(value)}")
    

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
    answer = await make_request(app, query, WORKER_CHAT, timeout=10, additional_filter=filters.user("mine_evo_bot"))
    await msg.edit(f"{SAD} Бот не ответил" if answer is None else layout.format(query, answer.text.html),
        disable_web_page_preview=True
    )

# запрос боту в ЛС
@cmd('bevo')
async def _bevo(app, msg):
    await msg.edit(f'{LOADING} Загрузка...')
    query = msg.text.split(maxsplit=1)[1]
    answer = await make_request(app, query, WORKER_CHAT, timeout=10, additional_filter=filters.user("mine_evo_bot"))
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
    (
        filters.regex(".*для атаки выбери босса\!.*") |
        filters.regex("🎉 Босс")
    ), group=get_group()
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
# @Client.on_message(
#     filters.chat(['mine_evo_bot', 'mine_evo_gold_bot']) &
#     filters.user(['mine_evo_bot', 'mine_evo_gold_bot']) &
#     filters.regex("Руда на уровень")
#     , group=get_group()
# )
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

# авто промо
async def auto_promo(app):
    while True:
        promo_msg = await make_request(app, 'промо', 'mine_evo_bot', timeout=10)
        if promo_msg != None:
            if "чтобы, ввести промокод, используй:" in promo_msg.text:
                bs = BeautifulSoup(promo_msg.text.html, 'lxml')
                promos = (*map(lambda e: e.text, bs.find_all('code')[2:]),)
                for promo in promos:
                    await app.send_message('mine_evo_bot', f'промо {promo}')
                    await asyncio.sleep(4)
        else:
            await asyncio.sleep(20)
            continue
        
        await asyncio.sleep(60*60*20)   
                    
# авто thx 
async def auto_thx(app):
    while True:
        sent_message = await app.send_message(WORKER_CHAT, 'thx')
        m = await get_answer(app, sent_message, startswith='❕')
        if m:
            try: await m.delete()
            except: pass
        await sent_message.delete()
        
        await asyncio.sleep(60*30)
    
    

    
