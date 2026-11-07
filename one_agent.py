import os
import requests
import json

class Prompt:
    def __init__(self, system_prompt: str = "", user_prompt: str = ""):
        self.system_prompt = system_prompt
        self.user_prompt = user_prompt

class Context:
    def __init__(self):
        self.messages = []

    def append_message(self, input: str, output: str):
        self.messages.append({'input': input, 'output': output})

    def get_context(self):
        return self.messages


'''
{
    "type": "action",
    "name": "get_weather",
    "params": {"location": "东莞", "time": "2026-10-26"},
    "message": ""
}
'''

def to_str(value):
    if value is None:
        return ""

    if isinstance(value, str):
        return value

    try:
        return json.dumps(
            value,
            ensure_ascii=False,
            default=lambda obj: obj.__dict__ if hasattr(obj, "__dict__") else str(obj)
        )
    except Exception:
        return str(value)

API_KEY = os.getenv("LLM_API_KEY")
BASE_URL = os.getenv("LLM_BASE_URL")

def call_llm(prompt: Prompt, context: Context, tools: list) -> dict:
    real_prompt = '''
    之前的对话记录为：[[[{0}]]]，格式为有序字典列表，input是输入，output是输出。
    可用的工具列表为：[[[{1}]]]，格式为字典列表，name是工具名称，description是工具描述，params是工具参数示例。
    你的角色和行为规范：[[[{2}]]]，当前问题是：[[[{3}]]]。
    请用json格式输出回复，其中type是回复类型（包含：action表示要进行工具调用，answer表示已经得到答案），name是工具名称，params是工具参数，message是回复内容。
    '''.format(to_str(context), to_str(tools), prompt.system_prompt, prompt.user_prompt)
    url = BASE_URL
    data = {
        "model": "gpt-5.5",
        "prompt": real_prompt
    }
    headers = {
        "Authorization": "Bearer {}".format(API_KEY),
        "Content-Type": "application/json"
    }
    response = requests.post(
        url,
        json=data,
        timeout=10,
        headers=headers
    )

    response.raise_for_status()
    result = response.json()["choices"][0]["text"]
    try:
        return json.loads(result)
    except (json.JSONDecodeError, TypeError):
        return {"type": "error", "message": "返回不是json" + result}


def get_weather(location: str, time: str) -> str:
    return "晴朗"

def get_currtime() -> str:
    return "2026-11-06 15:12:00"

def query_log(start_time: str, end_time: str, keyword: str) -> str:
    return '''
    2026-11-06 14:32:01.124 INFO  [http-nio-8080-exec-21] c.m.s.OrderService - Start processing order, orderId=ORD202611060001
2026-11-06 14:32:01.156 INFO  [http-nio-8080-exec-21] c.m.s.OrderService - Loading order detail from database
2026-11-06 14:32:01.209 INFO  [http-nio-8080-exec-18] c.m.s.ProductService - Query product information, productId=P100238
2026-11-06 14:32:02.331 WARN  [http-nio-8080-exec-25] c.m.cache.LocalCache - Cache size is high, currentEntries=1854320

2026-11-06 14:32:05.820 INFO  [GC] GC(1821) Pause Young (Normal) (G1 Evacuation Pause) 3584M->3421M(4096M) 186.421ms
2026-11-06 14:32:06.376 INFO  [GC] GC(1822) Pause Young (Concurrent Start) (G1 Humongous Allocation) 3721M->3618M(4096M) 302.553ms
2026-11-06 14:32:06.981 WARN  [http-nio-8080-exec-19] c.m.monitor.MemoryMonitor - JVM heap usage exceeded threshold: used=3728MB, max=4096MB, usage=91.0%

2026-11-06 14:32:07.442 INFO  [GC] GC(1823) Pause Full (G1 Compaction Pause) 3891M->3812M(4096M) 821.221ms
2026-11-06 14:32:08.310 WARN  [http-nio-8080-exec-28] c.m.monitor.MemoryMonitor - JVM heap usage exceeded threshold: used=3902MB, max=4096MB, usage=95.3%

2026-11-06 14:32:08.725 ERROR [http-nio-8080-exec-21] c.m.s.OrderService - Failed to process order ORD202611060001
java.lang.OutOfMemoryError: Java heap space
    at java.base/java.util.Arrays.copyOf(Arrays.java:3745)
    at java.base/java.lang.AbstractStringBuilder.ensureCapacityInternal(AbstractStringBuilder.java:172)
    at java.base/java.lang.AbstractStringBuilder.append(AbstractStringBuilder.java:538)
    at java.base/java.lang.StringBuilder.append(StringBuilder.java:179)
    at com.molex.service.OrderService.buildOrderHistory(OrderService.java:286)
    at com.molex.service.OrderService.processOrder(OrderService.java:145)
    at com.molex.controller.OrderController.submitOrder(OrderController.java:87)
    at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke0(Native Method)
    at java.base/jdk.internal.reflect.NativeMethodAccessorImpl.invoke(NativeMethodAccessorImpl.java:77)
    at java.base/java.lang.reflect.Method.invoke(Method.java:568)

2026-11-06 14:32:08.731 ERROR [http-nio-8080-exec-28] o.a.c.c.C.[.[.[/].[dispatcherServlet] - Servlet.service() threw exception
java.lang.OutOfMemoryError: Java heap space

2026-11-06 14:32:08.739 INFO  [GC] GC(1824) Pause Full (G1 Compaction Pause) 4093M->4087M(4096M) 1256.883ms
2026-11-06 14:32:10.002 ERROR [pool-3-thread-7] c.m.task.DataSyncTask - Unexpected error during data synchronization
java.lang.OutOfMemoryError: Java heap space
    at java.base/java.util.HashMap.resize(HashMap.java:702)
    at java.base/java.util.HashMap.putVal(HashMap.java:661)
    at java.base/java.util.HashMap.put(HashMap.java:610)
    at com.molex.sync.DataSyncTask.loadRecords(DataSyncTask.java:198)
    at com.molex.sync.DataSyncTask.run(DataSyncTask.java:102)

2026-11-06 14:32:10.114 ERROR [http-nio-8080-exec-14] o.s.b.w.s.ErrorPageFilter - Forwarding to error page failed
java.lang.OutOfMemoryError: Java heap space

2026-11-06 14:32:11.384 INFO  [GC] GC(1825) Pause Full (G1 Compaction Pause) 4094M->4090M(4096M) 1433.221ms
2026-11-06 14:32:11.385 ERROR [main] c.m.monitor.JvmHealthMonitor - JVM memory critically exhausted: heapUsed=4090MB, heapMax=4096MB

Exception in thread "http-nio-8080-exec-21" java.lang.OutOfMemoryError: Java heap space
Exception in thread "pool-3-thread-7" java.lang.OutOfMemoryError: Java heap space

2026-11-06 14:32:12.028 ERROR [main] o.s.b.SpringApplication - Application run failed
java.lang.OutOfMemoryError: Java heap space
    '''

