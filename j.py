#!/usr/bin/env python

import string, math, re

from molecule   import Molecule#get_p_axis, get_biggest_coordinate
from module     import DiracFile,Module,Property
from commons    import MissingInformation

#from scf        import Scf

class J:#(DiracFile):
    def __init__(self, scf, molecule):# the j files are associated with a molecule
        self.scf = scf.copy()
        self.molecule = molecule
        self.dirac = scf.contains(DiracFile.dirac.name)
        self.hamiltonian = scf.contains(DiracFile.hamiltonian.name)
        #keep a copy of the integrals to be modified
        self.integrals = scf.contains(DiracFile.integrals.name)
        self.integrals = self.integrals.copy()
        self.integrals.pop(DiracFile.twoint.name)

        #if we dont have visual yet, get it
        self.derive_visual(hamiltonian)

        #print the default representation
        self.printable = dirac.name
        self.printable += hamiltonian.__str__()
        self.printable += integrals.__str__()

    def derive_visual(self, hamiltonian):
        visual = Module(DiracFile.visual.name)

        j = Property(DiracFile.j.name)
        j.add_value('PAMXVC 1')
        visual.add_property(j)

        london = Property(DiracFile.london.name)
        london.add_value(self.molecule.p_axis)
        visual.add_property(london)

        two_d = Property(DiracFile.two_d.name)

        biggest_ = str(math.ceil(self.molecule.biggest_coordinate() * 2))
        fst_point = ['-' + biggest_, '-' + biggest_]
        snd_point = [biggest_, '-' + biggest_]
        trd_point = ['-' + biggest_, biggest_]
        index = 0 if self.molecule.p_axis == 'X' else 1 if self.molecule.p_axis == 'Y' else 2
        fst_point.insert(index, '1.0')
        snd_point.insert(index, '1.0')
        trd_point.insert(index, '1.0')

        two_d.add_value(' '.join(fst_point))
        two_d.add_value(' '.join(snd_point))
        two_d.add_value('200')
        two_d.add_value(' '.join(trd_point))
        two_d.add_value('200')

        if hamiltonian.properties.get(DiracFile.lvcorr.name):
            jdia_prop = Property(DiracFile.jdia.name)
            jdia_prop.add_value('PAMXVC 2')
            visual.add_property(jdia_prop)
        elif hamiltonian.properties.get(DiracFile.levy_leblond.name):
            jdia_prop = Property(DiracFile.jdia.name)
            jdia_prop.add_value('DFCOEF')
            noreortho = Property(DiracFile.noreortho.name)
            nodirect = Property(DiracFile.nodirect.name)
            visual.add_property(jdia_prop)
            visual.add_property(noreortho)
            visual.add_property(nodirect)
        else:
            raise MissingInformation('Missing hamiltonian module from scf.inp file')

        self.scf.add_module(visual)

    def write_j_dia():
        #if we have lvcorr
        module = scf.contains(DiracFile.visual.name)
        backup_para = module.properties.pop(DiracFile.j.name)#remove the para information

        #change the name of the jdia property to j
        if self.hamiltonian.properties.get(DiracFile.lvcorr.name):
            backup_dia = module.properties.pop(DiracFile.jdia.name)
            newDia = Property(DiracFile.j.name)
            newDia.add_values(backup_dia.values)
            module.properties.update({newDia.name:newDia})

        self.printable += module.__str__()
        self.printable += '*END OF\n'

        module.properties.update({backup_para.name:backup_para})#puts the para back where it belongs

        if self.hamiltonian.properties.get(DiracFile.lvcorr.name):
            module.properties.update({backup_dia.name:backup_dia})

    def write_j_para(self):
        module = scf.contains(DiracFile.visual.name)
        #remove temporary the dia property
        backup_dia = module.properties.pop(DiracFile.jdia.name)
        #print the module
        self.printable += module.__str__()
        self.printable += '*END OF\n'
        #restore the backup of the dia information
        module.properties.update({backup_dia.name:backup_dia})

    def write_j_total(self):
        if self.hamiltonian.properties.get(DiracFile.lvcorr.name):
            backup_j = self.scf.modules.contains(DiracFile.j.name)
            backup_jdia = self.scf.modules.contains(DiracFile.jdia.name)
        else:
            return ''


        #this guys are the core of the file
        j_total_file.write('**DIRAC\n')
        j_total_file.write('#.WAVE FUNCTION\n')
        j_total_file.write('**HAMILTONIAN\n')
        j_total_file.write('.LEVY-LEBLOND\n')
        j_total_file.write('**INTEGRALS\n')
        j_total_file.write('*READIN\n')
        j_total_file.write('.UNCONTRACT\n')
        j_total_file.write('**WAVE FUNCTION\n')
        j_total_file.write('.SCF\n')
        j_total_file.write('**VISUAL\n')
        j_total_file.write('.JDIA\n')
        j_total_file.write(' DFCOEF\n')
        j_total_file.write('.NOREORTHO\n')
        j_total_file.write('.NODIRECT\n')
        j_total_file.write('.J\n')
        j_total_file.write(' PAMXVC 1\n')
        j_total_file.write('.LONDON\n')

        #retrieve the perpendicular plane in a molecule (the plane where most atoms are closer to zero)
        p_axis = get_p_axis(mol_file)
        axis = 'X' if p_axis == 'BXLAO' else 'Y' if p_axis == 'BYLAO' else 'Z'
        j_total_file.write(axis + '\n')

        j_total_file.write('.2D\n')

        biggest_ = str(math.ceil(get_biggest_coordinate(mol_file) * 2))
        fst_point = ['-' + biggest_, '-' + biggest_, '\n']
        snd_point = ['+' + biggest_, '-' + biggest_, '\n']
        trd_point = ['-' + biggest_, '+' + biggest_, '\n']
        index = 0 if axis == 'X' else 1 if axis == 'Y' else 2
        fst_point.insert(index, '1.0')
        snd_point.insert(index, '1.0')
        trd_point.insert(index, '1.0')

        j_total_file.write(' '.join(fst_point))
        j_total_file.write(' '.join(snd_point))
        j_total_file.write('200\n')
        j_total_file.write(' '.join(trd_point))
        j_total_file.write('200\n')

        j_total_file.write('*END OF\n')


    #    all_points = [fst_point, snd_point, trd_point]
    #    for point in all_points:
    #        if index == 0:
    #            temp = '1.0 '.join(string.join(point, " ")).join('\n')
    #        elif index == 1:
    #            temp = point[0].join(' ').join('1.0 ').join(point[1].join('\n'))
    #        else :
    #            temp = string.join(point, " ").join('1.0\n')
    #        j_dia_file.write(temp)
    #first_point = '-'.join(biggest_).join(' ').join('-').join(biggest_).join('\n')
    #second_point = '+'.join(biggest_).join(' ').join('-').join(biggest_).join('\n')
    #third_point = '-'.join(biggest_).join(' ').join('+').join(biggest_).join('\n')
