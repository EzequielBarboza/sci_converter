#!/usr/bin/env python

import string, math, re

from molecule   import Molecule#get_p_axis, get_biggest_coordinate
from commons    import MissingInformation, InvalidParameter

from scf        import Scf

class J(Scf):
    def __init__(self, scf, molecule, isLondon=True):# the j files are associated with a molecule
#basic validation
        self.validateScf(scf)
        template = self.template#create local variable to ease the reference

#basic initialization
        self.modules    = scf.copy().modules
        self.isLvcorr   = self.getModule(template.hamiltonian).getProperty(template, template.lvcorr)
        self.isLondon   = isLondon
        self.molecule   = molecule

#assemble a **INTEGRALS special for the j calculations
        integrals = self.getModule(template.integrals)
        if integrals:
            integrals.removeSubModule(template.twoint)#don't ask me why... it is just a requirement... :-(
        self.addModule(integrals)

#assemble a **WAVE FUNCTION, but with just some properties
        wave_function   = template.wave_function.shallow_copy()
        scf_prop        = template.scf_prop.shallow_copy()
        wave_function.addProperty(template, scf_prop)

#assemble the **VISUAL
        visual = self.createVisualModule(self.getModule(template.hamiltonian))
#add the .LONDON only if it is a london calculation
        if isLondon :
            london = template.london.shallow_copy()
            london.add_value(template, molecule.p_axis)
            visual.addProperty(template, london)

#remove all the modules, except the ones bellow
        self.modules = [template.dirac.shallow_copy(),
                        self.getModule(template.hamiltonian),
                        integrals,
                        wave_function,
                        visual]

    def __str__(self):
        #set the common part to print
        printable = ''
        #from sp01 ahead, have to print the #.WAVE FUNCTION, so remove dirac temporally
        dirac = self.removeModule(self.template.dirac)
        printable += str(dirac)
        printable += '#.WAVE FUNCTION\n'
        for module in self.modules:
            printable += str(module)
        printable += '*END OF\n'
        #put the dirac back
        self.modules.insert(0, dirac)
        return printable

    def createVisualModule(self, hamiltonian):
        template = self.template#create local variable to ease reference
        visual = template.visual.shallow_copy()

        #.JDIA property
        if hamiltonian.getProperty(template, template.lvcorr):
            jdia = template.jdia.shallow_copy()
            jdia.add_value(template, 'PAMXVC 2')
            visual.addProperty(template, jdia)
        elif hamiltonian.getProperty(template, template.levy_leblond):
            jdia = template.jdia.shallow_copy()
            jdia.add_value(template, 'DFCOEF')
            visual.addProperty(template, jdia)
            if self.isLondon :
                visual.addProperty(template, template.noreortho.shallow_copy())
                visual.addProperty(template, template.nodirect.shallow_copy())

        #.J property
        j = template.j.shallow_copy()
        j.add_value(template, 'PAMXVC 1')
        visual.addProperty(template, j)

        # two_d
        biggest_ = str(math.ceil(self.molecule.biggest_coordinate * 2))
        fst_point = ['-' + biggest_, '-' + biggest_]
        snd_point = [biggest_, '-' + biggest_]
        trd_point = ['-' + biggest_, biggest_]
        index = 0 if self.molecule.p_axis == 'X' else 1 if self.molecule.p_axis == 'Y' else 2
        fst_point.insert(index, '1.0')
        snd_point.insert(index, '1.0')
        trd_point.insert(index, '1.0')

        values_for_two_d = []
        values_for_two_d.append(' '.join(fst_point))
        values_for_two_d.append(' '.join(snd_point))
        values_for_two_d.append('200')
        values_for_two_d.append(' '.join(trd_point))
        values_for_two_d.append('200')

        two_d = template.two_d.shallow_copy()
        two_d.add_values(template, values_for_two_d)

        visual.addProperty(template, two_d)
        return visual

    def validateJ(self, j):
        if not isinstance(j, J) : raise InvalidParameter(j, J)
        if not j.getModule(self.template.visual) : raise MissingInformation('J state is invalid : there is no **VISUAL module')
        if not j.getModule(self.template.hamiltonian) : raise MissingInformation('J state is invalid : there is no **HAMILTONIAN module' )

    #overrides the super method because it needs
    def copy(self):
        the_copy = super(J, self).copy()
        the_copy.isLvcorr = self.isLvcorr
        the_copy.isLondon = self.isLondon
        return the_copy

class JDia(J):
    def __init__(self, j):
        self.validateJ(j) # the j should be valid
        #basic initialization
        self.modules = j.copy().modules #copy the modules from the father J
        template = self.template #create local variable, in order to get easier to use it here

        #if we have lvcorr
        visual = self.getModule(template.visual)
        # j_dia files are not supposed to have .J (para) modules, so remove it
        visual.removeProperty(template.j)#remove the para information

        # in the j_dia files, the .JDIA is called simply .J (of course!!!), so rename it but only if the **HAMILTONIAN have the .LVCORR property
        if self.getModule(template.hamiltonian).getProperty(template, template.lvcorr):
            visual.getProperty(template, template.jdia).name = self.template.j.name

class JPara(J):
    def __init__(self, j):
        #basic initializations
        self.validateJ(j)
        self.modules = j.copy().modules
        template = self.template
        #remove .noreortho
        self.getModule(template.visual).removeProperty(template.noreortho)
        #remove the .nodirect property
        self.getModule(template.visual).removeProperty(template.nodirect)
        #remove the jdia property (this is the jpara file, duh...)
        self.getModule(template.visual).removeProperty(template.jdia)

class JTotal(J):
    def __init__(self, j):
        #basic initializations
        self.validateJ(j)
        the_father = j.copy()#instead of having to call the super with its attributes, get just what we need from the super
        self.modules = the_father.modules
        self.isLvcorr = the_father.isLvcorr
        self.isLondon = the_father.isLondon
        template = self.template

        # note that, after this change, the JTotal will have two properties with the same name : .J
        if not self.isLondon or (self.isLondon and self.isLvcorr) :
            self.getModule(template.visual).getProperty(template, template.jdia).name = template.j.name

    def __str__(self):
        if self.isLondon and not self.isLvcorr :
            return ''
        else :
            return super(JTotal, self).__str__()
#for now, we wait for the inclusion of on script to generate the correct jtotal for levy-leblond
#what happens is that the london calculations with levy-leblond are kind recent on dirac
# so they have to be calculated later using a script that sums up the para and dia files : the add-plots.py