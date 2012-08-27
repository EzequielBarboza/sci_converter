from mol import get_p_plane, get_biggest_coordinate

def write_j_dia_london(j_dia_london_file, scf_file, mol_file):
    #this guys are the core of the file
    j_dia_london_file.write('**DIRAC\n')
    j_dia_london_file.write('#.WAVE FUNCTION\n')
    j_dia_london_file.write('**HAMILTONIAN\n')
    j_dia_london_file.write('.LEVY-LEBLOND\n')
    j_dia_london_file.write('**INTEGRALS\n')
    j_dia_london_file.write('*READIN\n')
    j_dia_london_file.write('.UNCONTRACT\n')
    j_dia_london_file.write('**WAVE FUNCTION\n')
    j_dia_london_file.write('.SCF\n')
    j_dia_london_file.write('**VISUAL\n')
    j_dia_london_file.write('.JDIA\n')
    j_dia_london_file.write('DFCOEF\n')
    j_dia_london_file.write('.NOREORTHO\n')
    j_dia_london_file.write('.NODIRECT\n')
    j_dia_london_file.write('#.J\n')
    j_dia_london_file.write('# PAMXVC 1\n')
    j_dia_london_file.write('.LONDON\n')

    #retrieve the perpendicular plane in a molecule (the plane where most atoms are closer to zero)
    p_plane = get_p_plane(mol_file)
    axis = 'X' if p_plane == 'BXLAO' else 'Y' if p_plane == 'BYLAO' else 'Z'
    j_dia_london_file.write(axis.join('\n'))

    j_dia_london_file.write('.2D')

    biggest_ = get_biggest_coordinate(mol_file)
    fst_point = ['-'.join(biggest_), '-'.join(biggest_), '\n']
    snd_point = ['+'.join(biggest_), '-'.join(biggest_), '\n']
    trd_point = ['-'.join(biggest_), '+'.join(biggest_), '\n']
    index = 0 if axis == 'X' else 1 if axis == 'Y' else 2
    fst_point.insert(1.0, index)
    snd_point.insert(1.0, index)
    trd_point.insert(1.0, index)
#    all_points = [fst_point, snd_point, trd_point]
#    for point in all_points:
#        if index == 0:
#            temp = '1.0 '.join(string.join(point, " ")).join('\n')
#        elif index == 1:
#            temp = point[0].join(' ').join('1.0 ').join(point[1].join('\n'))
#        else :
#            temp = string.join(point, " ").join('1.0\n')
#        j_dia_london_file.write(temp)
#first_point = '-'.join(biggest_).join(' ').join('-').join(biggest_).join('\n')
#second_point = '+'.join(biggest_).join(' ').join('-').join(biggest_).join('\n')
#third_point = '-'.join(biggest_).join(' ').join('+').join(biggest_).join('\n')
    j_dia_london_file.write(string.join(fst_point, " "))
    j_dia_london_file.write(string.join(snd_point, " "))
    j_dia_london_file.write('200'.join('\n'))
    j_dia_london_file.write(string.join(trd_point, " "))
    j_dia_london_file.write('200'.join('\n'))

    j_dia_london_file.write('*END OF')