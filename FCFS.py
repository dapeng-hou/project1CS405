from concurrent.futures import process
from time import sleep
import json


process_list = []
time = 0
CPU_list = []
process_dict = dict()
next_step_dict = dict()

with open('processes.json') as f:
    data = json.load(f)
   # print(data)

for key, value in data.items():
    process_list.append(key)
    process_index = []
    for key1, value1 in value.items():

        l = []
        for key2, value2 in value1.items():

            l.append(key2)
            l.append(value2)
        process_index.append(l)
    process_dict[key] = process_index
print(process_dict)

CPU_timer = 0
IO_timer = []
while True:
    for key, value in process_dict.items():
        if(value[0][1] == time):
            l = []
            print(key, ": is created at ", time)
            l.append(time)          # start time mark
            l.append(value[2][1])   # Burst time
            l.append(value[2][0])   # Burst type
            l.append(2)             # Burst index in the array
            next_step_dict[key] = l

       # next_step_dict = sorted(next_step_dict.items(), key=lambda item: item[0])
        if next_step_dict:
            #print(next_step_dict)
            for next_step_key, next_step_value in next_step_dict.items():
                #print(next_step_value)
                if next_step_value[0] + next_step_value[1] == time: #cpu burst finished
                    print(next_step_key, ': CPU to IO queue at ', time)

                    IO_timer.append(next_step_key)
                    IO_timer.append(process_dict[next_step_key][next_step_value[3] + 1][1])

                    l = []
                    l.append(time + process_dict[next_step_key][next_step_value[3] + 1][1])  # start time mark
                    l.append(process_dict[next_step_key][next_step_value[3] + 2][1])  # Burst time
                    l.append(process_dict[next_step_key][next_step_value[3] + 2][0])  # Burst type
                    l.append(next_step_value[3] + 2)  # Burst index in the array
                    next_step_dict[next_step_key] = l

    time += 1
    if IO_timer:
        IO_timer[1] -= 1
        if IO_timer[1] == 0:
            print(IO_timer[0], ': IO to ready queue at ', time)
            IO_timer[1] = -1
    print('time = ', time)


