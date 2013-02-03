#!/usr/bin/env python

import os
import sys
from optparse import OptionParser

options = []

def trim_path(path):
    if path == os.sep:
        return path
    return path.rstrip(os.sep)

def get_size(file):
    try:
        return os.path.getsize(file)
    except OSError:
        return 0
        
def get_usage(path):
    global options
    if (options.verbose):
        print "Get Usage: %s" % (path)
    if os.path.isfile(path):
        return os.path.getsize(path)
    elif os.path.isdir(path):
        total = 0
        for root, dirs, files in os.walk(path):
            total += sum([get_size(os.path.join(root, f)) for f in files])
            #if (options.verbose):
            #   print "\tWalk: %s - %i" % (root, total)
        return total
    else:
        return 0

def main():
    global options

    usage = "usage: %prog [options] arg"
    parser = OptionParser(usage)
    parser.add_option("-R", "--recursive",
                      action="store_true", dest="recursive", default=False)
    parser.add_option("-v", "--verbose",
                      action="store_true", dest="verbose")
    parser.add_option("-q", "--quiet",
                      action="store_false", dest="verbose")
    
    (options, args) = parser.parse_args()
    if len(args) == 0:
        parser.error("Please specify at least one path")
    
    print "%i B" % (sum([get_usage(trim_path(path)) for path in args]))     

if __name__ == "__main__":
    main()