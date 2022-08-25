import os
import subprocess
import sys

""" Objectives: Create Gaussian 16 input geometries (without using Gaussview)"""
# Output file name
option = int(sys.argv[1])
if option != 5:
    g16_input = sys.argv[2]

# Options:
# 1: Create output movie from Gaussian 16 output
# 2: Create the geometry of the last step from Gaussian 16 output
# 3: Freeze specific atom index
# 4: Add fragment labels
# 5: Create input restart files using the geometry from last step of Gaussian 16 output with the same constraints
# Atomic numbers
ptable = {'X': 0, 'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40, 'Nb': 41, 'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50, 'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60, 'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70, 'Lu': 71, 'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80, 'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85, 'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90, 'Pa': 91, 'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100, 'Md': 101, 'No': 102, 'Lr': 103, 'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109, 'Ds': 110, 'Rg': 111, 'Cn': 112, 'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117, 'Og': 118}

def isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False
def istint(value):
    try:
        int(value)
        return True
    except ValueError:
        return False

def iscoord(line):
    if len(line) >= 4:
        if False not in map(isfloat, line[-3:]) and isfloat(line[0]) == False:
            return True
        else:
            return False
    else:
        return False

if option == 1:
    # Get output geometry from awk 
    start = int(subprocess.check_output("awk '/Input/{{print NR}}' {} | tail -1".format(g16_input), shell=True).decode('ascii'))
    #start = subprocess.check_output("awk '/Input/{{print NR}}' {} | tail -1".format(g16_input), shell=True).decode('ascii')
    end = int(subprocess.check_output("awk '/Rotational/{{print NR}}' {} | tail -1".format(g16_input), shell=True).decode('ascii'))
    geometry_output = subprocess.check_output("awk 'NR>={} && NR<={} {{print}}' {}".format(start+5, end-2,g16_input), shell=True).decode('ascii')

    geometry_output = filter(None, geometry_output.split('\n'))
    output = []
    for line in geometry_output:
        data = line.split()
        atomic_number = int(data[1])
        element = list(ptable.keys())[list(ptable.values()).index(atomic_number)]
        output.append([element, data[-3], data[-2], data[-1]])

    f = open('output.xyz', 'w')
    f.write('{}\n'.format(len(output)))
    f.write('\n')
    for line in output:
        f.write(' '.join(line) + '\n')
        print(' '.join(line))
    f.close()

if option == 2:
    start = subprocess.check_output("awk '/Input/{{print NR}}' {}".format(g16_input), shell=True).decode('ascii')
    end = subprocess.check_output("awk '/Rotational/{{print NR}}' {}".format(g16_input), shell=True).decode('ascii')
    starts = filter(None, str(start).split('\n'))
    ends = filter(None, str(end).split('\n'))

    starts = [int(i) for i in starts]
    ends = [int(i) for i in ends]

    for start, end in zip(starts, ends):
        geometry_output = subprocess.check_output("awk 'NR>={} && NR<={} {{print}}' {}".format(start+5, end-2, g16_input), shell=True).decode('ascii')
        geometry_output = filter(None, geometry_output.split('\n'))
        output = []
        for line in geometry_output:
            data = line.split()
            atomic_number = int(data[1])
            element = list(ptable.keys())[list(ptable.values()).index(atomic_number)]
            output.append([element, data[-3], data[-2], data[-1]])


        f = open('output_movies.xyz', 'a')
        f.write('{}\n'.format(len(output)))
        f.write('\n')
        for line in output:
            f.write(' '.join(line) + '\n')
            print(' '.join(line))
        f.close()

# Atom indices from ase gui (atom index counts from 0)
if option == 3:
    data = []
    with open(g16_input, "r") as f:
        for line in f:
            l = line.split()
            if iscoord(l):
                data.append(l)

    freeze_indice = [21, 32, 65, 78, 83, 15, 17, 25, 30, 85, 62, 69, 76]

    for index, atom in enumerate(data):
        if index in freeze_indice:
            atom.insert(1, -1)
        else:
            atom.insert(1, 0)

    with open('output_fix_atom.xyz', 'w') as f:
        for m in data:
            for item in m:
                f.write(str(item) + ' ')
            f.write("\n")

if option == 4:
    data = []
    with open(g16_input, "r") as f:
        for line in f:
            l = line.split() 
            if iscoord(l):
                data.append(l)

    fragment_indice = {1: list(range(0,102)), 2: [102]}
    for item in fragment_indice:
        for k in fragment_indice[item]:
            data[k][0] = data[k][0] + '(Fragment={})'.format(item)

    with open('output_with_fragment.xyz', 'w') as f:
        for m in data:
            for item in m:
                f.write(item + ' ')
            f.write("\n")

if option == 5:
    import glob
    foutput = 'test.out'
    finput = 'test.gjf'

    rep = len(glob.glob("run*/"))
    oldrun = 'run' + str(rep)
    subprocess.call("mkdir {}".format(oldrun), shell=True)
    subprocess.call("cp {} {}".format(foutput, oldrun), shell=True)
    subprocess.call("cp {} {}".format(finput, oldrun), shell=True)

    # Get output geometry from awk 
    start = int(subprocess.check_output("awk '/Input/{{print NR}}' {}/{} | tail -1".format(oldrun,foutput), shell=True).decode('ascii'))
    end = int(subprocess.check_output("awk '/Rotational/{{print NR}}' {}/{} | tail -1".format(oldrun,foutput), shell=True).decode('ascii'))
    geometry_output = subprocess.check_output("awk 'NR>={} && NR<={} {{print}}' {}/{}".format(start+5, end-2,oldrun,foutput), shell=True).decode('ascii')
    print(geometry_output)
    geometry_output = filter(None, geometry_output.split('\n'))
    fcoords = []
    for line in geometry_output:
        lined = line.split()
        fcoords.append([lined[-3], lined[-2], lined[-1]])
    data = []
    with open(finput, 'r') as f:
        lines = f.readlines()
        for line in lines:
            data.append(line)

    
    coord_i = 0
    for index, line in enumerate(data):
        line = line.split()
        if iscoord(line):
            newline = line[0] + ' ' + line[1] + ' ' + fcoords[coord_i][0] + ' ' + fcoords[coord_i][1] +' ' + fcoords[coord_i][2] + '\n'
            data[index] = newline
            coord_i = coord_i +1

    with open(finput, 'w') as f:
        for line in data:
            f.write(line)

