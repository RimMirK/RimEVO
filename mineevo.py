from pyrogram import filters
from config.user_config import PREFIX
from utils import (
    Cmd, get_group, code, b, bq,
    helplist, Module, Argument as Arg, Feature, Command,
    plural, pnum, sec_to_str,
    ModifyPyrogramClient as Client,
    make_request
)
import asyncio
from bs4 import BeautifulSoup

cmd = Cmd(G:=get_group())

helplist.add_module(
    Module(
        "MineEvo",
        description="Модуль для игры @mine_evo_bot\nКанал с обновлениями: @RimEVO\nСкачать/обновить модуль: https://github.com/RimMirK/RimEVO",
        author="@RimMirK & @kotcananacom",
        version='3.9.0'
    ).add_command(
        Command(['msetlogchat'], [], 'Установить ЛОГ чат (куда выводить отчет о найденых кейсах)')
    ).add_command(
        Command(['msetworkerchat'], [], 'Устаночить Робочий чат (куда отправлять команды)')
    ).add_command(
        Command(['msetdigbot'], [], 'Установить бота для копания (где нужно копать)')
    ).add_command(
        Command(['mine'], [], 'Вывести сводку (статистику)')
    ).add_command(
        Command(['mdig'], [], 'Начать копать')
    ).add_command(
        Command(['mstopdig', 'mnodig', 'mundig'], [], 'Перестать копать')
    ).add_command(
        Command(['evo'], [Arg('запрос/команда')], 'Отправить запрос/команду в робочий чат и посмотреть ответ. Пример: .evo время')
    ).add_command(
        Command(['bevo'], [Arg('запрос/команда')], 'Отправить запрос/команду боту в ЛС и посмотреть ответ. Пример: .bevo время')
    ).add_command(
        Command(['mprof', 'мпроф'], [], 'Вывести профиль')
    ).add_command(
        Command(['mstat', 'ms', 'mstats', 'мстата', 'мстат', 'мстатистика'], [],'Вывести статистику бота')
    ).add_command(
        Command(['mcases', 'мк', 'мкейсы'], [], 'Вевести кейсы')
    ).add_command(
        Command(["mopen", "mcase", 'мо', 'мотк', 'моткрыть'], [Arg('([тип кейса] [количество]), ..')],'Открыть кейсы без лимитов. Можно открывать сразу несколько типов кейсов Примеры: .отк к 36 | .отк кт 27 ркт 6 к 3 ')
    ).add_command(
        Command(['моткл', 'mopenlim'], [Arg('кол-во')],'Установить лимит открытия кейсов за раз')
    ).add_command(
        Command(['mdelay'],    [Arg('заддержка в секундах', False)], 'Установить заддержку на копку / посмотреть заддержку')
    ).add_command(
        Command(['matcdelay'], [Arg('заддержка в секундах', False)], 'Установить заддержку на атаку босса / посмотреть заддержку')
    ).add_command(
        Command(['mlsend'], [Arg('ник чела в боте'), Arg('сколько раз'), Arg('сумма (лимит) (можно поставить любое значение, если включен авто-лимит. Тогда значение установиться само)')], 'Отправить лимиты')
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
        Command(['mla'], [Arg('период', False)], 'Установить период авто-лимита. 0 чтобы выкл')
    ).add_command(
        Command(['mldelay'], [Arg('заддержка в секундах', False)], 'Установить заддержку на отправку лимитов / посмотреть заддержку')
    ).add_command(
        Command(['mlv', 'mlvalue'], [Arg('значение', False)], 'Установить новый лимит / посмотреть текущий')
    ).add_feature(
        Feature('Авто-выборка шахты', 'автоматическая выборка шахты при увеличении уровня')
    ).add_feature(
        Feature('Log', 'Отчет по найденным кейсам, найденным бустерам, убитым боссам')
    ).add_feature(
        Feature('Статистика', 'Подсчет найденых ресурсов с копания и убитых боссов')
    ).add_feature(
        Feature('Авто атака', 'Само начинает и перестает атаковать босса при его выборе')
    ).add_feature(
        Feature('Авто авто-бур', 'Сам качает топливо и заправляет бур')
    ).add_feature(
        Feature('Авто Бонус', 'Сам получает Ежедневный Бонус каждый день')
    ).add_feature(
        Feature('Авто Thx', 'Сам вводит комманду thx')
    ).add_feature(
        Feature('Авто Промо', 'Сам смотрит доступные промокоды и активирует их')
    )
)

