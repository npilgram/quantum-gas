#!/bin/bash

#nohup simulation_2.sh 3.5 1.2 700 70000 1000. 200. "'Ising'" "'no'" 2 20 20 "'no'" 0 "'Ising_70000_decoh2_20x20_1.txt'" &
#nohup simulation_2.sh 3.5 1.2 700 70000 1000. 200. "'Ising'" "'no'" 2 60 60 "'no'" 0 "'Ising_70000_decoh2_60x60_1.txt'" &
nohup simulation_2.sh 3.7 0.1 1100 50000 1000. 550. "'Ising'" "'no'" 2 1 40 "'no'" 0 "'1D_Ising_3.7_0.1_1100_50000_tau460_1x40_2.txt'" &
