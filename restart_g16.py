import os
import glob
import subprocess

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
geometry_output = subprocess.check_output("awk 'NR>={} && NR<={} {{print}}' {}/{}".format(start+5, end-2,oldrun,foutput), shell=True)
geometry_output = filter(None, geometry_output.split('\n'))
ptable = {'X': 0, 'H': 1, 'He': 2, 'Li': 3, 'Be': 4, 'B': 5, 'C': 6, 'N': 7, 'O': 8, 'F': 9, 'Ne': 10, 'Na': 11, 'Mg': 12, 'Al': 13, 'Si': 14, 'P': 15, 'S': 16, 'Cl': 17, 'Ar': 18, 'K': 19, 'Ca': 20, 'Sc': 21, 'Ti': 22, 'V': 23, 'Cr': 24, 'Mn': 25, 'Fe': 26, 'Co': 27, 'Ni': 28, 'Cu': 29, 'Zn': 30, 'Ga': 31, 'Ge': 32, 'As': 33, 'Se': 34, 'Br': 35, 'Kr': 36, 'Rb': 37, 'Sr': 38, 'Y': 39, 'Zr': 40, 'Nb': 41, 'Mo': 42, 'Tc': 43, 'Ru': 44, 'Rh': 45, 'Pd': 46, 'Ag': 47, 'Cd': 48, 'In': 49, 'Sn': 50, 'Sb': 51, 'Te': 52, 'I': 53, 'Xe': 54, 'Cs': 55, 'Ba': 56, 'La': 57, 'Ce': 58, 'Pr': 59, 'Nd': 60, 'Pm': 61, 'Sm': 62, 'Eu': 63, 'Gd': 64, 'Tb': 65, 'Dy': 66, 'Ho': 67, 'Er': 68, 'Tm': 69, 'Yb': 70, 'Lu': 71, 'Hf': 72, 'Ta': 73, 'W': 74, 'Re': 75, 'Os': 76, 'Ir': 77, 'Pt': 78, 'Au': 79, 'Hg': 80, 'Tl': 81, 'Pb': 82, 'Bi': 83, 'Po': 84, 'At': 85, 'Rn': 86, 'Fr': 87, 'Ra': 88, 'Ac': 89, 'Th': 90, 'Pa': 91, 'U': 92, 'Np': 93, 'Pu': 94, 'Am': 95, 'Cm': 96, 'Bk': 97, 'Cf': 98, 'Es': 99, 'Fm': 100, 'Md': 101, 'No': 102, 'Lr': 103, 'Rf': 104, 'Db': 105, 'Sg': 106, 'Bh': 107, 'Hs': 108, 'Mt': 109, 'Ds': 110, 'Rg': 111, 'Cn': 112, 'Nh': 113, 'Fl': 114, 'Mc': 115, 'Lv': 116, 'Ts': 117, 'Og': 118}

fcoords = []
for line in geometry_output:
    data = line.split()
    fcoords.append([data[-3], data[-2], data[-1]])

def iscoord(line):
    if len(line) == 4 or len(line) == 5:
        if isfloat(line[1]) and isfloat(line[2]) and isfloat(line[3]):
            return True
        else:
            return False
    else:
        return False

def isfloat(value):
    try:
        float(value)
    except ValueError:
        return False
    return True

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

