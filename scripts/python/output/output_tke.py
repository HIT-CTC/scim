#!/usr/bin/python

from output import readHDF, confDict, norAll
import re                  # Regular Expression for Python
import h5py                # HDF5 for Python
import numpy as np         # Numpy
import argparse as ap
from pathlib import Path   # Pathlib --- a very useful tool for use system path

#-----------------------------------------#
#------- Sort The Name Of Variable -------#
#-----------------------------------------#
# Sort the variable in order u,v,w
# For example: vwu ----> uvw
def sortName(var):
    type = re.compile(r'[uvw][^uvw]?')
    var_out = ''
    var_list = type.findall(var)
    var_list.sort()     # Sort it to get right order of variable
    if len(var_list) == 3 and var_list[1] == var_list[2]:
        var_list.append(var_list.pop(0))
    for var in var_list:
        var_out += var
    return var_out
    
#----------------------------------------#
#- Define Turbulent Kinetic Energy Name -#
#----------------------------------------#
# This code defines the name of kinetic
# energy.
def defTKEName(varname):
    vardict = {}
    direction = {'u': 'x', 'v':'y', 'w':'z'}
    varname = sortName(varname)
    ui, uj = varname[0], varname[1]
    #-------------- Production --------------#
    i = 0
    if ui == uj:
        for dire_var, dire in direction.items():
            i += 1
            vardict['prod_{}'.format(i)] = 'm2{}d{}d{}'.format(sortName(ui+dire_var), uj, dire)
    else:
        for dire_var, dire in direction.items():
            i += 1
            vardict['prod_{}'.format(i)] = 'm{}d{}d{}'.format(sortName(ui+dire_var), uj, dire)
        for dire_var, dire in direction.items():
            i += 1
            vardict['prod_{}'.format(i)] = 'm{}d{}d{}'.format(sortName(uj+dire_var), ui, dire)
    #---------- Turbulent Transport ----------#
    i = 0
    for dire_var, dire in direction.items():
        i += 1
        vardict['turb_trans_{}'.format(i)] = 'md{}d{}'.format(ui+uj+dire_var, dire)
    #----------- Viscous Transport -----------#
    i = 0
    for dire_var, dire in direction.items():
        i += 1
        vardict['visc_trans_{}'.format(i)] = 'd2{}d{}2'.format(sortName(ui+uj), dire)
    #-- Pressure Strain&Pressure Transport --#
    if ui == uj:
        vardict['press_strain'] = '2pd{}d{}'.format(ui, direction[uj])
        vardict['press_trans'] = '2dp{}d{}'.format(ui, direction[uj])
    else:
        vardict['press_strain'] = 'p(d{}d{}+d{}d{})'.format(ui, direction[uj], uj, direction[ui])
        vardict['press_trans'] = 'dp{}d{}+dp{}d{}'.format(ui, direction[uj], uj, direction[ui])
    #---------- Viscous Dissipation ----------#
    i = 0
    for dire_var, dire in direction.items():
        i += 1
        vardict['visc_diss_{}'.format(i)] = '2d{}d{}d{}d{}'.format(ui, dire, uj, dire)
    return vardict
    
