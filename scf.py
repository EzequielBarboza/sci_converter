#-------------------------------------------------------------------------------
# Name:        scf
# Purpose:      The scf is a dirac input file composed of several modules, which
#               are instructions to the dirac system of the calculations to be performed.
#               1. Read the scf.inp given with instructions to create a set of
#               other input files(j,integrate,london...)
#               2. Add new modules (if needed) to improve the dirac calculations
#               with this file
#
# Author:      ezequiel
#
# Created:     02/09/2012
# Copyright:   (c) ezequiel 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

from module import Module

class Scf:
    #the constructor reads from the input and generates a set of modules.
    #these modules are used further by the other parts of the system to generate
    #other files. The constructor also adds the atomst module if it was not
    #in the original input
    def __init__(self, template, scf_file, atoms):
        self.modules = []
        self.template = template
        i = 0
        #iterate over the input generating the modules
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
        #add the atomst module if it was not in the original input
        wave_function = self.getModule(template.wave_function)
        if wave_function:# if the module exists, proceed searching for the submodule
            scf = wave_function.getSubmodule(template.scf)
            if scf:# if the submodule existis, proceed searching for the property
                atomst = scf.getProperty(template.atomst)
                if not atomst:#if we don't have the atomst, copy from the template and add the atoms values
                    atomst = template.atomst.copy()
                    for atom in atoms:
                        atomst.addAtomAsValue(template, atom)
                    scf.addProperty(template, atomst)

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
    #new version of the constains function. This has a more significative name
    # and receives a module
    def getModule(self, module):
        if not isinstance(module, Module) : return None
        for m in self.modules:
            if m.name == module.name:
                return m
        return None

    def __str__(self):
        printable = ''
        for i in self.modules:
            printable += i.__str__()
        printable += '*END OF\n'
        return printable

    def copy(self):
        the_copy = Scf(self.template, [], [])
        for module in self.modules:
            the_copy.modules.append(module.copy())
        return the_copy

    # safelly remove one module by name
    def remove(self, name):
        for i in range(len(self.modules)):
            if name == self.modules[i].name:
                return self.modules.pop(i)
        return None


