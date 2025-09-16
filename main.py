import telebot
from telebot import types

from bg import solve_equation, solve_inequality, solve_system

TOKEN = "8490027010:AAGe6xBYqf395tnLcurJ_lBQ5rocK-wQg90"
bot = telebot.TeleBot(TOKEN)
user_states = {}


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Обычное", callback_data="default")
    button2 = types.InlineKeyboardButton(
        "Неравенство", callback_data="inequality")
    button3 = types.InlineKeyboardButton("Система", callback_data="system")
    markup.row(button1, button2, button3)
    bot.send_message(
        message.chat.id,
        "Привет, {0.first_name}! Я вспомогательный бот, который поможет тебе решать уравнения. Выбери тип уравнения, который ты хочешь решить".format(
            message.from_user),
        reply_markup=markup
    )


@bot.callback_query_handler(func=lambda callback: True)
def callback_message(callback):
    if callback.data == 'default':
        bot.answer_callback_query(callback.id)
        msg = bot.send_message(
            callback.message.chat.id,
            "Введите уравнение и переменную, которую нужно найти, через запятую.\nПример: x^2 = 9, x"
        )
        user_states[callback.from_user.id] = 'waiting_equation'

    if callback.data == 'inequality':
        bot.answer_callback_query(callback.id)
        msg = bot.send_message(
            callback.message.chat.id,
            "Введите уравнение и переменную, которую нужно найти, через запятую.\nПример: x^2 <= 9, x"
        )
        user_states[callback.from_user.id] = 'waiting_inequality'
        
    if callback.data == 'system':
        bot.answer_callback_query(callback.id)
        msg = bot.send_message(
            callback.message.chat.id,
            """Введите уравнения на разных строках, а затем, на последней строке, укажите переменные уравнений через запятую. Пример:
x + y = 5
2*x - y = 1
x, y"""
        )
        user_states[callback.from_user.id] = 'waiting_system'

@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_equation')
def handle_equation(message):
    user_states.pop(message.from_user.id, None)
    try:
        answer = message.text.split(",")
        if len(answer) == 2:
            eq, var = answer
        else:
            eq, var = answer[0], "x"

        eq = eq.replace("^", "**")
        solution = solve_equation(eq, var)
        out = [f"{var}{i} = {x}".lstrip()
            for i, x in zip(list(range(len(solution))), solution)]
        print(out)

        bot.send_message(message.chat.id, "\n".join(out))
    except Exception:
        bot.send_message(message.chat.id, 'Неверный формат ввода')
    send_main_message(message)


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_inequality')
def handle_inequality(message):
    user_states.pop(message.from_user.id, None)
    try:
        answer = message.text.split(",")
        if len(answer) == 2:
            eq, var = answer
        else:
            eq, var = answer[0], "x"

        eq = eq.replace("^", "**")
        out = solve_inequality(eq, var)
        bot.send_message(message.chat.id, out)
    except Exception:
        bot.send_message(message.chat.id, 'Неверный формат ввода')
    send_main_message(message)


@bot.message_handler(func=lambda message: user_states.get(message.from_user.id) == 'waiting_system')
def handle_system(message):
    user_states.pop(message.from_user.id, None)
    try:
        answer = message.text.split("\n")
        equations = [i.strip() for i in answer[:-1]]
        variables = answer[-1].strip().split(", ")
        solution = solve_system(equations, variables)
        out = [f"{i} = {solution[i]}" for i in solution]
        bot.send_message(message.chat.id, "\n".join(out))
    except Exception:
        bot.send_message(message.chat.id, 'Неверный формат ввода')
    send_main_message(message)
    

def send_main_message(message):
    markup = types.InlineKeyboardMarkup()
    button1 = types.InlineKeyboardButton("Обычное", callback_data="default")
    button2 = types.InlineKeyboardButton(
        "Неравенство", callback_data="inequality")
    button3 = types.InlineKeyboardButton("Система", callback_data="system")
    markup.row(button1, button2, button3)
    bot.send_message(
        message.chat.id, "Хотите решить другое уравнения?", reply_markup=markup)


bot.polling(non_stop=True, interval=0)
