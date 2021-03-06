set term epslatex standalone color newstyle 
set xlabel '\Large $z^+$' 
set ylabel '\Large uu'
set xrange[0:200]
set logscale x
set key spacing 1.2
set key samplen 4
set border lw 2
set output "uu_sym.tex"
plot './output.dat' every 1::105::204 u (395.4-$2):4 with l lw 4  title 'Upper', \
     './output.dat' every 1::5::105 u 2:4 with l lw 4 title 'Lower', \
     '~/DATA/data_old/channel/channel_Moin/retau180/LM_Channel_0180_vel_fluc_prof.dat' u 2:3 with l lw 4 title 'Moser'
