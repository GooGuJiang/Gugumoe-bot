import sys

from telebot.async_telebot import AsyncTeleBot
from telebot.types import Message, CallbackQuery
import asyncio
from telebot import asyncio_helper
from gugumoe_bot.settings import settings
import os
import importlib
from loguru import logger

# 插件目录
PLUGIN_DIR = 'plugins'

# 初始化 TeleBot
asyncio_helper.proxy = settings.proxy
bot = AsyncTeleBot(settings.token)

# 设置日志格式和级别
logger.add(sys.stderr, level=settings.log_level)

# 动态加载插件
plugins = []
for filename in os.listdir(os.path.join(os.path.dirname(__file__), PLUGIN_DIR)):
    if filename.endswith('.py'):
        module_name = filename[:-3]
        module = importlib.import_module(f'.{PLUGIN_DIR}.{module_name}', 'gugumoe_bot')
        plugin_class = getattr(module, f'{module_name.capitalize()}Plugin')
        plugins.append(plugin_class())
        logger.info(f'Loaded plugin: {module_name}')

logger.info('All plugins loaded, bot is starting...')


# Handle all text messages
@bot.message_handler(func=lambda m: True)
async def handle_all_text_messages(message: Message) -> None:
    if message.text.startswith('/'):
        command = message.text.split(' ', 1)[0][1:]
        for plugin in plugins:
            if plugin.command == command:
                logger.info(f'Handling command: {command}')
                await plugin.handle_command(bot, message)
    else:
        for plugin in plugins:
            await plugin.handle_message(bot, message)


@bot.callback_query_handler(func=lambda call: True)
async def handle_callback_query(call: CallbackQuery) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_callback_query'):
            await plugin.handle_callback_query(bot, call)


@bot.message_handler(content_types=['audio'])
async def handle_audio(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_audio'):
            await plugin.handle_audio(bot, message)


@bot.message_handler(content_types=['video'])
async def handle_video(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_video'):
            await plugin.handle_video(bot, message)


@bot.message_handler(content_types=['photo'])
async def handle_photo(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_photo'):
            await plugin.handle_photo(bot, message)


@bot.message_handler(content_types=['document'])
async def handle_document(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_document'):
            await plugin.handle_document(bot, message)


@bot.message_handler(content_types=['sticker'])
async def handle_sticker(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_sticker'):
            await plugin.handle_sticker(bot, message)


@bot.message_handler(content_types=['voice'])
async def handle_voice(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_voice'):
            await plugin.handle_voice(bot, message)


@bot.message_handler(content_types=['video_note'])
async def handle_video_note(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_video_note'):
            await plugin.handle_video_note(bot, message)


@bot.message_handler(content_types=['contact'])
async def handle_contact(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_contact'):
            await plugin.handle_contact(bot, message)


@bot.message_handler(content_types=['location'])
async def handle_location(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_location'):
            await plugin.handle_location(bot, message)


@bot.message_handler(content_types=['venue'])
async def handle_venue(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_venue'):
            await plugin.handle_venue(bot, message)


@bot.message_handler(content_types=['poll'])
async def handle_poll(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_poll'):
            await plugin.handle_poll(bot, message)


@bot.message_handler(content_types=['dice'])
async def handle_dice(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_dice'):
            await plugin.handle_dice(bot, message)


@bot.message_handler(content_types=['new_chat_members'])
async def handle_new_chat_members(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_new_chat_members'):
            await plugin.handle_new_chat_members(bot, message)


@bot.message_handler(content_types=['left_chat_member'])
async def handle_left_chat_member(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_left_chat_member'):
            await plugin.handle_left_chat_member(bot, message)


@bot.message_handler(content_types=['new_chat_title'])
async def handle_new_chat_title(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_new_chat_title'):
            await plugin.handle_new_chat_title(bot, message)


@bot.message_handler(content_types=['new_chat_photo'])
async def handle_new_chat_photo(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_new_chat_photo'):
            await plugin.handle_new_chat_photo(bot, message)


@bot.message_handler(content_types=['delete_chat_photo'])
async def handle_delete_chat_photo(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_delete_chat_photo'):
            await plugin.handle_delete_chat_photo(bot, message)


@bot.message_handler(content_types=['group_chat_created'])
async def handle_group_chat_created(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_group_chat_created'):
            await plugin.handle_group_chat_created(bot, message)


@bot.message_handler(content_types=['supergroup_chat_created'])
async def handle_supergroup_chat_created(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_supergroup_chat_created'):
            await plugin.handle_supergroup_chat_created(bot, message)


@bot.message_handler(content_types=['channel_chat_created'])
async def handle_channel_chat_created(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_channel_chat_created'):
            await plugin.handle_channel_chat_created(bot, message)


@bot.message_handler(content_types=['migrate_to_chat_id'])
async def handle_migrate_to_chat_id(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_migrate_to_chat_id'):
            await plugin.handle_migrate_to_chat_id(bot, message)


@bot.message_handler(content_types=['migrate_from_chat_id'])
async def handle_migrate_from_chat_id(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_migrate_from_chat_id'):
            await plugin.handle_migrate_from_chat_id(bot, message)


@bot.message_handler(content_types=['pinned_message'])
async def handle_pinned_message(message: Message) -> None:
    for plugin in plugins:
        if hasattr(plugin, 'handle_pinned_message'):
            await plugin.handle_pinned_message(bot, message)


# Start the bot
asyncio.run(bot.polling())
logger.info('Bot has started.')
