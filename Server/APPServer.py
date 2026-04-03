#!/usr/bin/env/python3
# File name   : WebServer.py
# Website     : www.adeept.com
# Author      : Adeept
# Date        : 2025/04/23

import time
import threading
import os
import Info as info

import RobotLight as robotLight
import Switch as switch
import socket

import SpiderG
SpiderG.move_init()

import asyncio
import websockets
import Voltage
import json
import app
import Buzzer

#Buzzer
player = Buzzer.Player()
player.start()

#Voltage
batteryMonitor = Voltage.BatteryLevelMonitor()
batteryMonitor.start()

curpath = os.path.realpath(__file__)
thisPath = "/" + os.path.dirname(curpath)
SteadyMode = 0

FLB_init_pwm = SpiderG.FLB_init_pwm
FLM_init_pwm = SpiderG.FLM_init_pwm
FLE_init_pwm = SpiderG.FLE_init_pwm

FRB_init_pwm = SpiderG.FRB_init_pwm
FRM_init_pwm = SpiderG.FRM_init_pwm
FRE_init_pwm = SpiderG.FRE_init_pwm

HLB_init_pwm = SpiderG.HLB_init_pwm
HLM_init_pwm = SpiderG.HLM_init_pwm
HLE_init_pwm = SpiderG.HLE_init_pwm

HRB_init_pwm = SpiderG.HRB_init_pwm
HRM_init_pwm = SpiderG.HRM_init_pwm
HRE_init_pwm = SpiderG.HRE_init_pwm


def servoPosInit():
    SpiderG.move_init()


def functionSelect(command_input, response):
    global functionMode, SteadyMode
    
    if 'findColor' == command_input:
        flask_app.modeselect('findColor')
        flask_app.modeselectApp('APP')

    elif 'motionGet' == command_input:
        flask_app.modeselect('watchDog')

    elif 'stopCV' == command_input:
        flask_app.modeselect('none')
        switch.switch(1,0)
        switch.switch(2,0)
        switch.switch(3,0)
        time.sleep(0.1)
        SpiderG.move_init()
        SpiderG.servoStop()

    elif 'police' == command_input:
        ws2812.police()

    elif 'policeOff' == command_input:
        ws2812.breath(70,70,255)

    elif 'Buzzer_Music' == command_input:
        player.start_playing()

    elif 'Buzzer_Music_Off' == command_input:
        player.pause()


def switchCtrl(command_input, response):
    if 'Switch_1_on' in command_input:
        switch.switch(1,1)

    elif 'Switch_1_off' in command_input:
        switch.switch(1,0)

    elif 'Switch_2_on' in command_input:
        switch.switch(2,1)

    elif 'Switch_2_off' in command_input:
        switch.switch(2,0)

    elif 'Switch_3_on' in command_input:
        switch.switch(3,1)

    elif 'Switch_3_off' in command_input:
        switch.switch(3,0) 


def robotCtrl(command_input, response):
    global SteadyMode
    clen = len(command_input.split())
    if 'forward' in command_input and clen == 2 and SteadyMode == 0:
        SpiderG.walk('forward')
    
    elif 'backward' in command_input and clen == 2 and SteadyMode == 0:
        SpiderG.walk('backward')

    elif 'left' in command_input and clen == 2 and SteadyMode == 0:
        SpiderG.walk('turnleft')

    elif 'right' in command_input and clen == 2 and SteadyMode == 0:
        SpiderG.walk('turnright')

    elif 'DTS' in command_input and SteadyMode == 0:
        SpiderG.move_init()
        SpiderG.servoStop()

    elif 'steadyCamera' == command_input:    
        SteadyMode = 1 
        SpiderG.move_init()               
        SpiderG.steadyModeOn()

    elif 'steadyCameraOff' == command_input:                    
        SteadyMode = 0
        SpiderG.steadyModeOff()

    elif 'Lean_L' == command_input and SteadyMode == 0:
        SpiderG.walk('Lean-L')

    elif 'Lean_R' == command_input and SteadyMode == 0:
        SpiderG.walk('Lean-R')

    elif 'up' == command_input and SteadyMode == 0:
        SpiderG.status_GenOut(0, -150, 0)
        SpiderG.direct_M_move()

    elif 'down' == command_input and SteadyMode == 0:
        SpiderG.status_GenOut(0, 150, 0)
        SpiderG.direct_M_move()

    elif 'StandUp' == command_input and SteadyMode == 0:
        SpiderG.status_GenOut(-200, 0, 0)
        SpiderG.direct_M_move()

    elif 'StandLow' == command_input and SteadyMode == 0:
        SpiderG.status_GenOut(200, 0, 0)
        SpiderG.direct_M_move()

    else:
        pass


