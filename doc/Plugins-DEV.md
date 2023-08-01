# GuguMoe Bot Plugin 开发文档

## 1. 介绍

GuguMoe Bot 使用插件化设计，方便开发者为其添加新功能。这份文档将指导你如何创建一个新插件。

## 2. 插件结构

一个插件由一个 Python 文件构成，必须定义一个继承自 `PluginInterface` 的类，且这个类必须实现 `handle_message` 方法。下面是一个基本的插件文件的结构：

```python
class MyPlugin(PluginInterface):
    command = 'my_command'

    async def handle_message(self, bot, message):
        # TODO: 在此处理所有的文本消息
```

在这个例子中，`MyPlugin` 是插件类的名字，`my_command` 是这个插件的命令。插件类中的 `handle_message` 方法将处理所有的文本消息。

## 3. 命令处理

如果你的插件需要处理特定的命令，你需要在插件类中定义一个 `handle_command` 方法：

```python
class MyPlugin(PluginInterface):
    command = 'my_command'

    async def handle_command(self, bot, message):
        # TODO: 在此处理特定的命令
```

在这个例子中，当用户发送 `/my_command` 时，`handle_command` 方法将被调用。

## 4. 其他消息类型

除了文本消息和命令，GuguMoe Bot 还支持处理其他类型的消息，比如音频、视频、图片等。要处理这些消息，你需要在插件类中定义相应的处理方法，比如 `handle_audio`、`handle_video` 等：

```python
class MyPlugin(PluginInterface):
    async def handle_audio(self, bot, message):
        # TODO: 在此处理音频消息

    async def handle_video(self, bot, message):
        # TODO: 在此处理视频消息
```

这些处理方法将在收到相应类型的消息时被调用。

## 5. 权限检查

如果你希望只有特定的用户可以使用你的插件，你可以在插件的处理方法中添加权限检查：

```python
from gugumoe_bot.settings import settings

class MyPlugin(PluginInterface):
    command = 'my_command'

    async def handle_command(self, bot, message):
        if message.from_user.id in settings.admins:
            # TODO: 在此处理命令
        else:
            await bot.reply_to(message, 'You are not an admin.')
```

在这个例子中，只有在管理员列表中的用户可以使用这个插件。

## 6. 错误处理

你的插件应该能够正确处理可能发生的错误。为了这个目标，你可以使用 Python 的 `try/except` 语句：

```python
class MyPlugin(PluginInterface):
    async def handle_message(self, bot, message):
        try:
            # TODO: 在此处理消息
        except Exception as e:
            await bot.reply_to(message, 'An error occurred.')
```

在这个例子中，如果在处理消息时发生错误，插件将向用户发送一条错误消息。

## 7. 总结

这就是 GuguMoe Bot 插件的基本结构。你可以根据这个指南创建你自己的插件。