#-*- coding: utf-8 -*-
import codecs
import glob
import re
import os
import sys


for i in codecs.open("deudores_redam.csv", "r", "utf-8"):
    i = i.strip().split("\t")
    url = i[5]
    id = re.search("idDeudor=([0-9]+)", url).groups()[0]

    dni = i[0].replace("/", "-")

    old_filename = "screenshots/screenshot_" + str(id) + "_.png"
    new_filename = "screenshots/screenshot_" + str(dni) + "_" + str(id) + ".png"

    print(old_filename, new_filename)
    os.rename(old_filename, new_filename)
