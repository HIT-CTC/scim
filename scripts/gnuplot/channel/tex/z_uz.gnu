set term epslatex standalone color newstyle 
set xlabel '\Large $z$' 
set ylabel '\Large dudz'
set key left reverse Left spacing 1.2
set key samplen 4
set border lw 2
set output "z_uz.tex"
plot './output.dat' u 1:6 with l lw 4 title '', \
