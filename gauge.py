#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:         gauge
# Purpose:      Keep and print information regarding the gauge.inp
#
# Author:      ezequiel.barboza
#
# Created:     13/10/2012
# Copyright:   (c) ezequiel.barboza 2012
# Licence:     GPL
#-------------------------------------------------------------------------------


##from molecule import Molecule
##from module import Module,Property,SubModule
from scf import Scf

#copy a set of modules from a given scf, generates a set of outputs different from the london
class Gauge(Scf):
    def __init__(self, scf, molecule):
        self.modules = scf.copy().modules

        #remove **wave_function.*scf..atomst
        wave_function = self.getModule(self.template.wave_function)
        if wave_function:
            scf_submodule = wave_function.getSubModule(self.template, self.template.scf)
            if scf_submodule:
                scf_submodule.removeProperty(self.template.atomst)

        # remove the visual module
        self.removeModule(self.template.visual)

        # add one new module **PROPERTIES
        #first add the .A OPERATOR, .B OPERATOR AND .ANALIZE
        a_operator  = self.template.a_operator.shallow_copy()
        b_operator  = self.template.b_operator.shallow_copy()
        analize     = self.template.analize.shallow_copy()

        a_operator.add_value(self.template, '\'B_' + molecule.p_axis.lower() + ' oper\'')
        b_operator.add_value(self.template, '\'B_' + molecule.p_axis.lower() + ' oper\'')

        a_operator.add_value(self.template, molecule.p_axis + 'AVECTOR')
        b_operator.add_value(self.template, molecule.p_axis + 'AVECTOR')

        axis_enum = molecule.axis_enum
        a_operator.add_value(self.template, '\'' + axis_enum[0] + 'DIPLEN\'')
        b_operator.add_value(self.template, '\'' + axis_enum[0] + 'DIPLEN\'')

        a_operator.add_value(self.template, '\'' + axis_enum[1] + 'DIPLEN\'')
        b_operator.add_value(self.template, '\'' + axis_enum[1] + 'DIPLEN\'')

        a_operator.add_value(self.template, 'COMFACTOR')
        b_operator.add_value(self.template, 'COMFACTOR')

        a_operator.add_value(self.template, '-68.517999904721')
        b_operator.add_value(self.template, '-68.517999904721')

        #add the properties to the submodule
        linear_response = self.template.linear_response.shallow_copy()
        linear_response.addProperty(self.template, a_operator)
        linear_response.addProperty(self.template, b_operator)
        linear_response.addProperty(self.template, analize)

        #then add the *NMR submodule
        gaugeo = self.template.gaugeo.shallow_copy()
        gaugeo.add_value(self.template, '0.0 0.0 0.0')
        nmr = self.template.nmr.shallow_copy()
        nmr.addProperty(self.template, gaugeo)

        #and add the submodule to the module
        newModule = self.template.prop_module.shallow_copy()
        newModule.addSubModule(self.template, linear_response)
        newModule.addSubModule(self.template, nmr)

        self.addModule(newModule)
