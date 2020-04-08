#!/usr/bin/python3.7
#program to convert xyz file formal to Dl_Poly conf format                         ##
import platform
import sys                                                                         #

print("System Information : ",sys.version, sys.platform)                           ##
print("Build Info : ",platform.machine(),platform.system())                        ##
print()                                                                            ##
print()                                                                            ##
                                                                                   ##
import os                                                                          ##
cwd = os.getcwd()  # Get the current working directory (cwd)                       ##
files = os.listdir(cwd)  # Get all the files in that directory                     ##
print("Available Files in directory %r : " % (cwd))                                ##
print()                                                                            ##
for counter, file_items in enumerate(files,1):                                     ##
    print(counter,"--" ,file_items)                                                ##
                                                                                   ##
print("--------------------------------------------------------------------------")##
                                                                                   ##
print()                                                                            ##
print()                                                                            ##
                                                                                   ##
#####################################################################################

print("This program converts the .xyz file format created 'from ADF' \n to LAMMPS Structure file.")
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



####################################################

### opening file format to write into CONF format#######

fw = open("structure.dat",'wt')

fw.write('LAMMPS data file created by Raghvender using ADF processed .xyz format \n')

print()


Shell_model = input("Do you want to split your atom into core-shell "
                    "\n 0 -- No"
                    "\n 1 -- Yes"
                    "\n => ")

################################################################################

## to double number of atoms incase of core-shell model

total_atom_name = Atom_name[:]
total_atom_x = Atom_x[:]
total_atom_y = Atom_y[:]
total_atom_z = Atom_z[:]



count_name = 0

if int(Shell_model) == 1:
    number_of_atom = 2 * number_of_atom
    total_atom_name.clear()
    total_atom_x.clear()
    total_atom_y.clear()
    total_atom_z.clear()
    for id in range(len(Atom_name)):
        total_atom_name.append(Atom_name[id])
        total_atom_x.append(Atom_x[id])
        total_atom_y.append(Atom_y[id])
        total_atom_z.append(Atom_z[id])
        #print(Atom_name[id])
        total_atom_name.append(Atom_name[id]+'_sh')
        total_atom_x.append(Atom_x[id])
        total_atom_y.append(Atom_y[id])
        total_atom_z.append(Atom_z[id])
        #print(Atom_name[id]+'_sh')


Atom_type = list(dict.fromkeys(total_atom_name)) ## types of atom including core shell types
fo.close()



fw.write(" % 3i  atoms \n" % (number_of_atom))
fw.write(" % 3i  atom types \n" % (len(Atom_type)))
#####################################################################3333##
#writing simulation box sizes in CONF FILE


fw.write(" % 5.5f  %7.5f  xlo  xhi \n" % (0,VECTOR[0][0]))
fw.write(" % 5.5f  %7.5f  ylo  yhi \n" % (0,VECTOR[1][1]))
fw.write(" % 5.5f  %7.5f  zlo  zhi \n" % (0,VECTOR[2][2]))

###########################################################################3

fw.write("\n")
fw.write("Masses \n ")
fw.write("\n")


#############################
#asking for atomic masses

atom_mass = []
Atomic_charge = []

print(Atom_type)
print()




for il, value in enumerate(Atom_type):
    Atomic_mass = input("Enter atomic mass (u) of {} atom : ".format(Atom_type[il]))
    charge = float(input("Enter atomic charge of {} atom : ".format(Atom_type[il])))
    Atomic_charge.append(charge)
    #    print(" %3i   %3.3f    # %3s     " %( il +1 , float(Atomic_mass) , Atom_type[il])  )
    fw.write(" %3i   %3.3f    # %3s   \n" %( il + 1   , float(Atomic_mass) , Atom_type[il])  )



fw.write("\n")
fw.write(" Atoms  # Charge " )
fw.write("\n")

#################

for item,value in enumerate(total_atom_name):
    t1 = Atom_type.index(value)
    t2 = Atomic_charge[t1]
    fw.write(" %7i  %3i %3.8f %3.6f  %3.6f %3.6f       #"
             " %5s  \n" % ( item + 1 ,  1 + t1, t2,total_atom_x[item],total_atom_y[item],total_atom_z[item],total_atom_name[item] ) )

###########################################33
fw.close()
print()
print("File with the name of (",fw.name,") has been successfully created in current directory.")











