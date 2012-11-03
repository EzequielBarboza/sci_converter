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

from scf import Scf

class London(Scf):
    def __init__(self, scf, molecule):
        self.validateScf(scf)
        self.modules = scf.copy().modules
        template = self.template

        #remove **wave_function.*scf..atomst
        scf_submodule = self.getModule(template.wave_function).getSubModule(template, template.scf)
        scf_submodule.removeProperty(self.template.atomst)

        # remove the visual module
        self.removeModule(self.template.visual)

        london = self.template.london.shallow_copy()
        doeprn = self.template.doeprn.shallow_copy()
        intflg = self.template.intflg.shallow_copy()
        intflg.add_value(self.template, '1 1 0')#calculating just large-large large-small
        nmr = self.template.nmr.shallow_copy()
        nmr.addProperty(self.template, london)
        nmr.addProperty(self.template, doeprn)
        nmr.addProperty(self.template, intflg)

        properties = self.template.prop_module.shallow_copy()
        magnetic_field   = template.properties.get('.' + molecule.magneticField).shallow_copy()
        properties.addProperty(self.template, magnetic_field)
        properties.addSubModule(self.template, nmr)

        self.addModule(properties)
