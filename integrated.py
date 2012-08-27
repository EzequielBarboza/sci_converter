#!/usr/bin/env python

def write_integrated_dia(scf_file, mol_file):
    lines = []
    lines.append('**DIRAC')
    lines.append('#.WAVE FUNCTION')
    lines.append('**HAMILTONIAN')
    lines.append('#.LVCORR')
    lines.append('#.URKBAL')
    lines.append('.LEVY-LEBLOND')
    lines.append('**INTEGRALS')
    lines.append('*READIN')
    lines.append('.UNCONTRACT')
    lines.append('**WAVE FUNCTION')
    lines.append('.SCF')
    lines.append('**VISUAL')
    lines.append('.JDIA')
    lines.append(' DFCOEF')
    lines.append('.NOREORTHO')
    lines.append('.NODIRECT')
    lines.append('#.J')
    lines.append('# PAMXVC 1')
    lines.append('.LONDON')

    #retrieve the perpendicular plane in a molecule (the plane where most atoms are closer to zero)
    p_plane = get_p_plane(mol_file)
    axis = 'X' if p_plane == 'BXLAO' else 'Y' if p_plane == 'BYLAO' else 'Z'
    lines.append(axis)
#static data
    XZ = [0,2]
    YZ = [1,2]
    XY = [0,1]
    line1 = [0.0, 0.0, 0.0]
    line2 = [0.0, 0.0, 0.0]
    line3 = [0.0, 0.0, 0.0]

#now, calculating
    planes = [YZ, XZ] if p_plane == 'BZLAO' else [XZ, XY] if p_plane == 'BXLAO' else [YZ, XY]
#planes discovered, lets assemble 2 possible outputs
    output1 = []
    indexForLine2 = planes[0][0]#this is the value of the first axis
    indexForLine3 = planes[0][1]#this is the value of the second axis
    line2[indexForLine2] = 10.0
    line3[indexForLine3] = 10.0

    output1.append(line1)
    output1.append(line2)
    output1.append(10)
    output1.append(line3)
    output1.append(10)
    output1.append(10)
    output1.append('*END OF')

#reset everything
    line2 = [0.0, 0.0, 0.0]
    line3 = [0.0, 0.0, 0.0]
    output2 = []
    indexForLine2 = planes[1][0]#this is the value of the first axis
    indexForLine3 = planes[1][1]#this is the value of the second axis
    line2[indexForLine2] = 10.0
    line3[indexForLine3] = 10.0

    output2.append(line1)
    output2.append(line2)
    output2.append(10)
    output2.append(line3)
    output2.append(10)
    output2.append(10)
    output2.append('*END OF')

    file_name1 = "XY" if axis == 'Z' else 'XZ' if axis == 'X' else 'YZ'
    file_name1 = "integrate_dia".join(file_name1).join('.inp')
    integrated_dia_file1 = open(''.join([output_path, os.sep, file_name1]), 'w')

    file_name2 = "XY" if axis == 'Z' else 'XZ' if axis == 'X' else 'YZ'
    file_name2 = "integrate_dia".join(file_name2).join('.inp')
    integrated_dia_file2 = open(''.join([output_path, os.sep, file_name2]), 'w')

    for line in lines:
        integrated_dia_file1.write(line)
        integrated_dia_file2.write(line)

    for line in output1:
        integrated_dia_file1.write(line)

    for line in output2:
        integrated_dia_file2.write(line)

    integrated_dia_file1.close()
    integrated_dia_file2.close()

