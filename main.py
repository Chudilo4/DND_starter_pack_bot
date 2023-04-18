import logging
import re

from telegram import Update, InlineKeyboardButton, \
    InlineKeyboardMarkup
from telegram.ext import CommandHandler, ContextTypes, \
    ConversationHandler, CallbackQueryHandler, Application
import sqlite3

con = sqlite3.connect("dnd.db")

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

cur = con.cursor()

# Stages
START_ROUTES, END_ROUTES = range(0, 2)


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Send message on `/start`."""
    user = update.message.from_user
    logging.info("User %s started the conversation.", user.first_name)
    keyboard = [
        [
            InlineKeyboardButton("Магазин", callback_data='shop'),
            InlineKeyboardButton("Таверна", callback_data='tavern'),
            InlineKeyboardButton("Магия", callback_data='magic'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_text("Что вам нужно?", reply_markup=reply_markup)
    return START_ROUTES


async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Выводим пользователю меню что он может купить"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Доспехи", callback_data="armor"),
            InlineKeyboardButton('Оружие', callback_data='weapon'),
            InlineKeyboardButton('Снаряжение', callback_data='equipment'),
            InlineKeyboardButton('Назад', callback_data="hub"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Доспехи и оружие в Магазин Львиный щит Снаряжение в Припасы Бартена?", reply_markup=reply_markup
    )
    return START_ROUTES


async def hub(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton("Магазин", callback_data='shop'),
            InlineKeyboardButton("Таверна", callback_data='tavern'),
            InlineKeyboardButton("Магия", callback_data='magic'),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Что вам нужно?", reply_markup=reply_markup
    )
    return START_ROUTES


async def armor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Легкие', callback_data="light_armor"),
            InlineKeyboardButton('Средние', callback_data="medium_armor"),
            InlineKeyboardButton('Тяжелые', callback_data="heavy_armor"),
            InlineKeyboardButton('Назад', callback_data="shop"),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Список доступных достпехов для покупки", reply_markup=reply_markup
    )
    return START_ROUTES


async def weapon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем выбор оружия"
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Простое рукопашное оружие', callback_data="simple_melee_weapon"),
        ],
        [
            InlineKeyboardButton('Простое дальнобойное оружие', callback_data="simple_ranged_weapon")
        ],
        [
            InlineKeyboardButton('Воинское рукопашное оружие', callback_data="military_melee_weapon"),
        ],
        [
            InlineKeyboardButton('Воинское дальнобойное оружие', callback_data="military_ranged_weapon")
        ],
        [
            InlineKeyboardButton('Назад', callback_data="shop")
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text="Список доступного оружия для покупки", reply_markup=reply_markup
    )
    return START_ROUTES


async def equipment(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    res = cur.execute("SELECT * FROM equipment")
    l = [f'Название: {i[1]}\nСтоимость: {i[2]}\nВес: {i[3]}' for i in res.fetchall()]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data="shop"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='\n_____\n'.join(l), reply_markup=reply_markup
    )
    return START_ROUTES


async def tavern(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Вывод что можно сделать в таверне"""
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Еда', callback_data="food"),
            InlineKeyboardButton('Постой', callback_data="rooming"),
            InlineKeyboardButton('Назад', callback_data="hub"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Постоялый двор Стоунхилл', reply_markup=reply_markup
    )
    return START_ROUTES


async def rooming(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    res = cur.execute("SELECT * FROM room_tavern")
    l = [f'Название: {i[1]}\nСтоимость: {i[2]}' for i in res.fetchall()]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data="tavern"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='\n_____\n'.join(l), reply_markup=reply_markup
    )
    return START_ROUTES


