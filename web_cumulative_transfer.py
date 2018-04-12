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
        print "{0} <max_items>".format(sys.argv[0])
        sys.exit(0)
    max = int(sys.argv[1])

    logs = open('data', 'r').readlines()
    slogs = [sanitize(log) for log in logs]
    two_hundreds = [l for l in slogs if l[5] == '200']
    gets = [l for l in two_hundreds if l[2] == 'GET']

    resources = {}
    for l in gets:
        if l[3] not in resources:
            resources[l[3]] = int(l[6])
        else:
            resources[l[3]] += int(l[6])

    count = 0
    for key in sorted(resources):
        print "%s: %s" % (key, resources[key])
        count += 1
        if count == max:
            break 
main()
