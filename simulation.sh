#!/bin/bash

echo "full date: "`date  +'%T  %d  %h  %y  (%a)'`

export code=QGas_Simulation
export tdate=`date +%m%d%y_%H%M_%S`
#export T_i=$1
#export T_f=$2
export wdir=./
export ofile=$code"_$1_$2_$tdate.txt"

echo " "
echo "running: "$code.py
echo "on date (MMDDYY_HourMin_Sec): "$tdate
echo "log file: " $ofile
echo "will output to file: " $13

#echo "adding input params: " $1 "and" $2 "in script" $code.py

## method 1 (this one exports to ofile)
python $code.py << eof
$1
$2
$3
$4
$5
$6
$7
$8
$9
${10}
${11}
${12}
${13}
eof


## method 2
#python $code.py << eof > $ofile
#3
#4
#eof


## yet another method
#python test.py << eof > $ofile
#$var1
#$var2
#eof

