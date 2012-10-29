#!/usr/bin/python

"""
Copyright (C) 2012  The University of Texas at Austin.

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

Written by: Jeff Strunk, Department of Mathematics,
The University of Texas at Austin 78712.    jstrunk@math.utexas.edu
    
Modified by: Richard Halkyard, Minnesota Supercomputing Institute
University of Minnesota.    richard@msi.umn.edu
"""

import cups
import sys
import os
from Foundation import CFPreferencesCopyAppValue

BUNDLE_ID = 'edu.utexas.ma.browsecups'

if __name__ == '__main__':
    if len(sys.argv) == 2:
        server = sys.argv[1]
    else:
        print """Usage: {program} hostname
            """.format(program=sys.argv[0])
        sys.exit(1)
    try:
        lc = cups.Connection()
    except RuntimeError, e:
        print e
        sys.exit(2)

    cups.setServer(server)    
    try:
        rc = cups.Connection()
    except RuntimeError, e:
        print e
        sys.exit(2)
    try:
        printers = rc.getPrinters()
    except cups.IPPError, (code, msg):
        print "Error retrieving printer list: {}".format(msg)
        sys.exit(3)

    for p in printers.keys():
        try:
            ppd = rc.getPPD(p)
            if ppd is not None:
                lc.addPrinter(p, device=printers[p]['printer-uri-supported'], location=printers[p]['printer-location'], info=printers[p]['printer-info'], filename=ppd)
            else:
                lc.addPrinter(p, device=printers[p]['printer-uri-supported'], location=printers[p]['printer-location'], info=printers[p]['printer-info'])
            lc.setPrinterShared(p, False)
            lc.enablePrinter(p)
            lc.acceptJobs(p)
        except cups.IPPError, (code, msg):
            print "Could not add/modify printer {}: {}".format(p, msg)
            sys.exit(code)
    
