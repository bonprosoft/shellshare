#-*- coding: utf-8 -*-
import sys
import time
from stream_client import *

def watch(path, interval, client):
    interval_sec = interval / 1000.

    with open(path, "r") as file:
        while 1:
            fpos = file.tell()
            line = file.readline()
            if (not line) or (not "\n" in line):
                time.sleep(interval_sec)
                file.seek(fpos)
            else:
                client.notify_update(line.strip("\n"))

def main():
    args = sys.argv
    if (len(args) != 4):
        print "Usage:\n\t python %s [Path] [Interval(msec)] [UserName]" % args[0]
        sys.exit(-1)

    path = args[1]
    interval = int(args[2])
    username = args[3]

    ws = StreamClient('ws://localhost:4567/', name = username)
    try:
        ws.connect()
        watch(path, interval, ws)
    finally:
        ws.close()

if __name__ == "__main__":
    main()

