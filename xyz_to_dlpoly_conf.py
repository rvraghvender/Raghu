#!/usr/bin/python3.7
#program to convert xyz file formal to Dl_Poly conf format
import platform
import sys

print("System Information : ",sys.version, sys.platform)
print("Build Info : ",platform.machine(),platform.system())
print()
print()

import os
cwd = os.getcwd()  # Get the current working directory (cwd)
files = os.listdir(cwd)  # Get all the files in that directory
print("Available Files in directory %r : " % (cwd))
print()
for counter, file_items in enumerate(files,1):
    print(counter,"--" ,file_items)

print("--------------------------------------------------------------------------")

print()
print()

###############################################################################

print("This program converts the .xyz file format created 'from ADF' \n to Dl_Poly Conf. Structure.")
print()



#### opening file .xyz format #####

fo = open(input("Enter the name of the xyz file to convert : "),'r')


Atom_name = [] ###defininig list for atomic name and coordinates
Atom_x = []    ### that will be appended later.
Atom_y = []
Atom_z = []

Lattice_VECTORS = [] #for orthorhombic like structures
VECTOR =  [[],[],[]]  # for monoclinic like structures

count = 1


while True:
    line = fo.readline().split()
    if len(line) == 0 : break  ## to stop coding after reaching end
    if len(line) == 1:  ## to read line (First line generally)
        number_of_atom = int(line[0])
        continue
    if len(line) != 4: continue  ## because i beleive 4 elements are for
    na, x, y, z = [a for a in line[:4]]  # atoms and their coordinates
    if na[0:3] == 'VEC':              ## This section is to read
        VECTOR[count-1].append(float(x))
        VECTOR[count-1].append(float(y))
        VECTOR[count-1].append(float(z))
        Lattice_VECTORS.append(line[count]) ## lattice vectors for orthorhombic like structure
        count += 1   ## this method will read diagonal terms of matrix
    else:
        Atom_name.append(na)
        Atom_x.append(float(x))
        Atom_y.append(float(y))
        Atom_z.append(float(z))

print()

Atom_type = list(dict.fromkeys(Atom_name)) ## types of atom
fo.close()

####################################################

### opening file format to write into CONF format#######

fw = open("CONFIG",'wt')

fw.write('CONFIG file created by Raghvender using ADF processed .xyz format ')



print()
config_key = input("Enter the value of config key (integer value) : "
                   "\n 0  -- Include coordinates in the file "
                   "\n 1  -- Include coordinates and velocities in the file"
                   "\n 2  -- Include coordinates, velocities and forces in the file"
                   "\n => ")   ## see manual

print()

periodic_boundary_condition = input("Enter the value of Periodic Boundary Condition (integer value) : "
                   "\n 0  -- No periodic boundary condition "
                   "\n 1  -- Cubic boundary condition"
                   "\n 2  -- Orthorhombic boundary condition"
                   "\n 3  -- Parallelepiped boundary condition "
                   "\n 4  -- x-y parellelogram boundary condition with no periodicity in z-direction"
                   "\n => ")   ## see manual

################################################################################
print()

Shell_model = input("Do you want to split your atom into core-shell "
                    "\n 0 -- No"
                    "\n 1 -- Yes"
                    "\n => ")

################################################################################

## to double number of atoms incase of core-shell model


if int(Shell_model) == 1:
    number_of_atom = 2 * number_of_atom

fw.write(" \n  % 3i % 5i %6i" % (int(config_key),int(periodic_boundary_condition),number_of_atom))

#####################################################################3333##
#writing simulation box sizes in CONF FILE

for i in range(3):
    fw.write(" \n % 5.5f  %7.5f  %7.5f  " % (VECTOR[i][0],VECTOR[i][1],VECTOR[i][2]))

###########################################################################3



### fow writing atomic coordinates

atom_count = 1

for iz in range(len(Atom_name)):
    fw.write(" \n %1s %10i " % (Atom_name[iz], atom_count))
    fw.write(" \n %9.5f  %3.5f  %3.5f " % (Atom_x[iz],Atom_y[iz],Atom_z[iz]))
    atom_count = atom_count + 1
    if int(config_key) != 0:
        fw.write(" \n %9.5f  %3.5f  %3.5f " % (0,0,0)) ######## writing the velocities
        if int(config_key) == 2:
            fw.write(" \n %9.5f  %3.5f  %3.5f  " % (0,0,0))  ### writing the forces

    #### for writing shell atoms
    if int(Shell_model) == 1:
        fw.write(" \n %1s_sh %10i " % (Atom_name[iz], atom_count))
        fw.write(" \n %9.5f  %3.5f  %3.5f  " % (Atom_x[iz],Atom_y[iz],Atom_z[iz]))
        if int(config_key) != 0:
            fw.write(" \n %9.5f  %3.5f  %3.5f  " % (0,0,0))  ### writing the velocities
            if int(config_key) == 2:
                fw.write(" \n %9.5f  %3.5f  %3.5f  " % (0,0,0)) ### writing the forces

    atom_count = atom_count + 1 

###########################################33
fw.close()
print()
print("File with the name of (",fw.name,") has been successfully created in current directory.")