M = 'MineEVO'

dig_bots = ["mine_evo_bot", "mine_evo_gold_bot", "mine_evo_emerald_bot"]

plural_raz = ["раз", "раза", "раз"]

get_worker_chat = lambda app: app.db.get('MineEVO.config', 'worker_chat', 'mine_evo_bot')
get_log_chat = lambda app, thread=False: app.db.get('MineEVO.config', 'log_chat.thread') if thread else app.db.get('MineEVO.config', 'log_chat', 'me')
get_dig_bot = lambda app: app.db.get('MineEVO.config', 'digbot', 'mine_evo_bot')

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


@cmd(['msetlogchat'])
async def _setlogchat(app, msg):
    await app.db.set("MineEVO.config", 'log_chat', msg.chat.id)
    await app.db.set("MineEVO.config", 'log_chat.thread', msg.message_thread_id)
    await msg.edit(b("Лог чат успешно установлен!"))

@cmd(['msetworkerchat', 'msetworkchat'])
async def _setworkerchat(app, msg):
    await app.db.set("MineEVO.config", 'worker_chat', msg.chat.id)
    await msg.edit(b("Робочий чат успешно установлен!"))

@cmd(['msetdigbot', 'msetdigchat'])
async def _setdigbot(app, msg):
    await app.db.set("MineEVO.config", 'digbot', msg.chat.id)
    await msg.edit(b("Чат для копки успешно установлен!"))

get_stats = lambda app, case, all=False: app.db.get(f'MineEVO.stats{".all" if all else ""}', case, 0)
fm = lambda num: f"{num:,}" if num >= 10000 else str(num)

# сводка
@cmd(['mine'])  
async def _mine(app, msg):
    c = await app.db.get('MineEVO.stats', 'c', 0)
    all_c = await app.db.get('MineEVO.stats.all', 'c', 0)
    o = "⛏ Копаю: " + b(
            'Да <emoji id="5359300921123683281">✅</emoji>'
            if await app.db.get(M, 'work', False)
            else 'Нет <emoji id="5359457318062798459">❌</emoji>', False
        ) + '\n'
    o += f"🪨 Вскопал: {b(fm(c))} {b(plural(c, plural_raz))} | {b(fm(all_c))} {b(plural(all_c, plural_raz))}\n"
    o += f"🎆 Плазма: {b(fm(await get_stats(app, 'плазма')))} | {b(fm(await get_stats(app, 'плазма', True)))}\n\n"
    o += b('Статистика по найденным кейсам:\n')
    s = (
        (f"  ✉️ Конверт: {             b(fm(await get_stats(app, 'кт'))) } | {b(fm(await get_stats(app, 'кт',  True)))} \n" if (await get_stats(app, 'кт'))  > 0 or (await get_stats(app, 'кт', True))  > 0 else '') +
        (f"  🧧 Редкий конверт: {      b(fm(await get_stats(app, 'ркт')))} | {b(fm(await get_stats(app, 'ркт', True)))} \n" if (await get_stats(app, 'ркт')) > 0 or (await get_stats(app, 'ркт', True)) > 0 else '') +
        (f"  📦 Кейс: {                b(fm(await get_stats(app, 'к')))  } | {b(fm(await get_stats(app, 'к',   True)))} \n" if (await get_stats(app, 'к'))   > 0 or (await get_stats(app, 'к', True))   > 0 else '') +
        (f"  🗳 Редкий кейс: {         b(fm(await get_stats(app, 'рк'))) } | {b(fm(await get_stats(app, 'рк',  True)))} \n" if (await get_stats(app, 'рк'))  > 0 or (await get_stats(app, 'рк', True))  > 0 else '') +
        (f"  🕋 Мифический кейс: {     b(fm(await get_stats(app, 'миф')))} | {b(fm(await get_stats(app, 'миф', True)))} \n" if (await get_stats(app, 'миф')) > 0 or (await get_stats(app, 'миф', True)) > 0 else '') +
        (f"  💎 Кристальный кейс: {    b(fm(await get_stats(app, 'кр'))) } | {b(fm(await get_stats(app, 'кр',  True)))} \n" if (await get_stats(app, 'кр'))  > 0 or (await get_stats(app, 'кр', True))  > 0 else '') +
        (f"  🎲 Дайс кейс: {           b(fm(await get_stats(app, 'дк'))) } | {b(fm(await get_stats(app, 'дк',  True)))} \n" if (await get_stats(app, 'дк'))  > 0 or (await get_stats(app, 'дк', True))  > 0 else '') +
        (f"  💼 Портфель с эскизами: { b(fm(await get_stats(app, 'псэ')))} | {b(fm(await get_stats(app, 'псэ', True)))} \n" if (await get_stats(app, 'псэ')) > 0 or (await get_stats(app, 'псэ', True)) > 0 else '') +
        (f"  👜 Сумка с предметами: {  b(fm(await get_stats(app, 'ссп')))} | {b(fm(await get_stats(app, 'ссп', True)))} \n" if (await get_stats(app, 'ссп')) > 0 or (await get_stats(app, 'ссп', True)) > 0 else '') +
        (f"  🌌 Звездный кейс: {       b(fm(await get_stats(app, 'зв'))) } | {b(fm(await get_stats(app, 'зв',  True)))} \n" if (await get_stats(app, 'зв'))  > 0 or (await get_stats(app, 'зв', True))  > 0 else '')
    )
    o += s if s else b("Пусто\n")
    await msg.edit(o)
    

