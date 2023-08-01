from typing import Any

from telebot.types import Message, CallbackQuery


class PluginInterface:
    command: str = None

    async def handle_message(self, bot: Any, message: Message) -> None:
        pass

    async def handle_command(self, bot: Any, message: Message) -> None:
        pass

    async def handle_callback_query(self, bot: Any, call: CallbackQuery) -> None:
        pass

    async def handle_audio(self, bot: Any, message: Message) -> None:
        pass

    async def handle_video(self, bot: Any, message: Message) -> None:
        pass

    async def handle_photo(self, bot: Any, message: Message) -> None:
        pass

    async def handle_document(self, bot: Any, message: Message) -> None:
        pass

    async def handle_sticker(self, bot: Any, message: Message) -> None:
        pass

    async def handle_voice(self, bot: Any, message: Message) -> None:
        pass

    async def handle_video_note(self, bot: Any, message: Message) -> None:
        pass

    async def handle_contact(self, bot: Any, message: Message) -> None:
        pass

    async def handle_location(self, bot: Any, message: Message) -> None:
        pass

    async def handle_venue(self, bot: Any, message: Message) -> None:
        pass

    async def handle_poll(self, bot: Any, message: Message) -> None:
        pass

    async def handle_dice(self, bot: Any, message: Message) -> None:
        pass

    async def handle_new_chat_members(self, bot: Any, message: Message) -> None:
        pass

    async def handle_left_chat_member(self, bot: Any, message: Message) -> None:
        pass

    async def handle_new_chat_title(self, bot: Any, message: Message) -> None:
        pass

    async def handle_new_chat_photo(self, bot: Any, message: Message) -> None:
        pass

    async def handle_delete_chat_photo(self, bot: Any, message: Message) -> None:
        pass

    async def handle_group_chat_created(self, bot: Any, message: Message) -> None:
        pass

    async def handle_supergroup_chat_created(self, bot: Any, message: Message) -> None:
        pass

    async def handle_channel_chat_created(self, bot: Any, message: Message) -> None:
        pass

    async def handle_migrate_to_chat_id(self, bot: Any, message: Message) -> None:
        pass

    async def handle_migrate_from_chat_id(self, bot: Any, message: Message) -> None:
        pass

    async def handle_pinned_message(self, bot: Any, message: Message) -> None:
        pass
