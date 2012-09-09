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

from module import DiracFile, Module, SubModule

class Scf:#(DiracFile):
    #the constructor
    def __init__(self, scf_file):
        self.modules = []
        i = 0
        while i < len(scf_file):
            if DiracFile.module_pattern.match(scf_file[i]):
                name = scf_file[i]
                lines = []
                i += 1
                while not DiracFile.module_pattern.match(scf_file[i]) and scf_file[i] != '*END OF' and i < len(scf_file):
                    lines.append(scf_file[i])
                    i += 1
                self.add_module(name, lines)
            else:
                i += 1
    def __init__(self):
        None

    def add_module(self, name, lines):
##        if not self.contains(name) and self.is_module(name):
            module = Module(name)
            module.add(lines)
            return self.add_module(module)
##            self.modules.append(module)
##            return module
##        return None

    def add_module(self, module):
        if not self.contains(module.name) and DiracFile.is_module(name):
            self.modules.append(module)
            return module
        return None

    def contains(self, name):
        for m in self.modules:
            if m.name == name:
                return m
        return None

    def __str__(self):
        printable = ''
        for i in modules:
            printable += i.to_string()
        printable += '*END OF\n'

    def copy(self):
        the_copy = Scf()