# копатель
async def digger(app: Client):
    while True:
        if await app.db.get(M, 'work', False) == True:
            app.logger.debug('коп')
            await app.send_message(await get_dig_bot(app), "⛏ Копать")
            await asyncio.sleep(await app.db.get(M, 'delay', 3)) 
        else: return

# атака
async def attacker(app):
    while True:
        if await app.db.get(M, 'atc', False):
            app.logger.debug('атк')
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
        app.logger.debug("кач")
        new_fuel_msg = await make_request(app, "кач", "mine_evo_bot", timeout=10)
        if new_fuel_msg is None:
            await asyncio.sleep(10)
            continue
        if 'кончилась' in new_fuel_msg.text:
            app.logger.warning("нефть закончилась")
            break
        if 'Хранилище заполнено топливом!' in new_fuel_msg.text:
            app.logger.warning("Бак заполнен!")
            break
        if 'позже' in new_fuel_msg.text:
            app.logger.error("Бура нет!")
            break
        await asyncio.sleep(2)
            
    app.logger.debug('бур')
    bur_msg = await make_request(app, "бур", "mine_evo_bot", timeout=10)
    if bur_msg is None: return
    
    await app.request_callback_answer(
        bur_msg.chat.id, bur_msg.id,
        callback_data=f"am_refuel:am_refuel:{app.me.id}"
    )

# авто авто-бур
async def start_autobur(app):
    app.logger.debug("Пополняю бур")
    while True:
        await do_autobur(app)
        await asyncio.sleep(60*60)

