#!/home/yh/anaconda3/bin/python

import h5py
import numpy as np
import argparse as ap

class readHDF(object):
    def __init__(self, filename):
        self.filename = filename
        
    def readInfo(self, var):
        f = h5py.File(self.filename, 'r')
        for svar in var:
            print('Variables name is {}'.format(svar))
            print('Type is', f[svar].dtype)
            if f[svar].shape != (1, ):
                print('The shape of the variables is ', f[svar].shape)
            else:
                print('The number of the variable is', f[svar][0])
            print('----------------------------')

    def printAll(self):
        f = h5py.File(self.filename, 'r')
        dict={}
        for key in f.keys():
            if str(f[key].dtype) in dict.keys():
                if str(f[key].shape) in dict[str(f[key].dtype)]: 
                    dict[str(f[key].dtype)][str(f[key].shape)][str(key)]=f[key][0]
                else:
                    dict[str(f[key].dtype)][str(f[key].shape)] = {str(key):f[key][0]}
            else:
                dict[str(f[key].dtype)] = {str(f[key].shape):{str(key):f[key][0]}}
        for i in dict:
            print('')
            print('===================')
            print(i)
            for j in dict[i]:
                print('')
                #print('--------------------')
                print('  '+str(j)+': ')
                counter = 0
                for k in dict[i][j]:
                    if counter == 8:
                        print('    '+str(k).ljust(4))
                        counter = 0
                    else:
                        print('    '+str(k).ljust(4),end=" ")
                        counter += 1
                
               # print('\n-------------------')
    def printallinfo(self):
        f = h5py.File(self.filename, 'r')
        var = f.keys()
        self.readInfo(var)
 
#HDF5的读取：
# f = h5py.File('avg_recy.h5','r')   #打开h5文件
# 可以查看特定的变量
# varName = input('please input varName:')
# if(f.get(varName) is None):
#     print('There is no ' + varName)
# else:
#     print(type(f[varName]))
#     print(len(f[varName]))
#     print(f[varName].shape)
# 可以查看所有的变量
#for key in f.keys():
#     print(f[key].name)
#     print(f[key].shape)

if __name__ == '__main__':
    parser = ap.ArgumentParser(prog='HDFView', description='Generate a xdmf file to view HDF file.')
    parser.add_argument(
                        '-f', '--filename',            # Option Name
                        required='True',               # Requirement
                        help='Type the Filename(must)',# Help log
                        metavar='Filename'             # [-f filename]
                        )
    parser.add_argument(
                        '-v', '--variables',
                        action='extend',               # Action of option
                        nargs='*',                     # N args
                        help='Type the Variables',
                        metavar='Variables'
                        )
    parser.add_argument(
                        '-a', '--all',
                        action='store_true',
                        help='Type nothing'
                        )
    parser.add_argument(
                        '-a -v', '--all information',
                        action='store_true',
                        help='Type nothing'
                        )
    args = parser.parse_args()
    #a = readHDF(args.filename).readInfo(args.variables)
    a = readHDF(args.filename)
    if args.variables is None:
        a.printAll()     
    elif args.all is not True:
        a.readInfo(args.variables) 
    else :
        a.printallinfo()
    
