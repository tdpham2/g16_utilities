import os
import subprocess

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

def gjf_reader(finput="test.gjf", only_coords=False):
    data = []
    with open(finput, "r") as f:
        for line in f:
            data.append(line)
    if only_coords == False:
        return data
    else:
        coords_data = []
        for line in data:
            line = line.split()
            if iscoord(line):
                coords_data.append(line)
        return coords_data

def out_reader(foutput="test.out"):
    return True

# Get final geometry. If "freq" is in route, then the position is slightly different
def get_final_geometry(finput="test.gjf",foutput="test.out", writexyz=True, fileout="final_optimized.xyz"):
    data = gjf_reader(finput=finput)
    route = data[3].strip().split()
    if "freq" in route:
        # Where to find the geometry
        npos = 2
    else:
        npos = 1

    start = int(subprocess.check_output("awk '/Input/{{print NR}}' {} | tail -1".format(foutput), shell=True).decode('ascii'))
    end = int(subprocess.check_output("awk '/Rotational constant/{{print NR}}' {} | tail -{}| head -1".format(foutput, npos), shell=True).decode('ascii'))
    geometry_output = subprocess.check_output("awk 'NR>={} && NR<={} {{print}}' {}".format(start+5, end-2,foutput), shell=True).decode('ascii')

    geometry_output = filter(None, geometry_output.split('\n'))
    output = []
    for line in geometry_output:
        data = line.split()
        atomic_number = int(data[1])
        element = list(ptable.keys())[list(ptable.values()).index(atomic_number)]
        output.append([element, data[-3], data[-2], data[-1]])

    if writexyz==True:
        f = open(fileout, 'w')
        f.write('{}\n'.format(len(output)))
        f.write('\n')
        for line in output:
            f.write(' '.join(line) + '\n')
            print(' '.join(line))
        f.close()

    return output

#Continue calculation from previously calculation 
def continue_calculation(finput="test.gjf",foutput="test.out", fileout="new.gjf", counterpoise=False):
    final_geo = get_final_geometry(finput=finput, foutput=foutput, writexyz=False)
    initial_geo = gjf_reader(finput=finput, only_coords=True)
    merged_geo = []
    for i, j in zip(initial_geo, final_geo):
        merged_geo.append([i[0], i[1], j[1], j[2], j[3], '\n'])
    # Keep all input section from orginal file
    inputf = gjf_reader(finput=finput)
    
    coord_counter = 0
    for index, line in enumerate(inputf):
        line=line.strip().split()
        if iscoord(line):
            inputf[index] = ' '.join(merged_geo[coord_counter])
            coord_counter = coord_counter + 1
    with open(fileout, "w") as f:
        for line in inputf:
            f.write(line)
    if counterpoise == True:
        subprocess.call("sed -i 's/opt freq/sp counterpoise=2/' {}".format(fileout), shell=True)

# Fragment indice: {fragment_number: list of atoms}
fragment_indice = {1: list(range(0,102))}

def add_fragment(fragment_indice,finput="test.gjf", fileout="new.gjf"):
    coords = gjf_reader(finput=finput,only_coords=True)

    for fragment in fragment_indice:
        for k in fragment_indice[fragment]:
            coords[k][0] = coords[k][0] + '(Fragment={})'.format(fragment)
    with open("temp.xyz", 'w') as f:
        for item in coords:
            f.write(" ".join(item) + "\n")
#continue_calculation()
add_fragment(fragment_indice)
