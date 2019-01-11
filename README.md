# CTF
Thermal-hydraulics and subchannel simulations

The purpose of the project is to generate a full-core subchannel model for a PWR; the python script "ctf_fullcore_01.py" creates the steady state case, the script "ctf_fullcore_02.py" the transient case. The data are written into the CTF template input file "KXX_SIM5_1-1-1_template" and "KXX_SIM5_1-1-1_template_transient" respectively. 

As an example a 3x3 fuel assembly "mini-core" model is generated. It has 36 six axial nodes and 2209 subchannels for a 16x16-20 FA type.

The radial layout and fuel assembly names is shown in figure 1:
![Figure 1:](./ctf_radial_fa_model_16x16.jpg)

The radial FA layout is shown in figure 2:
![Figure 2:](./ctf_radial_model_3x3.jpg)

The schema of the axial FA layout is shown in figure 3:
![Figure 3:](./ctf_axial_model_3x3.jpg)

The steady state results for the mass flow of fuel assembly FA 14 for every subchannel is shown in figure 4:
![Figure 4:](./ctf_result_3x3_steady_state_FA14_mass_flow_per_channel.jpg)

The steady state results for the pressure of fuel assembly FA 14 for every subchannel is shown in figure 5 as function of node:
![Figure 5:](./ctf_result_3x3_steady_state_FA14_pressure_per_channel.jpg)

The steady state results for the temperature of fuel assembly FA 14 for every subchannel is shown in figure 6 as a function of node:
![Figure 6:](./ctf_result_3x3_steady_state_FA14_temperature_rise_per_node_per_channel.jpg)

The steady state results for the periphery gap cross flow of fuel assembly FA 14 for every subchannel is shown in figure 7 as a function of node:
![Figure 7:](./ctf_result_3x3_steady_state_FA14_cross_flow_border_gaps_per_node.jpg)