# авто Бонус
async def start_autobonus(app: Client):
    while True:
        await make_request(app, 'еб', await get_worker_chat(app), timeout=10)
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
async def _stopdig(app: Client, msg):
    S = 'MineEVO.stats'
    if not await app.db.get(M, 'work', False):
        return await msg.edit(f'❎ а я и не копаю')

    await app.db.set(M, 'work', False)

    c = await app.db.get(S, 'c', 0)
    
    for var in (await app.db.getall(S)).keys():
        await app.db.delete(S, var)
    
    await msg.edit(f'❎ не копаю. Успел копнуть {b(c)} {b(plural(c, plural_raz))}')


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
            
            current = await app.db.get(M, 'limits.current', 0)
            count = await app.db.get(M, 'limits.count', 0)
            
            if (current == count): 
                await app.db.set(M, 'limits.status', 'Отправка завершена!')
                break
        
            nickname = await app.db.get(M, 'limits.nickname', '-')
            value = await app.db.get(M, 'limits.value', '-')
            autovalue = await app.db.get(M, 'limits.autovalue', 0)
            
            app.logger.info(f'перевести {nickname} {value}')
            
            if (autovalue > 0) and (current % autovalue==0):
                avm = await make_request(app, "б", await get_worker_chat(app), timeout=10)
                if not avm:
                    app.logger.error("limits autovalue: бот не ответил")
                bl = ''
                testval = ''
                
                for l in avm.text.split("\n"):
                    if l.startswith("💵"):
                        bl = l
                        break
                bal = bl.split()[3]
                testval += bal.split('.')[0]
                pref = ''
                for s in bal:
                    if s.isalpha():
                        pref += s
                testval += pref
                
                lim_auto = await make_request(app, f"перевести {nickname} {testval}", await get_worker_chat(app), timeout=10)
                
                value = str(lim_auto.text.split()[-1][:-1])
                
                await app.db.set(M, 'limits.value', value)
                app.logger.info(f"Значение лимита автоматически установлено на {value}!")
                
                await asyncio.sleep(await app.db.get(M, 'limits.delay', 5))
                
                                
            
            m = await make_request(app, f'перевести {nickname} {value}', await get_worker_chat(app), timeout=10, typing=False)
            
            if not m:
                app.logger.error(f'перевести {nickname} {value} | Бот не ответил')
                await asyncio.sleep(20)
                continue
            
            if 'недостаточно денег' in m.text:
                app.logger.error(f'перевести {nickname} {value} | Нет денег!')
                await app.send_message(await get_log_chat(app), "❗️ Не могу перевести лимиты: денег нету!", message_thread_id=await get_log_chat(app, True))
                await app.db.set(M, 'limits.status', "Денег нету!")
                break
            
            if f'перевел(а) игроку  {nickname}' in m.text:
                app.logger.info(m.text)
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
    except ValueError: return await msg.edit(f"<code>{PREFIX}{msg.command[0]}</code> < ник игрока > < сколько раз > < сумма (лимит) > ")
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
        
        status    = await app.db.get(M, 'limits.status', 'stopped')
        count     = await app.db.get(M, 'limits.count')
        current   = await app.db.get(M, 'limits.current', 0)
        value     = await app.db.get(M, 'limits.value', '-')
        autovalue = await app.db.get(M, 'limits.autovalue', 0)
        
        await msg.edit(
            b("Текущий перевод: \n\n") +
            f"ℹ️ {b('|')} Статус: {b(status)}\n"
            f"⏱ {b('|')} Заддержка: {b(sec_to_str(delay,False))}\n"
            f"📑 {b('|')} Авто-лимит: {b('Выкл' if autovalue==0 else f'каждые {autovalue} {plural(autovalue,plural_raz)}')}\n"
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
            f"⏱ Заддержка на отправку лимитов установлена на {b(pnum(delay))}\n"
            f"Таким темпом,\n"
            f"за {b('час')} ты отправишь {b(f'{60*60/delay:,.0f}')} {plural(int(60*60     /delay), plural_limit)}\n"
            f"за {b(f'день {  60*60*24  /delay:,.0f}'    )} {        plural(int(60*60*24  /delay), plural_limit)}\n"
            f"за {b(f'неделю {60*60*24*7/delay:,.0f}')} {            plural(int(60*60*24*7/delay), plural_limit)}\n"
        )
    except:
        delay = pnum(await app.db.get(M, "limits.delay", 5))
        await msg.edit(
            f'⏱ Текущая заддержка на отправку лимитов: {b(delay)}\n'
            f"Таким темпом,\n"
            f"за {b('час')} ты отправишь {b(f'{60*60/delay:,.0f}')} {plural(int(60*60     /delay), plural_limit)}\n"
            f"за {b(f'день {  60*60*24  /delay:,.0f}'    )} {        plural(int(60*60*24  /delay), plural_limit)}\n"
            f"за {b(f'неделю {60*60*24*7/delay:,.0f}')} {            plural(int(60*60*24*7/delay), plural_limit)}\n"
        )

