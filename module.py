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
from atoms import Atom
from commons import *

#one property may contain values. The values can be atoms, strings, or numbers
class Property:
    def __init__(self, name):
        self.name = name
        self.values = []

    def add_values(self, template, values):
        for value in values:
            self.add_value(template, value)

    def add_value(self, template, value):
        #one valud can be an Atom
        if isinstance(value, Atom):
            if self.name != template.atomst.name : raise InvalidParameter('Cannot insert Atom in property different from .ATOMST')
            for v in self.values:
                if isinstance(v, Atom) and v.symbol == value.symbol : self.values.remove(v)
            self.values.append(value)
        elif is_value(value):
            self.values.append(value)

    #return a string reprensentation
    def __str__(self):
        printable = self.name +NEW_LINE
        for i in self.values:
            printable += i.__str__() + NEW_LINE
        return printable

    #return a full copy
    def copy(self):
        the_copy = Property(self.name)
        for value in self.values:
            the_copy.values.append(value)
        return the_copy

    #return a copy without the values
    def shallow_copy(self):
        return Property(self.name)

#search the file,
#if you find a module, instantiate a module
class Module:#this are the guys with 2* (**)
    def __init__(self, name):
        self.name       = name
        self.submodules = {}
        self.properties = {}

    #add properties an submodules to a Module through the parsing of a list of entries
    def parse(self, template, lines):
        i = 0
        while i < len(lines):
            if template.properties.get(lines[i]):#if it is a property
                name = lines[i]
                values = []
                i += 1
                while i < len(lines) and is_value(lines[i]):
                    values.append(lines[i])
                    i += i
                prop = Property(name)
                prop.add_values(template, values)
                self.addProperty(template, prop)
            elif template.submodules.get(lines[i]):# else if it is a submodule
                name = lines[i]
                sublines = []
                i += 1
                while i < len(lines) and not template.submodules.get(lines[i]):
                    sublines.append(lines[i])
                    i += 1
                submodule = SubModule(name)
                submodule.parse(template, sublines)
                self.addSubModule(template, submodule)
            else:
                i += 1

    #add one already created submodule. ! Attention!! if the submodule already exists, it will be replaced
    def addSubModule(self, template, submodule):
        self.validateSubmodule(template, submodule)
        self.submodules.update({submodule.name : submodule})

    #abstracts (hide) the direct access to the inner of the module
    def getSubModule(self, template, submodule):
        self.validateSubmodule(template, submodule)
        return self.submodules.get(submodule.name)

    def removeSubModule(self, template, submodule):
        self.validateSubmodule(template, submodule)
        if self.submodules.has_key(submodule.name):
            return self.submodules.pop(submodule.name)
        return None

    #verifies if one submodule belongs to this Module
    def validateSubmodule(self, template, submodule):
        if not isinstance(submodule, SubModule) : raise InvalidParameter(str(submodule) + ' is not a SubModule')
        if not template.modules.get(self.name).submodules.get(submodule.name) : raise InvalidParameter(str(submodule) + ' is not a valid SubModule for ' + str(self))

    #add one property already created ! note: if the property already exists in the module, it will be overwritten
    def addProperty(self, template, prop):
        self.validateProperty(template, prop)
        self.properties.update({prop.name : prop})

    def getProperty(self, template, prop):
        self.validateProperty(template, prop)
        return self.properties.get(prop.name)

    def removeProperty(self, prop):
        if not isinstance(prop, Property) : raise InvalidParameter( prop, Property)

        if self.properties.has_key(prop.name):
            return self.properties.pop(prop.name)
        return None

    def validateProperty(self, template, prop):
        if not isinstance(prop, Property) : raise InvalidParameter(prop, Property)
        if not template.modules.get(self.name).properties.get(prop.name) : raise InvalidParameter(prop, self)

    def __str__(self):
        printable = self.name + NEW_LINE
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

    #add one property by parsing a list of strings, the first is the property name
    #and the others are its values, until another property name is found
    def parse(self, template, lines):
        i = 0
        while i < len(lines) :
            name = lines[i]
            values = []
            i += 1
            while i < len(lines) and is_value(lines[i]):
                values.append(lines[i])
                i += 1
            prop = Property(name)
            prop.add_values(template, values)
            self.addProperty(template, prop)

    #add one property already created
    def addProperty(self, template, prop):
        self.validateProperty(template, prop)
        self.properties.update({prop.name:prop})

    def getProperty(self, template, prop):
        self.validateProperty(template, prop)
        return self.properties.get(prop.name)

    def validateProperty(self, template, prop):
        if not isinstance(prop, Property) : raise InvalidParameter(str(prop) + ' is not a Property')
        if not template.submodules.get(self.name).properties.get(prop.name) : raise InvalidParameter(str(prop) + ' is not a valid Property for ' + self.name)

    def shallow_copy(self):
        return SubModule(self.name)
