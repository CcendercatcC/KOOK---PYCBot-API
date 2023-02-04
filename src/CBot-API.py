# coding=UTF-8
import json
import websockets
import socket
import asyncio
import urllib.request
import zlib


#注意:由于本人的技术原因 暂时只支持WebSocket




async def useAPI(addr,Token):#访问kook api的方法,自动将返回的Json转为字典 需要提供地址（如/api/v3/gateway/index 为Gateway的地址）和Token
    return json.loads(urllib.request.urlopen(urllib.request.Request("https://www.kookapp.cn/"+addr,headers={'Authorization': 'Bot '+Token})).read())


async def GetWay(Token,compress=1):
    index=1


    while True:
        WaitTime=2
        try:
            return (await asyncio.create_task(useAPI("/api/v3/gateway/index?compress="+str(compress), Token)))["data"]["url"] #调用useAPI获取Gateway地址
        except Exception as e:#出现异常时自动开始指数回退（参考PHP-Bot）
            print("CBot>",str(e))
            if WaitTime>=60:
                WaitTime=60
            else:
                WaitTime**=index
            print("CBot> Wating",WaitTime,"s......")
            await asyncio.sleep(WaitTime)
            if WaitTime<60:
                index+=1
            continue


async def Connect(url):#用于连接 返回已经连接的Websocket，提供WateGate
    return async websockets.connect(url)


async def Receive(websocket,compress=1):#这里提供Websocket
    async websocket:#访问Gateway 并接收报文
        if compress==0:
            data=await websocket.recv()
        else:
            data=zlib.decompress(await websocket.recv())#用于解压报文
        JsData = json.loads(data)
        Code = JsData["d"]["code"] #提取状态码 用于发起异常
        if JsData["s"]==1 or JsData["s"]==5:
            if Code!=0:#后面用来发起异常的 方便使用者根据实际情况调整
                if Code == 40100:
                    raise ValueError["Missing Parameter!"]
                if Code == 40101:
                    raise ValueError["Invalid Token!"]
                if Code == 40102:
                    raise ValueError["Token Validation Failed!"]
                if Code == 40103:
                    raise ValueError["Token Expired! Please GateWay Again!"]
                if Code == 40106:
                    raise ValueError["Missing Parameter! RECONNECT!!!"]
                if Code == 40107:
                    raise ValueError["Current SessionHas Expired! RECONNECT!!!"]
                if Code == 40108:
                    raise ValueError["Invalid sn! RECONNECT!!!"]
        return JsData
