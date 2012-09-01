#!/usr/bin/env python

from mol import get_p_axis
import os

class Integrate():
    def __init__(self, output_path, mol_file):
        # each index in the arrays represent an axis
        #gross translation of what is a dot, to number index in a array [x,y,z]=[0,0,0]
        XZ = [0,2]
        YZ = [1,2]
        XY = [0,1]
        line1 = [0.0, 0.0, 0.0]#each of this lines in the file, represent a line to be written to the output
        line2 = [0.0, 0.0, 0.0]#coordinates in the cartesian space
        line3 = [0.0, 0.0, 0.0]

        #retrieve the perpendicular plane in a molecule (the plane where most atoms are closer to zero)
        self.p_axis = get_p_axis(mol_file)
        self.p_axis = 'X' if self.p_axis == 'BXLAO' else 'Y' if self.p_axis == 'BYLAO' else 'Z'

        self.p_planes = [YZ, XZ] if self.p_axis == 'Z' else [XZ, XY] if self.p_axis == 'X' else [YZ, XY]
        self.axis_enum = ['X', 'Y', 'Z']#enumeration of the axis
        self.output_path = output_path

        #now, calculating
        #since I found the perpendicular axis of a molecule, I can say that I can tranform it in two directions
        #say, it is Z, there are (at least) two perpendicular self.p_planes to the molecule,
        #XZ and YZ, then, I don't move the center of the coordinates: line1
        #but move the other two, since there are 2 possibilities, we have to create 2 output files

        #self.p_planes discovered, lets assemble 2 possible outputs
        indexForLine2 = self.p_planes[0][0]#this is the value of the first axis
        indexForLine3 = self.p_planes[0][1]#this is the value of the second axis
        line2[indexForLine2] = 10.0
        line3[indexForLine3] = 10.0

        self.output1 = []
        self.output1.append(' '.join(map(str, line1)))
        self.output1.append(' '.join(map(str, line2)))
        self.output1.append(10)
        self.output1.append(' '.join(map(str, line3)))
        self.output1.append(10)
        self.output1.append(10)
        self.output1.append('*END OF')

        #reset everything
        line2 = [0.0, 0.0, 0.0]
        line3 = [0.0, 0.0, 0.0]
        indexForLine2 = self.p_planes[1][0]#this is the value of the first axis
        indexForLine3 = self.p_planes[1][1]#this is the value of the second axis
        line2[indexForLine2] = 10.0
        line3[indexForLine3] = 10.0

        self.output2 = []
        self.output2.append(' '.join(map(str, line1)))
        self.output2.append(' '.join(map(str, line2)))
        self.output2.append(10)
        self.output2.append(' '.join(map(str, line3)))
        self.output2.append(10)
        self.output2.append(10)
        self.output2.append('*END OF')

        self.common_lines = []
        self.common_lines.append('**DIRAC')
        self.common_lines.append('#.WAVE FUNCTION')
        self.common_lines.append('**HAMILTONIAN')
        self.common_lines.append('#.LVCORR')
        self.common_lines.append('#.URKBAL')
        self.common_lines.append('.LEVY-LEBLOND')
        self.common_lines.append('**INTEGRALS')
        self.common_lines.append('*READIN')
        self.common_lines.append('.UNCONTRACT')
        self.common_lines.append('**WAVE FUNCTION')
        self.common_lines.append('.SCF')
        self.common_lines.append('**VISUAL')

    def write_integrate_dia(self) :
        file_name1 = 'integrate_dia_' + self.axis_enum[self.p_planes[0][0]] + self.axis_enum[self.p_planes[0][1]] + '.inp'
        integrate_dia_file1 = open(self.output_path + os.sep + file_name1, 'w')

        file_name2 = 'integrate_dia_' + self.axis_enum[self.p_planes[1][0]] + self.axis_enum[self.p_planes[1][1]] + '.inp'
        integrate_dia_file2 = open(self.output_path + os.sep + file_name2, 'w')

        dia_lines = []
        dia_lines.append('.JDIA')
        dia_lines.append(' DFCOEF')
        dia_lines.append('.NOREORTHO')
        dia_lines.append('.NODIRECT')
        dia_lines.append('#.J')
        dia_lines.append('# PAMXVC 1')
        dia_lines.append('.LONDON')
        dia_lines.append(self.p_axis)
        dia_lines.append('.2D_INT')

        for line in self.common_lines:
            integrate_dia_file1.write(line + '\n')
            integrate_dia_file2.write(line + '\n')

        for line in dia_lines:
            integrate_dia_file1.write(line + '\n')
            integrate_dia_file2.write(line + '\n')

        for line in self.output1:
            integrate_dia_file1.write(str(line) + '\n')

        for line in self.output2:
            integrate_dia_file2.write(str(line) +'\n')

        integrate_dia_file1.close()
        integrate_dia_file2.close()

    def write_integrate_para(self):
        file_name1 = 'integrate_para_' + self.axis_enum[self.p_planes[0][0]] + self.axis_enum[self.p_planes[0][1]] + '.inp'
        integrated_para_file1 = open(self.output_path + os.sep + file_name1, 'w')

        file_name2 = 'integrate_para_' + self.axis_enum[self.p_planes[1][0]] + self.axis_enum[self.p_planes[1][1]] + '.inp'
        integrated_para_file2 = open( self.output_path + os.sep + file_name2, 'w')

        para_lines = []
        para_lines.append('#.JDIA')
        para_lines.append('# DFCOEF')
        para_lines.append('#.NOREORTHO')
        para_lines.append('#.NODIRECT')
        para_lines.append('.J')
        para_lines.append(' PAMXVC 1')
        para_lines.append('.LONDON')
        para_lines.append(self.p_axis)
        para_lines.append('.2D_INT')

        for line in self.common_lines:
            integrated_para_file1.write(line + '\n')
            integrated_para_file2.write(line + '\n')

        for line in para_lines:
            integrated_para_file1.write(line + '\n')
            integrated_para_file2.write(line + '\n')

        for line in self.output1:
            integrated_para_file1.write(str(line) + '\n')

        for line in self.output2:
            integrated_para_file2.write(str(line) + '\n')

        integrated_para_file1.close()
        integrated_para_file2.close()

    def write_integrate_total(self):
        file_name1 = 'integrate_total_' + self.axis_enum[self.p_planes[0][0]] + self.axis_enum[self.p_planes[0][1]] + '.inp'
        integrated_total_file1 = open(self.output_path + os.sep + file_name1, 'w')

        file_name2 = 'integrate_total_' + self.axis_enum[self.p_planes[1][0]] + self.axis_enum[self.p_planes[1][1]] + '.inp'
        integrated_total_file2 = open( self.output_path + os.sep + file_name2, 'w')

        total_lines = []
        total_lines.append('.JDIA')
        total_lines.append(' DFCOEF')
        total_lines.append('.NOREORTHO')
        total_lines.append('.NODIRECT')
        total_lines.append('.J')
        total_lines.append(' PAMXVC 1')
        total_lines.append('.LONDON')
        total_lines.append(self.p_axis)
        total_lines.append('.2D_INT')

        for line in self.common_lines:
            integrated_total_file1.write(line + '\n')
            integrated_total_file2.write(line + '\n')

        for line in total_lines:
            integrated_total_file1.write(line + '\n')
            integrated_total_file2.write(line + '\n')

        for line in self.output1:
            integrated_total_file1.write(str(line) + '\n')

        for line in self.output2:
            integrated_total_file2.write(str(line) + '\n')

        integrated_total_file1.close()
        integrated_total_file2.close()
