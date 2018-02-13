#!/usr/bin/env python

import sys
import hccore

reload(sys)
sys.setdefaultencoding('utf-8')

if __name__ == '__main__':
	hc = hccore.hccore()
	hc.run()