set term epslatex standalone color newstyle 
set xlabel '\Large $z$' 
set ylabel '\Large uu'
set key spacing 1.2
set key samplen 4
set border lw 2
set output "z_uu.tex"
plot './output.dat' u 1:4 with l lw 4 title '', \