async def food(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Show new choice of buttons"""
    query = update.callback_query
    res = cur.execute("SELECT * FROM food")
    l = [f'Название: {i[1]}\nСтоимость: {i[2]}' for i in res.fetchall()]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data="tavern"),
        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='\n_____\n'.join(l), reply_markup=reply_markup
    )
    return START_ROUTES


async def light_armor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем выбор легкой брони"
    query = update.callback_query
    res = cur.execute("SELECT * FROM light_armor")
    l = [f'Название: {i[1]}\nСтоимость: {i[2]}\nКласс Доспеха (КД): {i[3]}\nВес: {i[4]}' for i in res.fetchall()]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data="armor"),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='\n_____\n'.join(l), reply_markup=reply_markup
    )
    return START_ROUTES


async def medium_armor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем выбор легкой брони"
    query = update.callback_query
    res = cur.execute("SELECT * FROM medium_armor")
    l = [f'Название: {i[1]},\nСтоимость: {i[2]},\nКласс Доспеха (КД): {i[3]},\nВес: {i[4]}' for i in res.fetchall()]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data="armor"),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='\n_____\n'.join(l), reply_markup=reply_markup
    )
    return START_ROUTES


async def heavy_armor(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем выбор легкой брони"
    query = update.callback_query
    res = cur.execute("SELECT * FROM heavy_armor")
    l = [f'Название: {i[1]},\nСтоимость: {i[2]},\nКласс Доспеха (КД): {i[3]},\nВес: {i[4]}' for i in res.fetchall()]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data="armor"),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='\n_____\n'.join(l), reply_markup=reply_markup
    )
    return START_ROUTES


async def simple_melee_weapon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем выбор легкой брони"
    query = update.callback_query
    res = cur.execute("SELECT * FROM simple_melee_weapon")
    l = [f'Название: {i[1]},\nСтоимость: {i[2]},\nУрон: {i[3]},\nВес: {i[4]},\nСвойства: {i[5]}' for i in
         res.fetchall()]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data="weapon"),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='\n_____\n'.join(l), reply_markup=reply_markup
    )
    return START_ROUTES


async def simple_ranged_weapon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем выбор легкой брони"
    query = update.callback_query
    res = cur.execute("SELECT * FROM simple_ranged_weapon")
    l = [f'Название: {i[1]},\nСтоимость: {i[2]},\nУрон: {i[3]},\nВес: {i[4]},\nСвойства: {i[5]}' for i in
         res.fetchall()]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data="weapon"),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='\n_____\n'.join(l), reply_markup=reply_markup
    )
    return START_ROUTES


async def military_melee_weapon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем выбор легкой брони"
    query = update.callback_query
    res = cur.execute("SELECT * FROM military_melee_weapon")
    l = [f'Название: {i[1]},\nСтоимость: {i[2]},\nУрон: {i[3]},\nВес: {i[4]},\nСвойства: {i[5]}' for i in
         res.fetchall()]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data="weapon"),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='\n_____\n'.join(l), reply_markup=reply_markup
    )
    return START_ROUTES


async def military_ranged_weapon(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем выбор легкой брони"
    query = update.callback_query
    res = cur.execute("SELECT * FROM military_ranged_weapon")
    l = [f'Название: {i[1]},\nСтоимость: {i[2]},\nУрон: {i[3]},\nВес: {i[4]},\nСвойства: {i[5]}' for i in
         res.fetchall()]
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data="weapon"),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='\n_____\n'.join(l), reply_markup=reply_markup
    )
    return START_ROUTES


async def magic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем выбор персонажей"
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Волшебник', callback_data="wizard"),
            InlineKeyboardButton('Жрец', callback_data="priest"),
            InlineKeyboardButton('Назад', callback_data="hub"),

        ]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите кого вы используете', reply_markup=reply_markup
    )
    return START_ROUTES


async def wizard(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем выбор персонажей"
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Заговоры (0 уровень)', callback_data="magic_wizard_level_zero"),
        ],
        [
            InlineKeyboardButton('1 уровень', callback_data="magic_wizard_level_one"),
        ],
        [
            InlineKeyboardButton('2 уровень', callback_data="magic_wizard_level_two"),
        ],
        [
            InlineKeyboardButton('3 уровень', callback_data="magic_wizard_level_third"),
        ],
        [
            InlineKeyboardButton('Назад', callback_data="magic"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите уровень круга магии', reply_markup=reply_markup
    )
    return START_ROUTES


async def priest(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем уровни заклинаний"
    query = update.callback_query
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Заговоры (0 уровень)', callback_data="magic_priest_level_zero"),
        ],
        [
            InlineKeyboardButton('1 уровень', callback_data="magic_priest_level_one"),
        ],
        [
            InlineKeyboardButton('2 уровень', callback_data="magic_priest_level_two"),
        ],
        [
            InlineKeyboardButton('3 уровень', callback_data="magic_priest_level_third"),
        ],
        [
            InlineKeyboardButton('Назад', callback_data="magic"),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите уровень круга магии', reply_markup=reply_markup
    )
    return START_ROUTES


async def magic_wizard_level_third(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем заклинания 3 уровня"
    query = update.callback_query
    l = ('Защита от энергии',
         'Молния',
         'Огненный шар',
         'Полёт',
         'Рассеивание магии',)
    res = cur.execute(f"SELECT * FROM magic WHERE title in {l}")
    q = res.fetchall()
    await query.answer()
    keyboard = [[InlineKeyboardButton(f'{i[1]}', callback_data=f"magic/{i[0]}")] for i in q]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите магию', reply_markup=reply_markup
    )
    return START_ROUTES


async def magic_priest_level_third(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем заклинания 3 уровня"
    query = update.callback_query
    l = ('Возрождение',
         'Духовные стражи',
         'Защита от энергии',
         'Маяк надежды',
         'Множественное лечащее слово',
         'Рассеивание магии')
    res = cur.execute(f"SELECT * FROM magic WHERE title in {l}")
    q = res.fetchall()
    await query.answer()
    keyboard = [[InlineKeyboardButton(f'{i[1]}', callback_data=f"magic/{i[0]}")] for i in q]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите магию', reply_markup=reply_markup
    )
    return START_ROUTES


async def magic_wizard_level_two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем заклинания 2 уровня"
    query = update.callback_query
    l = ('Внушение',
         'Невидимость',
         'Паук',
         'Паутина',
         'Пылающий шар',
         'Размытый образ',
         'Туманный шаг',
         'Тьма',
         'Удержание личности',)
    res = cur.execute(f"SELECT * FROM magic WHERE title in {l}")
    q = res.fetchall()
    await query.answer()
    keyboard = [[InlineKeyboardButton(f'{i[1]}', callback_data=f"magic/{i[0]}")] for i in q]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите магию', reply_markup=reply_markup
    )
    return START_ROUTES


async def magic_priest_level_two(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем заклинания 2 уровня"
    query = update.callback_query
    l = ('Божественное оружие',
         'Гадание',
         'Малое восстановление',
         'Молебен лечения',
         'Охраняющая связь',
         'Подмога',
         'Тишина',
         'Удержание личности')
    res = cur.execute(f"SELECT * FROM magic WHERE title in {l}")
    q = res.fetchall()
    await query.answer()
    keyboard = [[InlineKeyboardButton(f'{i[1]}', callback_data=f"magic/{i[0]}")] for i in q]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите магию', reply_markup=reply_markup
    )
    return START_ROUTES


async def magic_wizard_level_one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем заклинания 1 уровня"
    query = update.callback_query
    l = ('Волна грома',
         'Волшебная стрела',
         'Доспехи мага',
         'Обнаружение магии',
         'Огненные ладони',
         'Опознание',
         'Очарование личности',
         'Понимание языков',
         'Усыпление',
         'Щит')
    res = cur.execute(f"SELECT * FROM magic WHERE title in {l}")
    q = res.fetchall()
    await query.answer()
    keyboard = [[InlineKeyboardButton(f'{i[1]}', callback_data=f"magic/{i[0]}")] for i in q]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите магию', reply_markup=reply_markup
    )
    return START_ROUTES


async def magic_priest_level_one(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем заклинания 1 уровня"
    query = update.callback_query
    l = ('Благословение',
         'Лечащее слово',
         'Лечение ран',
         'Нанесение ран',
         'Направленный снаряд',
         'Обнаружение магии',
         'Приказ',
         'Убежище',
         'Щит веры')
    res = cur.execute(f"SELECT * FROM magic WHERE title in {l}")
    q = res.fetchall()
    await query.answer()
    keyboard = [[InlineKeyboardButton(f'{i[1]}', callback_data=f"magic/{i[0]}")] for i in q]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите магию', reply_markup=reply_markup
    )
    return START_ROUTES


async def magic_wizard_level_zero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем заклинания 0 уровня"
    query = update.callback_query
    l = ('Волшебная рука',
         'Луч холода',
         'Пляшущие огоньки',
         'Cвет',
         "Фокусы",
         "Электрошок")
    res = cur.execute(f"SELECT * FROM magic WHERE title in {l}")
    q = res.fetchall()
    await query.answer()
    keyboard = [[InlineKeyboardButton(f'{i[1]}', callback_data=f"magic/{i[0]}")] for i in q]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите магию', reply_markup=reply_markup
    )
    return START_ROUTES


async def magic_priest_level_zero(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем заклинания 0 уровня"
    query = update.callback_query
    l = ('Свет',
         'Священное пламя',
         'Сопротивление',
         'Указание',
         'Чудотворство')
    res = cur.execute(f"SELECT * FROM magic WHERE title in {l}")
    q = res.fetchall()
    await query.answer()
    keyboard = [[InlineKeyboardButton(f'{i[1]}', callback_data=f"magic/{i[0]}")] for i in q]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await query.edit_message_text(
        text='Выберите магию', reply_markup=reply_markup
    )
    return START_ROUTES


async def search_magic(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    "Возвращаем заклинания 0 уровня"
    query = update.callback_query
    r = re.findall(r'\d{1,}', query.data)
    cur.execute(f"SELECT * FROM magic WHERE id={r[0]}")
    match = cur.fetchone()
    await query.answer()
    keyboard = [
        [
            InlineKeyboardButton('Назад', callback_data='hub'),
        ],
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    txt = f"Название: {match[1]},\n" \
          f"Тип магии : {match[2]},\n{match[3]},\n" \
          f"{match[4]},\n{match[5]},\n{match[6]},\n" \
          f"Описание: {match[7]}"
    await query.edit_message_text(
        text=txt, reply_markup=reply_markup
    )
    return START_ROUTES


async def end(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    """Returns `ConversationHandler.END`, which tells the
    ConversationHandler that the conversation is over.
    """
    query = update.callback_query
    await query.answer()
    await query.edit_message_text(text="See you next time!")
    return ConversationHandler.END


async def callback_timer(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.message.chat_id
    await context.bot.send_message(chat_id=chat_id, text='Вам пришла новая заявка')


def main() -> None:
    """Run the bot."""
    application = Application.builder().token("5818251636:AAFIOC9Q3u3Q7cfMms0KqWcuhWXZUZTibE8").build()
    timer_handler = CommandHandler('timer', callback_timer)
    application.add_handler(timer_handler)
    conv_handler = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            START_ROUTES: [
                CallbackQueryHandler(shop, pattern="^" + 'shop' + "$"),
                CallbackQueryHandler(armor, pattern="^" + "armor" + "$"),
                CallbackQueryHandler(weapon, pattern="^" + "weapon" + "$"),
                CallbackQueryHandler(equipment, pattern="^" + "equipment" + "$"),
                CallbackQueryHandler(light_armor, pattern="^" + "light_armor" + "$"),
                CallbackQueryHandler(medium_armor, pattern="^" + "medium_armor" + "$"),
                CallbackQueryHandler(heavy_armor, pattern="^" + "heavy_armor" + "$"),
                CallbackQueryHandler(simple_melee_weapon, pattern="^" + "simple_melee_weapon" + "$"),
                CallbackQueryHandler(simple_ranged_weapon, pattern="^" + "simple_ranged_weapon" + "$"),
                CallbackQueryHandler(military_melee_weapon, pattern="^" + "military_melee_weapon" + "$"),
                CallbackQueryHandler(military_ranged_weapon, pattern="^" + "military_ranged_weapon" + "$"),
                CallbackQueryHandler(tavern, pattern="^" + "tavern" + "$"),
                CallbackQueryHandler(food, pattern="^" + "food" + "$"),
                CallbackQueryHandler(rooming, pattern="^" + "rooming" + "$"),
                CallbackQueryHandler(hub, pattern="^" + 'hub' + "$"),
                CallbackQueryHandler(magic, pattern="^" + 'magic' + "$"),
                CallbackQueryHandler(wizard, pattern="^" + 'wizard' + "$"),
                CallbackQueryHandler(priest, pattern="^" + 'priest' + "$"),
                CallbackQueryHandler(magic_wizard_level_zero, pattern="^" + 'magic_wizard_level_zero' + "$"),
                CallbackQueryHandler(magic_wizard_level_one, pattern="^" + 'magic_wizard_level_one' + "$"),
                CallbackQueryHandler(magic_wizard_level_two, pattern="^" + 'magic_wizard_level_two' + "$"),
                CallbackQueryHandler(magic_wizard_level_third, pattern="^" + 'magic_wizard_level_third' + "$"),
                CallbackQueryHandler(magic_priest_level_zero, pattern="^" + 'magic_priest_level_zero' + "$"),
                CallbackQueryHandler(magic_priest_level_one, pattern="^" + 'magic_priest_level_one' + "$"),
                CallbackQueryHandler(magic_priest_level_two, pattern="^" + 'magic_priest_level_two' + "$"),
                CallbackQueryHandler(magic_priest_level_third, pattern="^" + 'magic_priest_level_third' + "$"),
                CallbackQueryHandler(search_magic, pattern="^" + 'magic/' + '\d{1,}' + "$"),
            ],
            END_ROUTES: [
                # CallbackQueryHandler(start_over, pattern="^" + str(ONE) + "$"),
                CallbackQueryHandler(end, pattern="^" + 'end' + "$"),
            ],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    # Add ConversationHandler to application that will be used for handling updates
    application.add_handler(conv_handler)
    # job_queue = application.job_queue
    # job_queue.run_repeating(callback_minute, interval=60, first=10)

    # Run the bot until the user presses Ctrl-C
    application.run_polling()


if __name__ == "__main__":
    main()

