#!/usr/bin/env python


import re

value_pattern   = re.compile('^ *[^\*\.#]')
comment_pattern = re.compile(' *#.*')
axis_enum = ['X', 'Y', 'Z']

three_spaces    = '   '
six_spaces      = '      '
eight_spaces    = '        '

FINISH = 'FINISH'
NEW_LINE = '\n'

def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False
    return True

def is_value(s):
    return re.match(value_pattern, s)

def is_comment(line):
    m = re.match(comment_pattern, line)
    n = line.strip() == ''
    return m or n

class InvalidName(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class InvalidAtom(Exception):
    def __init__(self, atom):
        self.atom = atom

    def __str__(self):
        return self.atom + ' is not a valid Atom'

class MissingInformation(Exception):
    def __init__(self, msg):
        self.msg = msg

    def __str__(self):
        return repr(self.msg)

class InvalidParameter(Exception):
    def __init__(self, invalid, expected):
        self.invalid = invalid
        self.expected = expected

    def __str__(self):
        return repr('Invalid Parameter: \n' + str(invalid) + '\n is not a ' + str(expected))