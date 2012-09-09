#!/usr/bin/env python

#-------------------------------------------------------------------------------
# Name:        module
# Purpose:
#
# Author:      ezequiel
#
# Created:     01/09/2012
# Copyright:   (c) ezequiel 2012
# Licence: GPL
#-------------------------------------------------------------------------------

import re

#from diracfile import DiracFile

class Property:
##    def main():
##        pass
##
##    if __name__ == '__main__':
##        main()

    def __init__(self, name):
        self.simple_test()
        self.name = name
        self.values = []

    def simple_test(self):
        if DiracFile.properties.get(name) == None:
            raise InvalidName('Property name invalid: '+name)

    def add_values(self, values):
        for value in values:
            self.add_value(value)

    def add_value(self, value):
        if re.match(DiracFile.value_pattern, value):
            self.values.append(value)

    def __str__(self):
        printable = self.name
        for i in values:
            printable += i + '\n'
        return printable
#search the file,
#if you find a module, instantiate a module
class Module:#this are the guys with 2* (**)
    def __init__(self, name):
        if DiracFile.modules.get(name) == None:
            raise InvalidName('Module name invalid: '+name)
        self.name       = name
        self.submodules = {}
        self.properties = {}

    def add(self, lines):
        i = 0
        while i < len(lines):
##            if DiracFile.properties.get(lines[i]):

            if DiracFile.is_property(lines[i]):
                name = lines[i]
                values = []
                i += 1
                while i < len(lines) and DiracFile.is_value(lines[i]):
                    values.append(lines[i])
                    i += i
                self.add_property(name, values)

            elif DiracFile.is_submodule(lines[i]):
                name = lines[i]
                sublines = []
                i += 1
                while i < len(lines) and not DiracFile.is_submodule(lines[i]):
                    sublines.append(lines[i])
                    i += 1
                self.add_submodule(name, sublines)
            else:
                i += 1

    def add_submodule(self, name, lines):
        if not self.contains(name) and self.is_sub(name):
            sub = SubModule(name)
            sub.add_properties(lines)
            self.submodules.update({name: sub})
            return sub
        return None

    def contains(self, subname):
        return self.properties.__contains__(subname) or self.submodules.__contains__(subname)

    def is_sub(self, subname):
        temp = DiracFile.modules.get(self.name)
        sub = temp.submodules.get(subname)
        return  sub != None

    def add_property(self, name, values=None):
        if not self.contains(name) and self.is_prop(name):
            prop = Property(name)
            prop.add_values(values)
            return self.add_property(prop)
            self.properties.update({name:prop})
            return prop
        return None

##    def add_property(self, prop):
##        if not self.contains(prop.name) and self.is_prop(prop.name):
##            prop = Property(name)
##            prop.add_values(values)
##            self.properties.update({prop.name:prop})
##            return prop
##        return None


    def is_prop(self, subprop):
        temp = DiracFile.modules.get(self.name)
        prop = temp.properties.get(subprop)
        return prop != None

    def __str__(self):
        printable = self.name + '\n'
        for i in self.properties:
            printable += i.__str__()
        for i in self.submodules:
            printable += i.__str__()
        return printable
##        printable += self.properties.to_string()
##        printable += self.submodules.to_string()

class SubModule(Module): #this are the guys with only one *

    def __init__(self, name):
        if DiracFile.submodules.get(name) == None:
            raise InvalidName('SubModule name invalid: '+name)
        self.name = name
        self.properties = {}
        self.submodules = None

    def contains(self, subname):
        return self.properties.__contains__(subname)

    def add_submodule(self, subname):return None #submodules does not have submodules
    def is_sub(self, subname):return False

    def is_prop(self, subprop):
        temp = DiracFile.submodules.get(self.name)
        prop = temp.properties.get(subprop)
        return prop != None

    def add_properties(self, lines):
        i = 0
        while i < len(lines):
            if self.is_prop(lines[i]):
                name = lines[i]
                values = []
                i += 1
                while i < len(lines) and DiracFile.is_value(lines[i]):
                    values.append(lines[i])
                    i += 1
                self.add_property(name, values)
            else:
                i += 1

