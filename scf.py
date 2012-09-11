#-------------------------------------------------------------------------------
# Name:        scf
# Purpose:
#
# Author:      ezequiel
#
# Created:     02/09/2012
# Copyright:   (c) ezequiel 2012
# Licence:     <your licence>
#-------------------------------------------------------------------------------

from module import Module
from template import Template

class Scf:
    #the constructor
    def __init__(self, template, scf_file):
        self.modules = []
        self.template = template
        i = 0
        while i < len(scf_file):
            if self.template.is_module(scf_file[i]):
                name = scf_file[i]
                lines = []
                i += 1
                while not self.template.is_module(scf_file[i]) and scf_file[i] != '*END OF' and i < len(scf_file):
                    lines.append(scf_file[i])
                    i += 1
                self.addModuleByName(name, lines)
            else:
                i += 1

    def addModuleByName(self, name, lines=None):
            module = Module(name)
            module.add(self.template, lines)
            return self.addModule(module)

    def addModule(self, module):
        if not self.contains(module.name) and self.template.is_module(module.name):
            self.modules.append(module)
            return module
        return None

    #returns the module if it is in the list, good for checking if the module is in the list too
    def contains(self, name):
        for m in self.modules:
            if m.name == name:
                return m
        return None

    def __str__(self):
        printable = ''
        for i in self.modules:
            printable += i.__str__()
        printable += '*END OF\n'
        return printable

    def copy(self):
        the_copy = Scf(self.template, [])
        for module in self.modules:
            the_copy.modules.append(module.copy())
        return the_copy

    def remove(self, name):
        for i in range(len(self.modules)):
            if name == self.modules[i].name:
                return self.modules.pop(i)
        return None


