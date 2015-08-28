#!/bin/bash

nohup simulation_2.sh 4.5 1.5 810 50000 1000. 200. "'Ising Bell State'" "'no'" 2 40 40 "'no'" 0 "'Quenched_Ising_Bell_50000_decoh2_40x40_2.txt'" &
nohup simulation_2.sh 4.5 1.5 810 50000 1000. 200. "'Ising Bell State'" "'no'" 2 20 20 "'no'" 0 "'Quenched_Ising_Bell_50000_decoh2_20x20_1.txt'" &
nohup simulation_2.sh 4.5 1.5 810 50000 1000. 200. "'Ising Bell State'" "'no'" 2 60 60 "'no'" 0 "'Quenched_Ising_Bell_50000_decoh2_60x60_1.txt'" &