def configPWM(command_input, response):
    global  FLB_init_pwm, FLM_init_pwm, FLE_init_pwm, HLB_init_pwm, HLM_init_pwm, HLE_init_pwm, FRB_init_pwm, FRM_init_pwm, FRE_init_pwm, HRB_init_pwm, HRM_init_pwm, HRE_init_pwm, SteadyMode

    if 'SiLeft' in command_input and SteadyMode == 0:
        numServo = int(command_input[7:])
        if numServo == 0:
            FLB_init_pwm -= 5
            SpiderG.FLB_init_pwm = FLB_init_pwm
        elif numServo == 1:
            FLM_init_pwm -= 5
            SpiderG.FLM_init_pwm = FLM_init_pwm
        elif numServo == 2:
            FLE_init_pwm -= 5
            SpiderG.FLE_init_pwm = FLE_init_pwm
        elif numServo == 3:
            HLB_init_pwm -= 5
            SpiderG.HLB_init_pwm = HLB_init_pwm
        elif numServo == 4:
            HLM_init_pwm -= 5
            SpiderG.HLM_init_pwm = HLM_init_pwm
        elif numServo == 5:
            HLE_init_pwm -= 5
            SpiderG.HLE_init_pwm = HLE_init_pwm
        elif numServo == 6:
            FRB_init_pwm -= 5
            SpiderG.FRB_init_pwm = FRB_init_pwm
        elif numServo == 7:
            FRM_init_pwm -= 5
            SpiderG.FRM_init_pwm = FRM_init_pwm
        elif numServo == 8:
            FRE_init_pwm -= 5
            SpiderG.FRE_init_pwm = FRE_init_pwm
        elif numServo == 9:
            HRB_init_pwm -= 5
            SpiderG.HRB_init_pwm = HRB_init_pwm
        elif numServo == 10:
            HRM_init_pwm -= 5
            SpiderG.HRM_init_pwm = HRM_init_pwm
        elif numServo == 11:
            HRE_init_pwm -= 5
            SpiderG.HRE_init_pwm = HRE_init_pwm

        SpiderG.move_init()


    if 'SiRight' in command_input and SteadyMode == 0:
        numServo = int(command_input[8:])
        if numServo == 0:
            FLB_init_pwm += 5
            SpiderG.FLB_init_pwm = FLB_init_pwm
        elif numServo == 1:
            FLM_init_pwm += 5
            SpiderG.FLM_init_pwm = FLM_init_pwm
        elif numServo == 2:
            FLE_init_pwm += 5
            SpiderG.FLE_init_pwm = FLE_init_pwm

        elif numServo == 3:
            HLB_init_pwm += 5
            SpiderG.HLB_init_pwm = HLB_init_pwm
        elif numServo == 4:
            HLM_init_pwm += 5
            SpiderG.HLM_init_pwm = HLM_init_pwm
        elif numServo == 5:
            HLE_init_pwm += 5
            SpiderG.HLE_init_pwm = HLE_init_pwm

        elif numServo == 6:
            FRB_init_pwm += 5
            SpiderG.FRB_init_pwm = FRB_init_pwm
        elif numServo == 7:
            FRM_init_pwm += 5
            SpiderG.FRM_init_pwm = FRM_init_pwm
        elif numServo == 8:
            FRE_init_pwm += 5
            SpiderG.FRE_init_pwm = FRE_init_pwm

        elif numServo == 9:
            HRB_init_pwm += 5
            SpiderG.HRB_init_pwm = HRB_init_pwm
        elif numServo == 10:
            HRM_init_pwm += 5
            SpiderG.HRM_init_pwm = HRM_init_pwm
        elif numServo == 11:
            HRE_init_pwm += 5
            SpiderG.HRE_init_pwm = HRE_init_pwm

        SpiderG.move_init()


    if 'PWMMS' in command_input and SteadyMode == 0:
        numServo = int(command_input[6:])
        if numServo == 0:
            # print(f"numServo:{numServo} FLB_init_pwm:{FLB_init_pwm}")
            FLB_init_pwm = 300
            SpiderG.FLB_init_pwm = FLB_init_pwm
            SpiderG.set_angle(numServo,FLB_init_pwm)
        elif numServo == 1:
            FLM_init_pwm = 300
            SpiderG.FLM_init_pwm = FLM_init_pwm
            SpiderG.set_angle(numServo,FLM_init_pwm)
        elif numServo == 2:
            FLE_init_pwm = 300
            SpiderG.FLE_init_pwm = FLE_init_pwm
            SpiderG.set_angle(numServo,FLE_init_pwm)

        elif numServo == 3:
            HLB_init_pwm = 300
            SpiderG.HLB_init_pwm = HLB_init_pwm
            SpiderG.set_angle(numServo,HLB_init_pwm)
        elif numServo == 4:
            HLM_init_pwm = 300
            SpiderG.HLM_init_pwm = HLM_init_pwm
            SpiderG.set_angle(numServo,HLM_init_pwm)
        elif numServo == 5:
            HLE_init_pwm = 300
            SpiderG.HLE_init_pwm = HLE_init_pwm
            SpiderG.set_angle(numServo,HLE_init_pwm)

        elif numServo == 6:
            FRB_init_pwm = 300
            SpiderG.FRB_init_pwm = FRB_init_pwm
            SpiderG.set_angle(numServo,FRB_init_pwm)
        elif numServo == 7:
            FRM_init_pwm = 300
            SpiderG.FRM_init_pwm = FRM_init_pwm
            SpiderG.set_angle(numServo,FRM_init_pwm)
        elif numServo == 8:
            FRE_init_pwm = 300
            SpiderG.FRE_init_pwm = FRE_init_pwm
            SpiderG.set_angle(numServo,FRE_init_pwm)

        elif numServo == 9:
            HRB_init_pwm = 300
            SpiderG.HRB_init_pwm = HRB_init_pwm
            SpiderG.set_angle(numServo,HRB_init_pwm)
        elif numServo == 10:
            HRM_init_pwm = 300
            SpiderG.HRM_init_pwm = HRM_init_pwm
            SpiderG.set_angle(numServo,HRM_init_pwm)
        elif numServo == 11:
            HRE_init_pwm = 300
            SpiderG.HRE_init_pwm = HRE_init_pwm
            SpiderG.set_angle(numServo,HRE_init_pwm)


    elif 'PWMD' in command_input and SteadyMode == 0:
        FLB_init_pwm = 300
        FLM_init_pwm = 300
        FLE_init_pwm = 300

        HLB_init_pwm = 300
        HLM_init_pwm = 300
        HLE_init_pwm = 300

        FRB_init_pwm = 300
        FRM_init_pwm = 300
        FRE_init_pwm = 300

        HRB_init_pwm = 300
        HRM_init_pwm = 300
        HRE_init_pwm = 300

        SpiderG.FLB_init_pwm = FLB_init_pwm
        SpiderG.FLM_init_pwm = FLM_init_pwm
        SpiderG.FLE_init_pwm = FLE_init_pwm

        SpiderG.HLB_init_pwm = HLB_init_pwm
        SpiderG.HLM_init_pwm = HLM_init_pwm
        SpiderG.HLE_init_pwm = HLE_init_pwm

        SpiderG.FRB_init_pwm = FRB_init_pwm
        SpiderG.FRM_init_pwm = FRM_init_pwm
        SpiderG.FRE_init_pwm = FRE_init_pwm

        SpiderG.HRB_init_pwm = HRB_init_pwm
        SpiderG.HRM_init_pwm = HRM_init_pwm
        SpiderG.HRE_init_pwm = HRE_init_pwm
        SpiderG.move_init()


