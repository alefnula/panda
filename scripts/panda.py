#!/usr/bin/env python

import os
import sys
sys.path.append('../src')
for i in ('.', os.path.dirname(__file__), os.path.abspath(os.path.dirname(__file__))):
    while i in sys.path:
        sys.path.remove(i)

from panda.panda import main


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
