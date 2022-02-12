#!/usr/bin/env python3 

import argparse
import websocket
import time
import datetime
from datetime import time as dtime
import json
import os
import subprocess
import struct
import pytz

def on_message(ws, message):
  print("message", message)
  # curl 'http://192.168.0.102/control?var=quality&val=4' && sleep 2 && curl 'http://192.168.0.102/control?var=framesize&val=13' && sleep 5 && curl 'http://192.168.0.102/capture' --output capture.jpeg
  SAST = pytz.timezone('Africa/Johannesburg')
  ct = datetime.datetime.now(SAST).replace(tzinfo=None)

  if "_id" in message and "cam_ready" in message and dtime(7,00) <= ct.time() <= dtime(17,00):
    datajson = json.loads(message)
    node_id = datajson['node_id']
    cam_ready = datajson['cam_ready']
    filename = ("/tmp/" + node_id + "_" + str(ct) + ".jpg").replace(" ", "")
    ip = struct.unpack("<I", struct.pack(">I", int(datajson['ip'])))[0]
    cmd = "curl 'http://%s/control?var=quality&val=4' && sleep 2" % ip
    print(cmd)
    p = subprocess.Popen([cmd,"30"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    cmd = "curl 'http://%s/control?var=framesize&val=13' && sleep 5" % ip
    print(cmd)
    p = subprocess.Popen([cmd,"30"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    cmd = "curl 'http://%s/capture' --output %s && sleep 5" % (ip, filename)
    print(cmd)
    p = subprocess.Popen([cmd,"30"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()
    cmd = "scp %s root@10.8.0.1:farmpics/ && rm -f %s" % (filename, filename)
    print(cmd)
    p = subprocess.Popen([cmd,"30"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    (output, err) = p.communicate()

def on_error(ws, error):
  print("error", error)

def on_close(ws):
  print("### closed ###")

def on_open(ws):
  print("### WS Opened ###")
  time.sleep(1)
  ws.send("_id: Home, pic_listener")

if __name__ == "__main__":
  parser =argparse.ArgumentParser(description='Websocket client')
  parser.add_argument('-w', '--websocket_url', help='Websocket URL', required=False, default='ws://68.183.44.212')
  parser.add_argument('-p', '--websocket_port', help='Websocket Port', required=False, default=12012)
  args = parser.parse_args()

  ws = websocket.WebSocketApp(args.websocket_url+":"+str(args.websocket_port),
                            on_message = on_message,
                            on_error = on_error,
                            on_close = on_close,
                            on_open = on_open)
  ws.keep_running = False
  ws.run_forever()
