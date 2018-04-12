#!/usr/bin/env python
import sys

# Log format:
# - request date, time, and time zone
# - request line from the client
# - HTTP status code returned to the client
# - size (in bytes) of the returned object

def sanitize(log):
    output = []
    for i in log.split():
        i = i.strip('[').strip('"').strip(']').rstrip('\n')
        output.append(i)
    return tuple(output)

def main():

    if '-h' in sys.argv:
        print "{0} <no arguments>".format(sys.argv[0])
        print "(Looks for ./data)"
        sys.exit(0)

    def byte_count(resource, sanitized_logs):
        bytes = [int(b[6]) for b in sanitized_logs if b[3] == resource]
        return sum(bytes)

    max = 10

    logs = open('data', 'r').readlines()
    slogs = [sanitize(log) for log in logs]
    two_hundreds = [l for l in slogs if l[5].startswith('2')]
    gets = [l for l in two_hundreds if l[2] == 'GET']

    # count requests so we can show most
    # requested item
    resources = {}
    for l in gets:
        if l[3] not in resources:
            resources[l[3]] = 1
        else:
            resources[l[3]] += 1

    for key, value in sorted(resources.iteritems(), key=lambda (k,v): (v,k), reverse=True):
        bytes = byte_count(key, gets)
        print "%s: %s" % (key, bytes)

main()
