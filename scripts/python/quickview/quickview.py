#!/usr/bin/python

import PyGnuplot as gp
import numpy as np
import re
import sys
import argparse as ag
from pathlib import Path

class gnuQuickView(object):
    def __init__(self, fn, is_xlog=False, is_ylog=False, xrange=None, yrange=None):
        self.fn      = Path(fn).expanduser().resolve()
        self.is_xlog = is_xlog
        self.is_ylog = is_ylog
        self.xrange  = xrange
        self.yrange  = yrange

    def varList(self):
        data = open(self.fn, 'r')
        data.readline()
        data.readline()
        strings = data.readline()
        contains = strings.split()
        data.close()
        print(contains)
        
    def quickView(self, var):
        self.var = var
        #--------- Read Strings In File ---------# 
        data = open(self.fn, 'r')
        data.readline()
        data.readline()
        strings = data.readline()
        contains = strings.split()
        data.close()
        #---------- Input Number Or Str ----------#
        is_str = re.compile('\d+')
        if is_str.match(self.var[0]) is not None:
            for i in range(len(self.var)):
                self.var[i] = int(self.var[i])
        #-------- Find Index Of Variable --------#
        else:
            for i in range(len(self.var)):
                if self.var[i] not in contains:
                    print('Error!:Please check what you want to plot')
                    print(contains)
                    sys.exit()
                else:
                    self.var[i] = contains.index(self.var[i])+1
        ##-------------- Plot It Now --------------#
        var_x   = self.var.pop(0)
        var_y   = self.var
        label_x = contains[var_x-1]
        label_y = ''
        for v in var_y:
            label_y += contains[v-1]+' '
        gp.c('set xlabel "{}"'.format(label_x)) 
        gp.c('set ylabel "{}"'.format(label_y))
        if self.is_xlog:
            gp.c('set logscale x')
        if self.is_ylog:
            gp.c('set logscale y')
        if self.xrange != None:
            gp.c('set xrange[{}:{}]'.format(self.xrange[0],self.xrange[1]))
        if self.yrange != None:
            gp.c('set yrange[{}:{}]'.format(self.yrange[0],self.yrange[1]))
        str_output = 'plot '
        for v in var_y:
            str_output += '"{}" u {}:{} w l lw 2 t "{}",'.format(self.fn, var_x, v, contains[v-1])
        gp.c(str_output)
        
#-----------------------------------------#
#-------- Main Code Of Quick View --------#
#-----------------------------------------#
if __name__ == '__main__':
    parser = ag.ArgumentParser(prog='QuickView',
                               description='Quick View Data using Gnuplot')
    parser.add_argument(
                        '-f', '--filename',            # Option Name
                        required='True',               # Requirement
                        help='Type the Filename(must)',# Help log
                        metavar='Filename'             # [-f filename]
                        )
    parser.add_argument(
                        '-v', '--variables',
                        action='extend',               # Action of option
                        nargs='+',                     # N args
                        help='Type the Variables',
                        metavar='Variables'
                        )
    parser.add_argument(
                        '-x', '--xrange',
                        action='extend',            
                        nargs=2,                     
                        help='Range in x tic.',
                        metavar='Num'
                        )
    parser.add_argument(
                        '-y', '--yrange',
                        action='extend',            
                        nargs=2,                     
                        help='Range in y tic.',
                        metavar='Num'
                        )
    parser.add_argument(
                        '--logx',
                        action='store_true',            
                        help='Log scale in x tic',
                        )
    parser.add_argument(
                        '--logy',
                        action='store_true',            
                        help='Log scale in y tic',
                        )
    parser.add_argument(
                        '-c', '--check',
                        action='store_true',            
                        help='Check all variables',
                        )
    args=parser.parse_args()

    if args.check:
        print('The variables are:')
        gnuQuickView(args.filename).varList()
        sys.exit(0)

    gnuQuickView(args.filename, args.logx, args.logy, args.xrange, args.yrange).quickView(args.variables)
