# Answering Plugin

回答特定领域问题，搭配[llm-embed-qa](https://github.com/RockChinQ/llm-embed-qa)使用。

## 安装

配置好 QChatGPT 和 llm-embed-qa 程序后，使用 QChatGPT 的管理员 QQ 向机器人发送以下命令安装插件：
```
!plugin get https://github.com/RockChinQ/AnsweringPlugin
```

重启后，修改 QChatGPT 目录下的 `answer.yaml`，按照注释修改配置文件

## 使用

每次获得用户提问时，都会向 llm-embed-qa 获取回复。
