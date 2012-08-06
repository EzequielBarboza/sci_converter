import os

def write_london(london_file, scf_file, mol_file):
    #teste = open("teste")
    #teste.open()
    #teste.w
    for line in scf_file.readlines():
        trimmed = line.strip();
        if not trimmed == '*END OF':
            london_file.write(trimmed.join(os.linesep))
        else :
            london_file.write('**PROPERTIES'.join(os.linesep))
            plane = which_plane(mol_file)
            london_file.write(plane.join(os.linesep))
            london_file.write('*NMR'.join(os.linesep))
            london_file.write('.LONDON'.join(os.linesep))
            london_file.write('.DOEPRN'.join(os.linesep))
            london_file.write('.INTFLG'.join(os.linesep))
            symmetry = '0 1 1' if plane == 'BXLAO' else '1 0 1' if plane == 'BYLAO' else '1 1 0'
            london_file.write(symmetry.join(os.linesep))
            london_file.write('*END OF'.join(os.linesep))

def which_plane(mol_file):
    totalizator = [0,0,0]
    index_ = 0
    for line in mol_file.readlines() :
        if len(line.split()) >= 4 :
            x = abs(float(line.split()[1])) if is_number(line.split()[1])else ""
            y = abs(float(line.split()[2])) if is_number(line.split()[2])else ""
            z = abs(float(line.split()[3])) if is_number(line.split()[3])else ""
            index_ = 0 if x < y and x < z else 1 if y < z and y < x else 2
            totalizator[index_] += 1
    if totalizator[0] > totalizator[1] :
        if totalizator[0] > totalizator[2] :
            return 'BXLAO'
        else :
            return 'BZLAO'
    elif totalizator[1] > totalizator[2]:
        return 'BYLAO'
    else :
        return 'BZLAO'

def is_number(s):
    try:
        float(s) # for int, long and float
    except ValueError:
        try:
            complex(s) # for complex
        except ValueError:
            return False
    return True
