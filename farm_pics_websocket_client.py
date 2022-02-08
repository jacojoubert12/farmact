#!/usr/bin/env python3 

import argparse
import websocket
import time
import json
import os
import struct

def run_sys_cmd(self, cmd):
  p = subprocess.Popen([cmd,"30"], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
  (output, err) = p.communicate()
  if output:
    print(output)
  if err:
    print(err)
  return output, err


def on_message(ws, message):
    print("message", message)
    #ip = message decode from json['ip']
    #struct.unpack("<I", struct.pack(">I", ip))[0]
    cmd = "curl ip set quality"
    run_sys_cmd(cmd)
    cmd = "curl ip/capture"
    run_sys_cmd(cmd)
    cmd = "scp to dest"
    run_sys_cmd(cmd)

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
