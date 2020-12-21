set term epslatex standalone color newstyle 
set xlabel '\Large $z^+$' 
set ylabel '\Large w'
set xrange[0:200]
set logscale x
set key spacing 1.2 left Left reverse
set key samplen 4
set border lw 2
set output "w_sym.tex"
plot './output.dat' every 1::105::204 u (395.4-$2):(-$10) with l lw 4 title 'Upper', \
     './output.dat' every 1::5::105 u 2:10 with l lw 4 title 'Lower', \
