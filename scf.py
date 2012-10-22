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

from module     import Module
from template   import Template
from commons    import InvalidParameter, is_comment, MissingInformation

class Scf(object):
    template = Template()
    #the constructor reads from the input and generates a set of modules.
    #these modules are used further by the other parts of the system to generate
    #other files. The constructor also adds the .ATOMST to the **WAVE FUNCTION from a given set of atoms
    def __init__(self, scf_file=[], atoms=[]):
        self.modules = []
        if len(scf_file) > 0:
            self.parse(scf_file)
        #perform a validation before proceeding, to make the atomst insertion safe
        self.validateScf(self)
        #insert the atoms
        if len(atoms) > 0:
            #insert the atomst
            scfSubmodule = self.getModule(self.template.wave_function).getSubmodule(self.template.scf)
            if scfSubmodule :
                atomst = self.template.atomst.shallow_copy()
                for atom in atoms:
                    atomst.add_value(self.template, atom)
                scfSubmodule.addProperty(self.template, atomst)

    # receives a list of entries and constructs a set of modules
    def parse(self, scf_file):
        i = 0
        #iterate over the input generating the modules
        while i < len(scf_file):
            if self.template.modules.get(scf_file[i]):
                name = scf_file[i]
                lines = []
                i += 1
                #while does not encounter other module or the end of the file, all the lines belong to this module
                while not self.template.modules.get(scf_file[i]) and scf_file[i] != '*END OF' and i < len(scf_file) :
                    if not is_comment(scf_file[i]) : lines.append(scf_file[i])
                    i += 1
                module = Module(name)
                module.parse(self.template, lines)
                self.addModule(module)
            else:
                i += 1

    # append one new module, replacing one old with the same name if such exists
    def addModule(self, module):
        self.validateModule(module)
        #if the module already exists, replace it
        for i in range(len(self.modules)):
            if module.name == self.modules[i].name:
                self.modules.pop(i)
                self.modules.insert(i, module)
                return
        self.modules.append(module)

    # and receives a module
    def getModule(self, module):
        self.validateModule(module)
        for m in self.modules:
            if m.name == module.name:
                return m
        return None

    # safelly remove one module by name
    def removeModule(self, module):
        self.validateModule(module)
        for i in range(len(self.modules)):
            if module.name == self.modules[i].name:
                return self.modules.pop(i)
        return None

    #any operation over a module must validate if the module is valid
    def validateModule(self, module):
        if not isinstance(module, Module) : raise InvalidParameter(module, Module)
        if not self.template.modules.get(module.name) : raise InvalidParameter(module, Module)

    #the rules for the well formed Scf
    def validateScf(self, scf):
        template = self.template
        if not isinstance(scf, Scf) : raise InvalidParameter(scf, Scf)
        #**DIRAC IS MANDATORY
        if not scf.getModule(template.dirac) : raise MissingInformation( str(scf) + ' state is invalid : there is no **DIRAC module' )
        #**HAMILTONIAN IS MANDATORY
        hamiltonian = scf.getModule(template.hamiltonian)
        if not hamiltonian : raise MissingInformation( str(scf) + ' state is invalid : there is no **HAMILTONIAN module' )
        if not hamiltonian.getProperty(template, template.lvcorr) and not hamiltonian.getProperty(template, template.levy_leblond):
            raise MissingInformation(str(hamiltonian) + ' state is invalid : there is no .LVCORR or .LEVY-LEBLOND properties')
        #**INTEGRALS IS MANDATORY
        if not scf.getModule(template.integrals) : raise MissingInformation( str(scf) + ' state is invalid : there is no **INTEGRALS module' )
        #**WAVE FUNCTION IS MANDATORY
        wave_function = scf.getModule(template.wave_function)
        if not  wave_function : raise MissingInformation( str(scf) + ' state is invalid : there is no **WAVE FUNCTION module' )
        if not wave_function.getSubmodule(template.scf) : raise MissingInformation(str(wave_function) + ' state is invalid: there is no *SCF submodule')

    def copy(self):
        the_copy = Scf()
        for module in self.modules:
            the_copy.modules.append(module.copy())
        return the_copy

    def __str__(self):
        printable = ''
        for i in self.modules:
            printable += str(i)
        printable += '*END OF\n'
        return printable
