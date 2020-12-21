set term epslatex standalone color newstyle 
set xlabel '\Large $z$'
set ylabel '\Large uw'
set key spacing 1.2
set key samplen 4
set border lw 2
set output "z_uw.tex"
plot './output.dat' u 1:5 with l lw 4 title '', \
