#!/bin/bash

nohup simulation_2.sh 3.5 1.2 700 70000 1000. 200. "'Ising'" "'no'" 2 20 20 "'no'" 0 "'Ising_70000_decoh2_20x20_1.txt'" &
nohup simulation_2.sh 3.5 1.2 700 70000 1000. 200. "'Ising'" "'no'" 2 60 60 "'no'" 0 "'Ising_70000_decoh2_60x60_1.txt'" &
nohup simulation_2.sh 3.5 1.2 700 70000 1000. 200. "'Ising'" "'no'" 2 40 40 "'no'" 0 "'Ising_70000_decoh2_40x40_3.txt'" &
