import math

frequency = 50  # Hz
sampling_rate = 100  # Hz
duration = 1  # s


t = [i/sampling_rate for i in range(int(duration*sampling_rate))]

amplitude_v = 565.69
amplitude_i = 70

v_1_phase = 0
v_2_phase = 2*math.pi/3
v_3_phase = 4*math.pi/3

i_1_phase = 0
i_2_phase = 2*math.pi/3
i_3_phase = 4*math.pi/3

v_1_signal_value = [amplitude_v*math.sin(2*math.pi*frequency*time+v_1_phase) for time in t]
v_2_signal_value = [amplitude_v*math.sin(2*math.pi*frequency*time+v_2_phase) for time in t]
v_3_signal_value = [amplitude_v*math.sin(2*math.pi*frequency*time+v_3_phase) for time in t]

i_1_signal_value = [amplitude_i*math.sin(2*math.pi*frequency*time+i_1_phase) for time in t]
i_2_signal_value = [amplitude_i*math.sin(2*math.pi*frequency*time+i_2_phase) for time in t]
i_3_signal_value = [amplitude_i*math.sin(2*math.pi*frequency*time+i_3_phase) for time in t]
