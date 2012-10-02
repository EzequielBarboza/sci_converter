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

#from template import Template

class Property:
    def __init__(self, name):
        self.name = name
        self.values = []

    def add_values(self, template, values):
        for value in values:
            self.add_value(template, value)

    def add_value(self, template, value):
        if template.is_value(value):
            self.values.append(value)

    def __str__(self):
        printable = self.name +'\n'
        for i in self.values:
            printable += i + '\n'
        return printable

    def copy(self):
        the_copy = Property(self.name)
        for value in self.values:
            the_copy.values.append(value)
        return the_copy

#search the file,
#if you find a module, instantiate a module
class Module:#this are the guys with 2* (**)
    def __init__(self, name):
        self.name       = name
        self.submodules = {}
        self.properties = {}

    def add(self, template, lines):
        i = 0
        while i < len(lines):
            if template.is_property(lines[i]):
                name = lines[i]
                values = []
                i += 1
                while i < len(lines) and template.is_value(lines[i]):
                    values.append(lines[i])
                    i += i
                self.add_property(template, name, values)

            elif template.is_submodule(lines[i]):
                name = lines[i]
                sublines = []
                i += 1
                while i < len(lines) and not template.is_submodule(lines[i]):
                    sublines.append(lines[i])
                    i += 1
                self.add_submodule(template, name, sublines)
            else:
                i += 1

    def add_submodule(self, template, name, lines):
        if not self.contains(name) and template.is_submodule(name):
            sub = SubModule(name)
            sub.add_properties(template, lines)
            self.submodules.update({name: sub})
            return sub
        return None

    def contains(self, subname):
        return self.properties.__contains__(subname) or self.submodules.__contains__(subname)

    def is_sub(self, subname):
        temp = self.template.modules.get(self.name)
        sub = temp.submodules.get(subname)
        return  sub != None

    def add_property(self, template, name, values=[]):
        if not self.contains(name) and self.is_prop(template, name):
            prop = Property(name)
            prop.add_values(template, values)
            self.properties.update({name:prop})
            return prop
        return None

    #add one property already created
    def addProperty(self, template, prop):
        if not self.contains(prop.name) and self.is_prop(template, prop.name):
            self.properties.update({prop.name : prop})
            return prop
        return None

    def is_prop(self, template, subprop):
        temp = template.modules.get(self.name)
        prop = temp.properties.get(subprop)
        return prop != None

    def __str__(self):
        printable = self.name + '\n'
        for i in self.properties.itervalues():
            printable += i.__str__()
        for i in self.submodules.itervalues():
            printable += i.__str__()
        return printable

    def copy(self):
        the_copy = self.shallow_copy()
        for prop in self.properties.itervalues():
            the_copy.properties.update({prop.name:prop.copy()})
        for sub in self.submodules.itervalues():
            the_copy.submodules.update({sub.name:sub.copy()})
        return the_copy

    def shallow_copy(self):
        return Module(self.name)

class SubModule(Module): #this are the guys with only one *

    def __init__(self, name):
        self.name = name
        self.properties = {}
        self.submodules = {}

    def contains(self, subname):
        return self.properties.__contains__(subname)

    def add_submodule(self, subname):return None #submodules does not have submodules
    def is_sub(self, subname):return False

    def is_prop(self, template, subprop):
        temp = template.submodules.get(self.name)
        prop = temp.properties.get(subprop)
        return prop != None

    #add one property by parsing a list of strings, the first is the property name
    #and the others are its values, until another property name is found
    def add_properties(self, template, lines):
        i = 0
        while i < len(lines):
            if self.is_prop(template, lines[i]):
                name = lines[i]
                values = []
                i += 1
                while i < len(lines) and template.is_value(lines[i]):
                    values.append(lines[i])
                    i += 1
                self.add_property(template, name, values)
            else:
                i += 1

    #add one property already created
    def addProperty(self, template, prop):
        if not self.contains(prop.name) and self.is_prop(template, prop.name):
            self.properties.update({prop.name : prop})
            return prop
        return None

    def shallow_copy(self):
        return SubModule(self.name)
