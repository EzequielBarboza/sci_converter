#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         london
# Purpose:      Keep and print information regarding the london.inp
#
# Author:      ezequiel.barboza
#
# Created:     13/10/2012
# Copyright:   (c) ezequiel.barboza 2012
# Licence:     GPL
#-------------------------------------------------------------------------------


from molecule import Molecule
from module import Module,Property,SubModule

#considering that the only change to be done in this file is regarding the plane and the symmetry
#nothing else is been taken from the mol and the scf.inp files
def write_london(template, scf, molecule):
    printable = ''
    wave_function = scf.contains(template.wave_function.name)
    if wave_function:
        scf_submodule = wave_function.submodules.get(template.scf.name)
        if scf_submodule:
            atomst = scf_submodule.properties.pop(template.atomst.name, None)

    for module in scf.modules:
        if module.name != template.visual.name:
            printable += module.__str__()

    nmr = SubModule('*NMR')
    nmr.add_property(template, '.LONDON')
    nmr.add_property(template, '.DOEPRN')
    nmr.add_property(template, '.INTFLG', ['1 1 0'])#calculating just large-large large-small

    newModule = Module('**PROPERTIES')
    newModule.add_property(template, '.' + molecule.magnetic_field)
    newModule.submodules.update({'*NMR':nmr})

    printable += newModule.__str__()
    printable += '*END OF\n'

    if atomst:
        scf_submodule.properties.update({atomst.name:atomst})

    return printable
