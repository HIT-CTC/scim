set term epslatex standalone color newstyle 
set xlabel '\Large $z$' 
set ylabel '\Large u'
set key spacing 1.2 left Left reverse
set key samplen 4
set border lw 2
set output "z_u.tex"
plot './output.dat' u 1:3 with l lw 4 title '', \
