set term epslatex standalone color newstyle 
set xlabel '\Large $z^+$' 
set ylabel '\Large ww'
set xrange[0:400]
set key spacing 1.2 left Left reverse
set key samplen 4
set border lw 2
set output "ww.tex"
plot  './output.dat' u 2:11 with l lw 4 title ''
