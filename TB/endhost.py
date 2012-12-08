#!/usr/bin/python
import os
from multiprocessing import process
eng = ["/usr/bin/python", "/home/tritm/ChuTo_SimpleNetwork/TB/eng_endhost.py"]
sci = ["/usr/bin/python", "/home/tritm/ChuTo_SimpleNetwork/TB/sci_endhost.py"]

process.call(sci)
process.call(eng)