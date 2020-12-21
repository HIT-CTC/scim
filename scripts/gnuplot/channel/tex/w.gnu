set term epslatex standalone color newstyle 
set xlabel '\Large $z^+$' 
set ylabel '\Large w'
set xrange[0:400]
set key spacing 1.2 left Left reverse
set key samplen 4
set border lw 2
set output "w.tex"
plot  './output.dat' u 2:10 with l lw 4 title ''