def write_integrated_dia(scf_file, mol_file):
    lines = []
    lines.append('**DIRAC')
    lines.append('#.WAVE FUNCTION')
    lines.append('**HAMILTONIAN')
    lines.append('#.LVCORR')
    lines.append('#.URKBAL')
    lines.append('.LEVY-LEBLOND')
    lines.append('**INTEGRALS')
    lines.append('*READIN')
    lines.append('.UNCONTRACT')
    lines.append('**WAVE FUNCTION')
    lines.append('.SCF')
    lines.append('**VISUAL')
    lines.append('.JDIA')
    lines.append(' DFCOEF')
    lines.append('.NOREORTHO')
    lines.append('.NODIRECT')
    lines.append('#.J')
    lines.append('# PAMXVC 1')
    lines.append('.LONDON')

    #retrieve the perpendicular plane in a molecule (the plane where most atoms are closer to zero)
    p_plane = get_p_plane(mol_file)
    axis = 'X' if p_plane == 'BXLAO' else 'Y' if p_plane == 'BYLAO' else 'Z'
    lines.append(axis)
#static data
    XZ = [0,2]
    YZ = [1,2]
    XY = [0,1]
    line1 = [0.0, 0.0, 0.0]
    line2 = [0.0, 0.0, 0.0]
    line3 = [0.0, 0.0, 0.0]

#now, calculating
    planes = [YZ, XZ] if p_plane == 'BZLAO' else [XZ, XY] if p_plane == 'BXLAO' else [YZ, XY]
#planes discovered, lets assemble 2 possible outputs
    output1 = []
    indexForLine2 = planes[0][0]#this is the value of the first axis
    indexForLine3 = planes[0][1]#this is the value of the second axis
    line2[indexForLine2] = 10.0
    line3[indexForLine3] = 10.0

    output1.append(line1)
    output1.append(line2)
    output1.append(10)
    output1.append(line3)
    output1.append(10)
    output1.append(10)
    output1.append('*END OF')

#reset everything
    line2 = [0.0, 0.0, 0.0]
    line3 = [0.0, 0.0, 0.0]
    output2 = []
    indexForLine2 = planes[1][0]#this is the value of the first axis
    indexForLine3 = planes[1][1]#this is the value of the second axis
    line2[indexForLine2] = 10.0
    line3[indexForLine3] = 10.0

    output2.append(line1)
    output2.append(line2)
    output2.append(10)
    output2.append(line3)
    output2.append(10)
    output2.append(10)
    output2.append('*END OF')

    file_name1 = "XY" if axis == 'Z' else 'XZ' if axis == 'X' else 'YZ'
    file_name1 = "integrate_dia".join(file_name1).join('.inp')
    integrated_dia_file1 = open(''.join([output_path, os.sep, file_name1]), 'w')

    file_name2 = "XY" if axis == 'Z' else 'XZ' if axis == 'X' else 'YZ'
    file_name2 = "integrate_dia".join(file_name2).join('.inp')
    integrated_dia_file2 = open(''.join([output_path, os.sep, file_name2]), 'w')

    for line in lines:
        integrated_dia_file1.write(line)
        integrated_dia_file2.write(line)

    for line in output1:
        integrated_dia_file1.write(line)

    for line in output2:
        integrated_dia_file2.write(line)

    integrated_dia_file1.close()
    integrated_dia_file2.close()



#   planes = ['XY', 'XZ', 'YZ']
#    j_dia_file.write('**DIRAC')
#    j_dia_file.write('#.WAVE FUNCTION')
#    j_dia_file.write('**HAMILTONIAN')
#    j_dia_file.write('#.LVCORR')
#    j_dia_file.write('#.URKBAL')
#    j_dia_file.write('.LEVY-LEBLOND')
#    j_dia_file.write('**INTEGRALS')
#    j_dia_file.write('*READIN')
#    j_dia_file.write('.UNCONTRACT')
#    j_dia_file.write('**WAVE FUNCTION')
#    j_dia_file.write('.SCF')
#    j_dia_file.write('**VISUAL')
#    j_dia_file.write('.JDIA')
#    j_dia_file.write(' DFCOEF')
#    j_dia_file.write('.NOREORTHO')
#    j_dia_file.write('.NODIRECT')
#    j_dia_file.write('#.J')
#    j_dia_file.write('# PAMXVC 1')
#    j_dia_file.write('.LONDON')