async def recv_msg(websocket):
    global speed_set, modeSelect

    while True: 
        response = {
            'status' : 'ok',
            'title' : '',
            'data' : None
        }

        data = ''
        data = await websocket.recv()
        try:
            data = json.loads(data)
        except Exception as e:
            print('not A JSON')

        if not data:
            continue

        if isinstance(data,str):
            robotCtrl(data, response)

            switchCtrl(data, response)

            functionSelect(data, response)

            configPWM(data, response)

            if 'get_info' == data:
                response['title'] = 'get_info'
                response['data'] = [info.get_cpu_tempfunc(), info.get_cpu_use(), info.get_ram_info(),batteryMonitor.get_battery_percentage()]

        elif(isinstance(data,dict)):
            color = data['data']
            if "title" in data and data['title'] == "findColorSet":
                flask_app.colorFindSetApp(color[0],color[1],color[2])
            elif data['lightMode'] == "breath":  
                ws2812.breath(color[0],color[1],color[2])
            elif data['lightMode'] == "flowing":
                ws2812.flowing(color[0],color[1],color[2])
            elif data['lightMode'] == "rainbow":
                ws2812.rainbow(color[0],color[1],color[2])
            elif data['lightMode'] == "police":
                ws2812.police()

        print(data)
        response = json.dumps(response)
        await websocket.send(response)

async def main_logic(websocket, path):
    await recv_msg(websocket)

if __name__ == '__main__':
    switch.switchSetup()

    global flask_app
    flask_app = app.webapp()
    flask_app.startthread()

    try:
        ws2812=robotLight.Adeept_SPI_LedPixel(16, 255)
        if ws2812.check_spi_state() != 0:
            ws2812.start()
            ws2812.breath(70,70,255)
        else:
            ws2812.led_close()
    except KeyboardInterrupt:
        ws2812.led_close()
        pass

    while  1:
        try:                  #Start server,waiting for client
            start_server = websockets.serve(main_logic, '0.0.0.0', 8888)
            asyncio.get_event_loop().run_until_complete(start_server)
            print('waiting for connection...')
            break
        except Exception as e:
            print(e)
            ws2812.set_all_led_color_data(0,0,0)
            ws2812.show()

    try:
        asyncio.get_event_loop().run_forever()
    except Exception as e:
        print(e)
        ws2812.set_all_led_color_data(0,0,0)
        ws2812.show()
