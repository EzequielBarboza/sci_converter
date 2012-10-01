#!/usr/bin/env python
#-------------------------------------------------------------------------------
# Name:        job
# Purpose:  Creates a Dirac job script based on data that comes from the mol.mol
# file
#
# Author:      ezequiel
#
# Created:     29/09/2012
# Copyright:   (c) ezequiel 2012
# Licence:     GPL
#-------------------------------------------------------------------------------

class Job():
    def __init__(self, scf_file_name, mol_file_name, output_files, molecule):
        self.scf_file_name      = scf_file_name
        self.mol_file_name      = mol_file_name
        self.london_file_name   = output_files[0]
        self.j_dia_file         = output_files[1]
        self.j_para_file        = output_files[2]
        self.j_total_file       = output_files[3]
        self.int_dia_file       = output_files[4]
        self.int_para_file      = output_files[5]
        self.int_total_file     = output_files[6]
        self.molecule           = molecule

    def write_job(self):
#print the #atomic start
        printable = '#atomic start\n'
        for atom in self.molecule.atoms:
            printable += 'pam --mpi=8 --global-scratch-disk --noarch --mb=1200'
            printable += ' --inp=' + atom.symbol.lower() + '.inp'
            printable += ' --mol=' + atom.symbol.lower() + '.mol'
            printable += ' --get="DFACMO"'
            printable += '\n'
            printable += ' cp DFACMO ' + atom.symbol + 'COEF'
#print the #scf
        printable += '\n'
        printable += '#scf\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.scf_file_name
        printable += ' --mol=' + self.mol_file_name
        printable += ' --get="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'cp DFCOEF DFCOEF_scf'
        printable += '\n'
        printable += 'cp PAMXVC PAMXVC_scf'
#print the #london
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200 --incmo'
        printable += ' --inp=' + self.london_file_name
        printable += ' --mol=' + self.mol_file_name
        printable += ' --get="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'cp DFCOEF DFCOEF_l'
        printable += '\n'
        printable += 'cp PAMXVC PAMXVC_l'
        printable += '\n'
        printable += 'cp TBMO TBMO_l'
#print the #currents
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.j_dia_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --get="plot.2d.vector"'
        printable += ' --put="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'cp plot.2d.vector plot.2d.vector.dia'
        printable += '\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.j_para_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --get="plot.2d.vector"'
        printable += ' --put="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'cp plot.2d.vector plot.2d.vector.para'
        printable += '\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.j_total_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --get="plot.2d.vector" --put="DFCOEF PAMXVC TBMO"'
        printable += 'cp plot.2d.vector plot.2d.vector.total'
#print the #integration
        printable += '\n'
        printable += '#integration'
        printable += '\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.int_total_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --put="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.int_para_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --put="DFCOEF PAMXVC TBMO"'
        printable += '\n'
        printable += 'pam --mpi=8 --global-scratch-disk --mb=1200'
        printable += ' --inp=' + self.int_dia_file
        printable += ' --mol=' + self.mol_file_name
        printable += ' --put="DFCOEF PAMXVC TBMO"'
