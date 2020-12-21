#!/bin/bash

# Exec
LC=xelatex
GC=gnuplot
dir=0

helpFunction()
{
	echo ""
	echo "Usage of $0"
	echo "-h: Manual"
	echo "-f: Filename of the gnuplot script(almost in '.gnu')"
	echo "-d: In a dirty way."
	exit 1
}

while getopts "hf:d" opt
do
	case "$opt" in
		f ) fn=$OPTARG ;;
		d ) dir=1 ;;
		? ) helpFunction ;;
	esac
done

[ $fn ] && [ `expr index "$fn" .` != 0 ] && ([ ${fn#*.} = gnu ] || (echo 'Please select right type .gnu not .'${fn#*.}'';exit 1)) && fn=${fn%.*} 
[ $fn ] && gnufile=""$fn".gnu" ; texfile=""$fn".tex" ; path=${fn%/*} ; [ -d $path ] && cd $path
([ -f $gnufile ] || (echo "Not this file '$gnufile'"; exit 1)) && $GC $gnufile && ([ -f $texfile ] || (echo "Not this file '$texfile'"; exit 1)) && $LC $texfile 1>/dev/null && [ $dir -ne 1 ] && rm ""$fn".aux" ""$fn".log" ""$fn"-inc.eps"
