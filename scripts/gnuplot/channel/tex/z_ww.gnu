set term epslatex standalone color newstyle 
set xlabel '\Large $z$'
set ylabel '\Large ww'
set key spacing 1.2 left Left reverse
set key samplen 4
set border lw 2
set output "z_ww.tex"
plot './output.dat' u 1:11 with lp lw 4 title '', \
