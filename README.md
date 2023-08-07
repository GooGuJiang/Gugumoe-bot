# Gugumoe-bot

<div align="center">

<img src="https://www.gmoe.cc/wp-content/uploads/2023/08/d9a87c4686590512168d06bbcb9ae3bc.png" width="150" style="border-radius: 30px"/>

这是咕谷酱的Telegram机器人 (咕小酱)。是基于 [pyTelegramBotAPI](https://github.com/eternnoir/pyTelegramBotAPI) 的一个 Python 机器人。

~~同时会有一堆运行Bug~~

**咕小酱在这呢👉[@gugumoe_bot](http://t.me/gugumoe_bot)**

<a href="https://count.getloli.com"><img align="center" src="https://count.getloli.com/get/@Gugumoe-bot"></a><br>

![Alt](https://repobeats.axiom.co/api/embed/1931234205856e05e4269eba31551c98b6eb632c.svg "Repobeats analytics image")

## **⚠️项目正在重构**

</div>

## 部署

咕小酱 提供了多种部署方式，你可以根据自己的需求选择合适的部署方式。

### 本地部署

本项目使用 [Python](https://www.python.org/) 和 [poetry](https://python-poetry.org/)。请确保你本地安装了它们，当然你也可以选择其他部署方式。

注意：需要 Python 3.10 或以上版本。

```sh
# 检查 Python 版本
$ python --version

# 如果你还未安装 Poetry，使用下列命令进行安装
$ curl -sSL https://install.python-poetry.org | python -
```

首先，克隆并进入项目：

```sh
$ git clone https://github.com/GooGuJiang/Gugumoe-bot.git
$ cd Gugumoe-bot
```

使用 poetry 安装项目依赖：

```sh
$ poetry install
```

## 使用说明

使用 Gugumoe-bot，你首先需要在本地运行它。使用以下命令启动 Gugumoe-bot：

```sh
$ poetry run python -m gugumoe_bot
```

在 Telegram 中，你可以使用 `@gugumoe_bot` 来与 Gugumoe-bot 互动。

## 插件开发

你可以参考[插件开发文档](./doc/Plugins-DEV.md)来创建你自己的插件，以扩展 Gugumoe-bot 的功能。

## 项目状态

此项目正在进行重构。在重构期间可能会出现一些问题。我们将尽快解决这些问题。

## 开源许可

此项目遵循 [MIT](https://opensource.org/licenses/MIT) 开源许可协议。