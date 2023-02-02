# coding=UTF-8
import json
import websockets
import socket
import asyncio
import urllib.request
import zlib

async def useAPI(addr,Token):
    return json.loads(urllib.request.urlopen(urllib.request.Request("https://www.kookapp.cn/"+addr,headers={'Authorization': 'Bot '+Token})).read())

async def GetWay(Token,compress=1):
    index=1

    while True:
        WaitTime=2
        try:
            return (await asyncio.create_task(useAPI("/api/v3/gateway/index?compress="+str(compress), Token)))["data"]["url"]
        except Exception as e:
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

async def Receive(url,compress=1):
    async with websockets.connect(url) as websocket:
        if compress==0:
            data=await websocket.recv()
        else:
            data=zlib.decompress(await websocket.recv())
        JsData = json.loads(data)
        Code = JsData["d"]["code"]
        if JsData["s"]==1 or JsData["s"]==5:
            if Code!=0:
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


asyncio.run(Receive(asyncio.run(GetWay("1/MTUxNzE=/pbHK+iz6seAU0CDKiNYN1g=="))))