def query_code(key: str) -> str:
    return '''
    package com.molex.service;

public class OrderService {

    public void processOrder(String orderId) {
        System.out.println("Start processing order, orderId=" + orderId);

        buildOrderHistory(orderId);
    }

    private void buildOrderHistory(String orderId) {

        System.out.println("Building order history, orderId=" + orderId);

        StringBuilder builder = new StringBuilder();

        long count = 0;

        while (true) {

            builder.append("OrderId=")
                    .append(orderId)
                    .append(", material=P100238")
                    .append(", quantity=100")
                    .append(", status=COMPLETED")
                    .append(", timestamp=")
                    .append(System.currentTimeMillis())
                    .append("\n");

            count++;

            if (count % 100000 == 0) {
                System.out.println(
                        "Order history records loaded: " + count
                );
            }
        }
    }
}
    '''

def get_server_list(service_name: str) -> list:
    return [
        {
            "ip": "10.12.56.19",
            "port": 8080,
            "process_name": "molex-sfc.jar",
        }
    ]

def query_service_status(ip: str, process_name: str) -> str:
    return "down"

context = Context()
def agent(prompt: Prompt) -> str:
    # question -> thought -> action -> thought -> action -> thought -> answer
    functions = {
        "get_weather": get_weather,
        "get_currtime": get_currtime,
        "query_log": query_log,
        "query_code": query_code,
        "get_server_list": get_server_list,
        "query_service_status": query_service_status,
    }
    tools = [
        {
            "name": "get_weather",
            "description": "查询天气，参数是地点和时间",
            "params": {"location": "东莞", "time": "2026-10-26"}
        },
        {
            "name": "get_currtime",
            "description": "查询当前日期，无参数",
            "params": {}
        },
        {
            "name": "query_log",
            "description": "查询微服务日志，参数是时间范围和关键词",
            "params": {"start_time": "2026-10-26 12:15:21", "end_time": "2026-10-26 16:15:21", "keyword": "ERROR"}
        },
        {
            "name": "query_code",
            "description": "查询微服务代码，参数是关键词",
            "params": {"keyword": "sendMessage"}
        },
        {
            "name": "get_server_list",
            "description": "查询服务器信息，参数是服务名称，返回服务ip，port, process_name",
            "params": {"service_name": "molex-mo-dg-aux"}
        },
        {
            "name": "query_service_status",
            "description": "查询服务状态，参数是ip和process_name，返回status",
            "params": {"ip": "10.12.56.19", "process_name": "aux_service.jar"}
        }
    ]

    count = 0
    while True:
        if count > 5:
            return "对话次数过多，可能出现循环调用，请检查问题或工具定义。" + reply
        reply = call_llm(prompt, context, tools)
        context.append_message(prompt.user_prompt, reply)
        if reply["type"] == "answer":
            return reply["message"]
        elif reply["type"] == "action":
            if reply['name'] in functions.keys():
                try:
                    result = functions[reply['name']](**reply["params"])
                except Exception as e:
                    result = f"调用工具 {reply['name']} 时发生异常: {str(e)}"
            else:
                result = "未知操作"
            context.append_message(reply, result)
        elif reply["type"] == "error":
            context.append_message(reply, "llm回复异常")
        else:
            context.append_message(reply, "未知类型")

        count = count + 1



# prompt = Prompt("你是一个生活助理，可以准确回答各类生活问题", "今天在东莞适合户外运动吗？")
prompt = Prompt("你是一个制造业工厂微服务运维专家，可以准确回答各种生产运维问题", "sfc网页打不开，根本原因是什么？")
print(agent(prompt))
print("对话记录：")
for i, msg in enumerate(context.get_context()):
    print(f"第{i+1}轮对话：")
    print("用户输入：", msg['input'])
    print("助手输出：", msg['output'])