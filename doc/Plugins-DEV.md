# GuguMoe Bot Plugin 开发文档

## 1. 介绍

为方便开发者为其添加新功能, GuguMoe Bot使用插件化设计. 这份文档将指导你如何为GuguMoe创建一个新插件.

**注意**
程序本体基于[pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI)运行, 关于数据类型以及其它方法的使用,
请参考[官方文档](https://pytba.readthedocs.io/en/latest/index.html), 这里只做简单的介绍以及GuguMoe本地化说明

## 2. 插件结构

一个插件由一个 **Python文件** 构成,其必须包含一个继承自 `PluginInterface` 的类,且实现 `handle_message`
方法.下面是一个基本的插件文件的结构：

```python
class MyPlugin(PluginInterface):
    command = 'my_command'

    async def handle_message(self, bot, message):
        # TODO: 在此处理所有的文本消息
```

在这个例子中,`MyPlugin` 是插件类的名字,`my_command` 是此插件的命令.

**注意** 请将插件放至 `gugumoe_bot\plugins` 文件夹中

## 3. 命令处理

`handle_command`方法是整个插件的入口, 你可以在这里引用你的数据逻辑

```python
class MyPlugin(PluginInterface):
    command = 'my_command'

    async def handle_command(self, bot, message):
        # TODO: 在此处理特定的命令
```

当用户发送 `/my_command` 时,`handle_command` 方法将被调用.

## 4. 其他消息类型

处理其他类型的消息时,比如 音频|视频|图片, 你需要定义相应的处理方法,比如 `handle_audio`|`handle_video`
等：

```python
class MyPlugin(PluginInterface):
    async def handle_audio(self, bot, message):
        # TODO: 在此处理音频消息

    async def handle_video(self, bot, message):
        # TODO: 在此处理视频消息
```

这些处理方法将在收到相应类型的消息时被调用.

## 5. 权限检查

如果你希望只有特定的用户可以使用你的插件,你可以在插件的处理方法中添加权限检查：

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

在这个例子中,只有管理员可以使用这个插件.

## 6. 错误处理

由于Async方法的原因, 某些错误发生时并不会影响到主程序, 因此你的插件应当自主发现并处理错误信息, 你可以使用 Python
的 `try/except` 语句：

```python
class MyPlugin(PluginInterface):
    async def handle_message(self, bot, message):
        try:
        # TODO: 在此处理消息
        except Exception as e:
            await bot.reply_to(message, 'An error occurred.')
```