import json
import os
import sys
import types
import time
import requests

from volcenginesdkarkruntime import Ark
from openai import OpenAI
from tencentcloud.common import credential
from tencentcloud.hunyuan.v20230901 import hunyuan_client, models
from zhipuai import ZhipuAI
import sensenova
import hashlib

deepseek_answer_model = "deepseek-chat"

def deepseek_answer_x(question, knowledge_base, stream):

    client = OpenAI(
        api_key=os.getenv("DeepSeek_API_Key"),
        base_url="https://api.deepseek.com",
    )

    completion = client.chat.completions.create(
        model=deepseek_answer_model,
        messages=message_write(question, "deepseek"),
        stream=stream,
        stream_options={"include_usage": True}
        #temperature=0.8,
        #top_p=0.8
    )

    if stream:
        result = ""
        for chunk in completion:
            if chunk.choices == []:
                usage = chunk.usage
                break
            elif chunk.choices[0].delta.content:   #有个空值的结束标记，所以要判断
                delta = chunk.choices[0].delta.content
                result = result + delta
                sys.stdout.write(delta)
        usage = chunk.usage
    else:
        result = completion.choices[0].message.content
        usage = completion.usage
        sys.stdout.write(result)

    return result, usage


deepseek_answer_x("你好，你叫什么名字？", False, True)