@cmd(['mlv', 'mlvalue'])
async def _mlvalue(app, msg):
    try: _, value = msg.text.split(maxsplit=1)
    except ValueError: return await msg.edit(f"💵 Текущее значение: {code(await app.db.get(M, 'limits.value', '--'))}")
    await app.db.set(M, 'limits.value', value)
    await msg.edit(f"💵 Значение успешно установлено на {code(value)}")

@cmd(['mla', 'mlautovalue'])
async def _mlautoalue(app, msg):
    autovalue = await app.db.get(M, 'limits.autovalue', 0)
    try: _, value = msg.text.split(maxsplit=1)
    except ValueError: return await msg.edit(f"💵 Текущее значение: {code(autovalue) if autovalue > 0 else b('Выкл')}")
    await app.db.set(M, 'limits.autovalue', int(value))
    await msg.edit(f"💵 Автозначения успешно установлено на каждые {code(value)} {plural(int(value), plural_raz)}")
        

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
    answer = await make_request(app, query, await get_worker_chat(app), timeout=10, additional_filter=filters.user("mine_evo_bot"))
    await msg.edit(f"{SAD} Бот не ответил" if answer is None else layout.format(query, answer.text.html),
        disable_web_page_preview=True
    )

# запрос боту в ЛС
@cmd('bevo')
async def _bevo(app, msg):
    await msg.edit(f'{LOADING} Загрузка...')
    query = msg.text.split(maxsplit=1)[1]
    answer = await make_request(app, query, "mine_evo_bot", timeout=10, additional_filter=filters.user("mine_evo_bot"))
    await msg.edit(f"{SAD} Бот не ответил" if answer is None else layout.format(query, answer.text.html),
        disable_web_page_preview=True
    )

# показать кейсы
@cmd(['mcases', 'мк', 'мкейсы'])
async def _cases(app, msg):
    await msg.edit(f'{LOADING} Загрузка...')
    answer = await make_request(app, 'кейсы', await get_worker_chat(app), '📦 Кейсы игрока', 10)
    await msg.edit(
        f"{SAD} Бот не ответил" if answer is None else split_to(split_to(answer.text.html, '🔥'), 'Открыть'),
        disable_web_page_preview=True
    )

# показать профиль
@cmd(['mprof', 'mp', 'мп', 'мпроф', 'мпрофиль'])
async def _prof(app, msg):
    await msg.edit(f'{LOADING} Загрузка...')
    answer = await make_request(app, 'профиль', await get_worker_chat(app), 'Профиль пользователя', 10)
    await msg.edit(f"{SAD} Бот не ответил" if answer is None else split_to(answer.text.html, '🔥'),
        disable_web_page_preview=True
    )

# показать стату
@cmd(['mstat', 'ms', 'mstats', 'мстата', 'мстат', 'мстатистика'])
async def _stat(app, msg):    
    await msg.edit(f'{LOADING} Загрузка...')
    answer = await make_request(app, 'стата', await get_worker_chat(app), 'Статистика пользователя', 10)
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
    await app.send_message(await get_log_chat(app), "Бью боссиков", message_thread_id=await get_log_chat(app, True))
    
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
    await app.send_message(await get_log_chat(app), "Закончил бить босса", message_thread_id=await get_log_chat(app, True))

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


# лог кейсов, боссов
@Client.on_message(
    filters.chat(['mine_evo_bot', 'mine_evo_gold_bot', 'mine_evo_emerald_bot']) &
    filters.user(['mine_evo_bot', 'mine_evo_gold_bot', 'mine_evo_emerald_bot']) & (
        filters.regex('[✨|😄|📦|🧧|✉️|🌌|💼|👜|🗳|🕋|💎|🎲].*Найден.*') |
        filters.regex('⚡️.*нашел\(ла\).*') |
        filters.regex('🎉 Босс')
    ),
    group=get_group()
)
async def _find_cases(app, msg):
    await msg.copy(await get_log_chat(app), message_thread_id=await get_log_chat(app, True))

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
        await app.send_message(await get_worker_chat(app), 'thx')
        
        await asyncio.sleep(60*5)
    
    
