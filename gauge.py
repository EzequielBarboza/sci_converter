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


from molecule import Molecule
from module import Module,Property,SubModule
from scf import Scf

#copy a set of modules from a given scf
class Gauge(Scf):
    def __init__(self, template, scf, molecule):
        self.template = template
        self.modules = scf.copy().modules

        #remove **wave_function.*scf..atomst
        wave_function = self.getModule(template.wave_function)
        if wave_function:
            scf_submodule = wave_function.submodules.get(template.scf.name)
            if scf_submodule:
                atomst = scf_submodule.properties.pop(template.atomst.name, None)

        # remove the visual module
        self.remove(template.visual)

        # add one new module **PROPERTIES
        #first add the .A OPERATOR, .B OPERATOR AND .ANALIZE
        a_operator  = Property(template.a_operator.name)
        b_operator  = Property(template.b_operator.name)
        analize     = Property(template.analize.name)

        a_operator.add_value(template, '\'B_' + molecule.p_axis.lower() + ' oper\'')
        b_operator.add_value(template, '\'B_' + molecule.p_axis.lower() + ' oper\'')

        a_operator.add_value(template, molecule.p_axis + 'AVECTOR')
        b_operator.add_value(template, molecule.p_axis + 'AVECTOR')

        axis_enum = molecule.axis_enum
        a_operator.add_value(template, '\'' + axis_enum[0] + 'DIPLEN\'')
        b_operator.add_value(template, '\'' + axis_enum[0] + 'DIPLEN\'')

        a_operator.add_value(template, '\'' + axis_enum[1] + 'DIPLEN\'')
        b_operator.add_value(template, '\'' + axis_enum[1] + 'DIPLEN\'')

        a_operator.add_value(template, 'COMFACTOR')
        b_operator.add_value(template, 'COMFACTOR')

        a_operator.add_value(template, '-68.517999904721')
        b_operator.add_value(template, '-68.517999904721')

        #add the properties to the submodule
        linear_response = SubModule(template.linear_response.name)
        linear_response.addProperty(template, a_operator)
        linear_response.addProperty(template, b_operator)
        linear_response.addProperty(template, analize)

        #then add the *NMR submodule
        gaugeo = Property(template.gaugeo.name)
        gaugeo.add_value(template, '0.0 0.0 0.0')
        nmr = SubModule(template.nmr.name)
        nmr.addProperty(template, gaugeo)

        #and add the submodule to the module
        newModule = Module(template.prop_module.name)
        newModule.addSubmodule(template, linear_response)
        newModule.addSubmodule(template, gaugeo)

        self.addModule(newModule)
