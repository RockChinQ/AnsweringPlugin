import os
import shutil
import json

import yaml
import requests

from pkg.plugin.models import *
from pkg.plugin.host import EventContext, PluginHost


# 注册插件
@register(name="AnsweringPlugin", description="使用RockChinQ/llm-embed-qa作为后端，回答特定领域问题", version="0.1", author="RockChinQ")
class AnsweringPlugin(Plugin):

    cfg: dict

    # 插件加载时触发
    # plugin_host (pkg.plugin.host.PluginHost) 提供了与主程序交互的一些方法，详细请查看其源码
    def __init__(self, plugin_host: PluginHost):
        # 检查是否有answer.yaml文件
        if not os.path.exists("answer.yaml"):
            shutil.copyfile("plugins/AnsweringPlugin/config-template.yaml", "answer.yaml")
            logging.info("AnsweringPlugin: 未找到answer.yaml文件，已自动创建，请修改后重启程序")
            return
        
        # 读取answer.yaml文件
        with open("answer.yaml", "r", encoding="utf-8") as f:
            self.cfg = yaml.load(f, Loader=yaml.FullLoader)
        
    @on(GroupNormalMessageReceived)
    @on(PersonNormalMessageReceived)
    def _(self, event: EventContext, **kwargs):
        content = kwargs['text_message']
        
        resp = requests.get(
            url=self.cfg['endpoint']+"/ask",
            params={
                "content": content,
                "strict": 'true'
            },
            timeout=300
        )
        
        json_data = json.loads(resp.text)
        
        if len(json_data['doc_names']) > 0:
            event.prevent_default()
            event.prevent_postorder()

            logging.info("使用以下文档生成的回答：{}".format(json_data['doc_names']))
            
            event.add_return(
                "reply",
                [json_data['message']]
            )
        else: # 没有找到相关资料
            if self.cfg['skip_if_not_found']:
                
                if 'skip_tips' in self.cfg and self.cfg['skip_tips'] != "":
                    event.add_return(
                        "reply",
                        [self.cfg['skip_tips']]
                    )
                event.prevent_default()
                event.prevent_postorder()

    # 插件卸载时触发
    def __del__(self):
        pass
