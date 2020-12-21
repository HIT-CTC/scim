#/bin/bash

[ $1 ]&&cd $1

# Plot all gnu file
for file in `ls *.gnu`
do
  ~/.useful_bash/plotit.sh -f $file
  echo Plot $file done!
done
