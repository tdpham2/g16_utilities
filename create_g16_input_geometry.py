import os
import subprocess
import sys

""" Objectives: Create Gaussian 16 input geometries (without using Gaussview)"""
# Output file name
g16_input = sys.argv[1]
#options = ["output_xyz", "output_movie", "freeze_atoms"]

option = "output_xyz"
# Atomic numbers
ptable = {'X': 0, 'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40, 'Nb': 41, 'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50, 'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60, 'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70, 'Lu': 71, 'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80, 'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85, 'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90, 'Pa': 91, 'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100, 'Md': 101, 'No': 102, 'Lr': 103, 'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109, 'Ds': 110, 'Rg': 111, 'Cn': 112, 'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117, 'Og': 118}

if option == "output_xyz":
    # Get output geometry from awk 
    start = int(subprocess.check_output("awk '/Standard/{{print NR}}' {} | tail -1".format(g16_output), shell=True).decode('ascii'))
    end = int(subprocess.check_output("awk '/Rotational/{{print NR}}' {} | tail -1".format(g16_output), shell=True).decode('ascii'))
    geometry_output = subprocess.check_output("awk 'NR>={} && NR<={} {{print}}' test.out".format(start+5, end-2), shell=True).decode('ascii')


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

if options == "output_movie":
    start = subprocess.check_output("awk '/Input/{{print NR}}' {}".format(g16_input), shell=True)
    end = subprocess.check_output("awk '/Rotational/{{print NR}}' {}".format(g16_input), shell=True)

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

if options == "freeze_atoms":
    def isfloat(value):
        try:
            float(value)
            return True
        except ValueError:
            return False

    def iscoord(line):
        if len(line) >= 4:
            if False not in map(isfloat, line[1:4]):
                return True
            else:
                return False
        else:
            return False
    xyz_file = []

    with open(g16_input, "r") as f:
        for line in f:
            line = line.strip().split()
            if iscoord(line):
                xyz_file.append(line)


    freeze_indice = [21, 32, 65, 78, 83, 15, 17]

    for index, atom in enumerate(xyz_file):
        if index in freeze_indice:
            atom.insert(1, -1)
        else:
            atom.insert(1, 0)

    with open('output_fix_atom.xyz', 'w') as f:
        for atom in xyz_file:
            f.write('{} {} {} {} {}\n'.format(atom[0], atom[1], atom[2], atom[3], atom[4]))
        

    
       
