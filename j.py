#!/usr/bin/env python

import string, math, re

from molecule   import Molecule#get_p_axis, get_biggest_coordinate
from module     import Module,Property
from commons    import MissingInformation

#from scf        import Scf

class J:
    def __init__(self, template, scf_original, molecule):# the j files are associated with a molecule
        self.scf = scf_original.copy()
        self.molecule = molecule
#all we want from **dirac is the name
        dirac = self.scf.contains(template.dirac.name)
        dirac.properties.clear()
        dirac.submodules.clear()
#we want all the self.hamiltonian
        self.hamiltonian = self.scf.contains(template.hamiltonian.name)

#and just a piec of the integrals
        integrals = self.scf.contains(template.integrals.name)
        integrals.submodules.pop(template.twoint.name, None)

#remove all the rest
        self.scf.modules = [dirac, self.hamiltonian, integrals]
#set the common part to print
        self.printable = self.scf.__str__()

#and the visual, which we have to create. if we dont have visual yet, get it
        self.derive_visual(template)

    def derive_visual(self, template):
        visual = Module(template.visual.name)

        #jdia property
        if self.hamiltonian.properties.get(template.lvcorr.name):
            visual.add_property(template, template.jdia.name, ['PAMXVC 2'])
        elif self.hamiltonian.properties.get(template.levy_leblond.name):
            visual.add_property(template, template.jdia.name, ['DFCOEF'] )
            visual.add_property(template, template.noreortho.name )
            visual.add_property(template, template.nodirect.name )
        else:
            raise MissingInformation('Missing hamiltonian module from scf.inp file')

        visual.add_property(template, template.j.name, ['PAMXVC 1'])

        visual.add_property(template, template.london.name, [self.molecule.p_axis])

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

        visual.add_property(template, template.two_d.name, values_for_two_d)

        self.scf.addModule(visual)

    def write_j_dia(self, template):
        #if we have lvcorr
        visual = self.scf.contains(template.visual.name)
        backup_para = visual.properties.pop(template.j.name, None)#remove the para information

        #change the name of the jdia property to j
        if self.hamiltonian.properties.get(template.lvcorr.name):
            backup_dia = visual.properties.pop(template.jdia.name, None)
            if backup_dia:
                newDia = Property(template.j.name)
                newDia.add_values(template, backup_dia.values)
                visual.properties.update({newDia.name:newDia})

        printable = self.printable
        printable += visual.__str__()
        printable += '*END OF\n'

        visual.properties.update({template.j.name:backup_para})#puts the para back where it belongs

        if self.hamiltonian.properties.get(template.lvcorr.name):
            visual.properties.update({backup_dia.name:backup_dia})
        return printable

    def write_j_para(self, template):
        visual = self.scf.contains(template.visual.name)
        #remove temporary the dia property
        backup_dia = visual.properties.pop(template.jdia.name, None)
        #print the module
        printable = self.printable# se essa merda nao copiar a merda da string essa merda de linguagem que va a merda
        printable += visual.__str__()
        printable += '*END OF\n'
        #restore the backup of the dia information
        visual.properties.update({template.jdia.name:backup_dia})

        return printable

    def write_j_total(self, template):
        if self.hamiltonian.properties.get(template.lvcorr.name):
            visual = self.scf.contains(template.visual.name)

            backup_jdia = visual.properties.pop(template.jdia.name, None)

            if not backup_jdia: return ''

            backup_jdia.name = 'J'
            printable = self.printable
            printable += visual.name + '\n'
            printable += backup_jdia.__str__()
            for prop in visual.properties.itervalues():
                printable += prop.__str__()
            for sub in visual.submodules.itervalues():
                printable += sub.__str__()

            backup_jdia.name = template.jdia.name
            visual.properties.update({backup_jdia.name:backup_jdia})
            return printable

        else:
            return ''#for now, we wait for the inclusion of on script to generate the correct jtotal for levy-leblond
