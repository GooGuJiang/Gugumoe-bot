from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton

from gugumoe_bot.plugin_interface import PluginInterface


class ButtonsPlugin(PluginInterface):
    command = 'gubuttons'

    async def handle_command(self, bot, message):
        markup = InlineKeyboardMarkup()
        markup.row_width = 2
        markup.add(InlineKeyboardButton("Yes", callback_data="yes"),
                   InlineKeyboardButton("No", callback_data="no"))
        await bot.send_message(message.chat.id, "Do you like this bot?", reply_markup=markup)

    async def handle_callback_query(self, bot, call):
        if call.data == "yes":
            await bot.answer_callback_query(call.id, "That's great!")
        elif call.data == "no":
            await bot.answer_callback_query(call.id, "Oh, sorry to hear that.")
