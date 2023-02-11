# coding=UTF-8
import json
import websockets
import socket
import asyncio
import urllib.request
import zlib

# 注意:由于本人的技术原因 暂时只支持WebSocket


async def useAPI(
    addr, Token, TimeOut=6
):  # 访问kook api的方法,自动将返回的Json转为字典 需要提供地址（如/api/v3/gateway/index 为Gateway的地址）和Token
    return json.loads(
        urllib.request.urlopen(
            urllib.request.Request(
                "https://www.kookapp.cn/" + addr,
                headers={'Authorization': 'Bot ' + Token},
            ),
            timeout=TimeOut,
        ).read()
    )


async def GetWay(Token, compress=1):
    index = 1

    while True:
        WaitTime = 2
        try:
            return (
                await asyncio.create_task(
                    useAPI(
                        "/api/v3/gateway/index?compress="
                        + str(compress),
                        Token,
                    )
                )
            )["data"][
                "url"
            ]  # 调用useAPI获取Gateway地址
        except Exception as e:  # 出现异常时自动开始指数回退（参考PHP-Bot）
            print("CBot>", str(e))
            if WaitTime >= 60:
                WaitTime = 60
            else:
                WaitTime **= index
                index += 1
            print("CBot> Wating", WaitTime, "s......")
            await asyncio.sleep(WaitTime)

            continue


async def Connect(url):  # 用于连接 返回已经连接的Websocket，提供WateGate
    return await websockets.connect(url)


async def Receive(websocket, compress=1):  # 这里提供Websocket
    # 访问Gateway 并接收报文
    if compress == 0:
        data = await websocket.recv()
    else:
        data = zlib.decompress(await websocket.recv())  # 用于解压报文
    JsData = json.loads(data)
    Code = JsData["d"]["code"]  # 提取状态码 用于发起异常
    if JsData["s"] == 1 or JsData["s"] == 5:
        if Code != 0:  # 后面用来发起异常的 方便使用者根据实际情况调整
            if Code == 40100:
                raise ValueError["Missing Parameter!"]
            if Code == 40101:
                raise ValueError["Invalid Token!"]
            if Code == 40102:
                raise ValueError["Token Validation Failed!"]
            if Code == 40103:
                raise ValueError[
                    "Token Expired! Please GateWay Again!"
                ]
            if Code == 40106:
                raise ValueError["Missing Parameter! RECONNECT!!!"]
            if Code == 40107:
                raise ValueError[
                    "Current SessionHas Expired! RECONNECT!!!"
                ]
            if Code == 40108:
                raise ValueError["Invalid sn! RECONNECT!!!"]
    return JsData


async def Sent(websocket, data):
    websocket.Sent(json.dumps(data))


async def Ping(websocket, sn):
    ping = {"s": 2}
    ping["sn"] = sn
    await Sent(websocket, ping)


async def Retriever(
    websocket, ReturnList, ConditionList, compress=1
):  # 检索器
    while True:
        ReturnList.append(await Receive(websocket, compress))
        for Judge in ConditionList:
            try:
                for Condition in Judge:
                    if ReturnList[-1][Condition[0]] == Condition[1]:
                        pass
                    else:
                        raise
                return ReturnList[-1]
            except:
                pass


async def main():
    '''程序入口'''
    print("CBot> GateWay")
    l = []
    url = await GetWay("1/MTUzMzQ=/Fx08J7b32HGVL1Lq/4ELnw==")
    print("CBot> wating for HELLO")
    async with websockets.connect(url) as ws:
        ret = await Retriever(ws, l, [[["s", 1]]])
        print("CBot> ", ret)
        sn = 0


if __name__ == "__main__":  # 测试代码
    asyncio.run(main())
