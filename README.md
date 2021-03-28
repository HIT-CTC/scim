# SCIM[![tag](https://img.shields.io/badge/version-v0.1.0-blue.svg)]()

**SCIM**(**SCI** **IM**proved) is a new concept based on Linux system to change the way of your scientific research. We aimed at using these scripts or programs to get rid of endless repetitive work and save our precious time to do more valuable research.

## Installation
All programs now are scripts, and the best way to use it is **alias** or **put** in on /usr/bin.

## Usage
### Python
#### output
Requirement: h5py

(You can just use
```bash
./output.py -h
```
to see the usage of this scripts.)
#### h52xdmf
Requirement: h5py
You can just use
```bash
./xdmf_gener.py -h
```
to see the usage of this scripts.
#### quickview
Requirement: PyGnuplot
You can just use
```bash
./xdmf_gener -h
```
to see the usage of this scripts.
### var.py
Requirement: h5py
(You can just use
```bash
./var.py -h
```
to see the usage of this scripts.)

### Bash
#### Plotit\&Plotall
Plotit.sh and plotall.sh is a script to use gnuplot, you can just use
```bash
plotit -f [Filename(.gnu)]
```
to replace
```bash
gnuplot [filename.gnu]
xelatex filename.tex
```
you can also use
```bash
plotall [path]
```
to plot all the gnuplot scripts in a directory.