#-----------------------------------------#
#------- Output The Kinetic Energy -------#
#-----------------------------------------#
class outputTKE(object):
    def __init__(self, fp, prefix, varlist, normalize=True, blockz=None, blocky=None, blockx=None):
        self.tkedict = {
                        'uu': False,
                        'vv': False,
                        'ww': False,
                        'uv': False,
                        'uw': False,
                        'vw': False
                        }
        self.fp      = Path(fp).expanduser().resolve()
        self.prefix  = prefix
        self.varlist = varlist
        confDict(varlist, self.tkedict)
        print(self.tkedict)
        #---- Get Basic Information From File ----#
        for var_name, var_flag in self.tkedict.items():
            if var_flag:
                fn = '{}_{}.h5'.format(prefix, var_name)
                self.zc   = readHDF(self.fp/fn, 'zc'  )
                self.nu   = readHDF(self.fp/fn, 'nu'  )
                self.tau  = readHDF(self.fp/fn, 'tau' )
                self.utau = readHDF(self.fp/fn, 'utau')
                self.zplus= self.zc*self.utau/self.nu
                break
        #------------ Get Energy Dict ------------#
        nor = 1
        for var, var_flag in self.tkedict.items():
            if var_flag:
                fn = '{}_{}.h5'.format(prefix, var)
                setattr(self, '{}_dict'.format(var), defTKEName(var))
                for var_read, var_write in getattr(self, '{}_dict'.format(var)).items():
                    if normalize:
                            nor = self.nu/self.utau**4
                    setattr(self, var_write, norAll(readHDF(self.fp/fn, var_read, blockz, blocky, blockx))*nor)

    def outputData(self, varname, varlist, prefix):
        i = 0
        varlist = list(varlist)
        varlist.insert(0, 'zplus')
        varlist.insert(0, 'zc')
        filename  = '{}_{}.dat'.format(prefix, varname)
        filename = self.fp/filename
        head_str1 = ''
        head_str2 = ''
        for var_str in varlist:
            i += 1
            head_str1 += '{:^14s}'.format('C'+str(i))
            head_str2 += '{:^14s}'.format(var_str)
        title_head = '{:40s}'.format('Energy Transport Equation of {} Retau={} Rem={}'.format(varname, self.utau/self.nu, 1/self.nu))+'\n'
        head_str1 += '\n'
        head_str2 += '\n'
        spl_head = 80*'-'+'\n'
        # Write text in file
        outfile = open(filename, 'w')
        outfile.write(title_head+head_str1+head_str2+spl_head*2)
        for i in range(len(self.zc)):
            for var_str in varlist:
                var = getattr(self, var_str)[i]
                if var_str in ['rethe', 'redel', 'rex', 'retau', 'redeldi', 'redelen']:
                    outfile.write('{:14.2e}'.format(var))
                elif var_str in ['zc', 'zplus']:
                    outfile.write('{:14.4f}'.format(var))
                else:
                    outfile.write('{:14.6e}'.format(var))
            outfile.write('\n')
        print('File generated complete')
        outfile.close()

    #--------- Output All Variables ---------#
    def outputAll(self):
        tkelist = ['prod', 'turb_trans', 'visc_trans', 'press_strain', 'press_trans', 'visc_diss', 'balance']
        for varname in self.varlist:
            self.prod, self.turb_trans, self.visc_trans, self.visc_diss = np.zeros(len(self.zc)), np.zeros(len(self.zc)), np.zeros(len(self.zc)), np.zeros(len(self.zc))
            self.press_trans = np.zeros(len(self.zc))
            self.press_strain = np.zeros(len(self.zc))
            for var_read, var_write in getattr(self, '{}_dict'.format(varname)).items():
                if var_read[0:4] == 'prod':
                    self.prod += getattr(self, var_write)
                if var_read[0:4] == 'turb':
                    self.turb_trans += getattr(self, var_write)
                if var_read[0:10] == 'visc_trans':
                    self.visc_trans += getattr(self, var_write)
                if var_read[0:9] == 'visc_diss':
                    self.visc_diss += getattr(self, var_write)
                if var_read == 'press_strain':
                    self.press_strain += getattr(self, var_write)
                if var_read == 'press_trans':
                    self.press_trans += getattr(self, var_write)
            self.balance = self.prod+self.turb_trans+self.visc_trans+self.press_strain+self.press_trans-self.visc_diss
            self.outputData(varname, tkelist, 'TKE')
            self.outputData(varname, getattr(self, '{}_dict'.format(varname)).values(), 'TKE_all')

if __name__ == "__main__":
    parser = ap.ArgumentParser(prog='Output', description='Output data in a text file')
    parser.add_argument(
                        '-p', '--path',                # Option Name
                        help='Type the Path',          # Help log
                        metavar='Path',                # [-p path]
                        default='.'
                        )
    parser.add_argument(
                        '-f', '--prefix',            # Option Name
                        required='True',               # Requirement
                        help='Type the Prefix(must)',# Help log
                        metavar='Prefix'             # [-f prefix]
                        )
    parser.add_argument(
                        '-v', '--variables',
                        action='extend',               # Action of option
                        nargs='+',                     # N args
                        help='Type the Variables(must)',
                        metavar='Variables'
                        )
    parser.add_argument(
                        '-n', '--normalize',
                        action='store_false',            
                        help='Disable normalization',
                        )
    parser.add_argument(
                        '-x', '--blockx',
                        action='extend',            
                        nargs=4,                     
                        help='Select hyberslab of in x-direction(start, stride, count, block).',
                        type=int,
                        metavar='Int'
                        )
    parser.add_argument(
                        '-y', '--blocky',
                        action='extend',            
                        nargs=4,                     
                        help='Select hyberslab of in y-direction(start, stride, count, block).',
                        type=int,
                        metavar='Int'
                        )
    parser.add_argument(
                        '-z', '--blockz',
                        action='extend',            
                        nargs=4,                     
                        help='Select hyberslab of in z-direction(start, stride, count, block).',
                        type=int,
                        metavar='Int'
                        )
    args = parser.parse_args()
    outputTKE(args.path, args.prefix, args.variables).outputAll()
    #print(a.utau)
    #print(defTKEName('uv'))
