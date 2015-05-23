# -*- coding: utf-8 -*-
import os.path
import subprocess
import re
import sys


def do_capture(url):
    this_id = re.search("idDeudor=([0-9]+)", url).groups()[0]
    outfile = "screenshot_" + str(this_id) + "_.png"

    cmd = 'xvfb-run --server-args="-screen 0, 1024x768x24" '
    cmd += ' cutycapt --url="' + url + '"'
    cmd += ' --header=Accept-Language:en-US --min-width=650 '
    cmd += ' --out=' + outfile
    try:
        subprocess.check_call(cmd, shell=True)
    except subprocess.CalledProcessError as e:
        print("Error subprocess ")
        print(e)


def main():
    url = sys.argv[1].strip()
    do_capture(url)


if __name__ == "__main__":
    main()