# статистика для кейсов

async def add_stats(app, type, count):
    await app.db.set(
        "MineEVO.stats", type,
        await app.db.get("MineEVO.stats", type, 0) + count
    )
    await app.db.set(
        "MineEVO.stats.all", type,
        await app.db.get("MineEVO.stats.all", type, 0) + count
    )

@Client.on_message(
    filters.chat(dig_bots) &
    ~filters.me &
    filters.regex('[✨|😄|📦|🧧|✉️|🌌|💼|👜|🧳|🗳|🕋|💎|🎲].*Найден.*'), group=get_group())
async def stats_cases(app, msg):
    count_cases = int(msg.text.split()[-1])
    t = msg.text.lower()
    if "редкий конверт"       in t: await add_stats(app, 'ркт', count_cases)
    if "редкий кейс"          in t: await add_stats(app, 'рк' , count_cases)
    if "звездный кейс"        in t: await add_stats(app, 'зв' , count_cases)
    if "мифический кейс"      in t: await add_stats(app, 'миф', count_cases)
    if "кристальный кейс"     in t: await add_stats(app, 'кр' , count_cases)
    if "дайс кейс"            in t: await add_stats(app, 'дк' , count_cases)
    if "кейс"                 in t: await add_stats(app, 'к'  , count_cases)
    if "конверт"              in t: await add_stats(app, 'кт' , count_cases)
    if "сумка с предметами"   in t: await add_stats(app, 'ссп', count_cases)
    if "портфель c эскизами"  in t: await add_stats(app, 'псэ', count_cases)
    if "чемодан c предметами" in t: await add_stats(app, 'чсп', count_cases)


# статистика для плазмы


@Client.on_message(
    filters.chat(dig_bots) &
    ~filters.me &
    filters.regex('Руда на уровень'), group=get_group())
async def plasma_stats(app, msg):
    if 'Плазма' in msg.text:
        await add_stats(app, 'плазма', int(msg.text.split()[2]))
    await app.db.set('MineEVO.stats',     'c', (await app.db.get('MineEVO.stats',     'c', 0)) + 1)
    await app.db.set('MineEVO.stats.all', 'c', (await app.db.get('MineEVO.stats.all', 'c', 0)) + 1)


async def add_stats_boss(app, type, count):
    await app.db.set(
        "MineEVO.stats.bosses", type,
        await app.db.get("MineEVO.stats", type, 0) + count
    )

@Client.on_message(
    filters.chat(["mine_evo_bot"]) &
    ~filters.me &
    filters.regex('[🎉].*Босс.*'), group=get_group())
async def stats_boss(app, msg):
    boss = msg.text.lower().split()
    if "плазма"          in boss: await add_stats_boss(app, 'плазма',   boss[boss.index('плазма')     + 1])
    if "медаль"          in boss: await add_stats_boss(app, 'медаль',   boss[boss.index('медаль')     + 1])
    if "мифический кейс" in boss: await add_stats_boss(app, 'миф',      boss[boss.index('мифический') + 2])
    if "редкий кейс"     in boss: await add_stats_boss(app, 'рк',       boss[boss.index('редкий')     + 2])
    if "кейс"            in boss: await add_stats_boss(app, 'к',        boss[boss.index('кейс')       + 1])
    if "эссенция"        in boss: await add_stats_boss(app, 'эссенция', boss[boss.index('эссенция')   + 1])
    if "скрап"           in boss: await add_stats_boss(app, 'скрап',    boss[boss.index('скрап')      + 1])
    if "нанесено"        in boss: await add_stats_boss(app, 'урон',     boss[boss.index('нанесено')   + 1])
    if "сделано"         in boss: await add_stats_boss(app, 'удары',    boss[boss.index('сделано')    + 1])
