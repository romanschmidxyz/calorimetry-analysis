# Calorimetry Analysis
This program creates a T-t and dT/dt - t calorimetry plots and calculates Delta T_X, the temperature rise upon sample
combustion using the equal areas method and extrapolated pre- and post-period curves. Additionally an error estimate is calculated as described in Appendix B, equation 11 of the following document:
https://github.com/romanschmidxyz/calorimetry-analysis/blob/main/Bomb_Calorimetry_2025.pdf

## Instructions for use
- The program will prompt you for the file name: "your_filename" No need to add the ".csv"
- It will also prompt you for the name of your sample (This is used to display the plot titles).
- adjust upper and lower thresholds if necessary to get the desired boundaries for the rise period.

## Output
- DeltaT_x =  2.6679311422422565
- Error of DeltaT_x =  0.003293481196792661
![Alt text](https://github.com/romanschmidxyz/calorimetry-equal-areas/blob/main/BA1.png)
  
