class Process:
    def __init__(self, arrival_time, burst_time, priority):
        self.arrival_time = arrival_time
        self.burst_time = burst_time
        self.priority = priority

def prioritys(arrival_time, burst_time, priority):
    n = len(arrival_time)
    processes = []
    # List to store waiting time for each process
    wt = [0] * n
    # List to store turnaround time for each process
    tat = [0] * n
    # Copy burst times to avoid modifying the original list
    remaining_burst_time = burst_time[:]

    for i in range(n):
        p = Process(arrival_time[i], burst_time[i], priority[i])
        processes.append(p)

    current_time = 0  # Keep track of current time

    while any(remaining_burst_time):
        min_priority = float('inf')
        selected_process = None

        for p in processes:
            if remaining_burst_time[processes.index(p)] > 0 and p.arrival_time <= current_time:
                if p.priority < min_priority:
                    min_priority = p.priority
                    selected_process = p

        if selected_process:
            idx = processes.index(selected_process)
            remaining_burst_time[idx] -= 1

            if remaining_burst_time[idx] == 0:
                tat[idx] = current_time + 1 - arrival_time[idx]
            else:
                # Waiting time is the current time minus arrival time minus burst time remaining
                wt[idx] = current_time - arrival_time[idx] - (burst_time[idx] - remaining_burst_time[idx])

        current_time += 1
    wtd=[]
    for i in range(n):
        wtd.append(tat[i] - burst_time[i])

    return wtd, tat ,sum(wtd)/n,sum(tat)/n




def fcfs(arrival_times, burst_times):
    n = len(arrival_times)

    # Organizing data into a dictionary
    d = {}
    for i in range(n):
        key = "P" + str(i + 1)
        l = [arrival_times[i], burst_times[i]]
        d[key] = l

    # Sorting the dictionary based on arrival times
    d = sorted(d.items(), key=lambda item: item[1][0])

    # Calculating exit time
    ET = []
    for i in range(len(d)):
        if i == 0:
            ET.append(d[i][1][1])
        else:
            ET.append(ET[i - 1] + d[i][1][1])

    # Calculating turnaround time
    TAT = [ET[i] - d[i][1][0] for i in range(len(d))]

    # Calculating waiting time
    WT = [TAT[i] - d[i][1][1] for i in range(len(d))]

    # Calculating average waiting time
    avg_WT = sum(WT) / n
    avg_TAT = sum(TAT) / n

    return WT, TAT, avg_WT, avg_TAT


def sjf(arrival_times, burst_times):
    n = len(arrival_times)
    # Organizing data into a dictionary
    d = {}
    for i in range(n):
        key = "P" + str(i + 1)
        l = [arrival_times[i], burst_times[i]]
        d[key] = l

    # Sorting the dictionary based on arrival times and burst times
    d = sorted(d.items(), key=lambda item: (item[1][0], item[1][1]))

    # Calculating exit time
    ET = []
    for i in range(len(d)):
        if i == 0:
            ET.append(d[i][1][1])
        else:
            ET.append(ET[i - 1] + d[i][1][1])

    # Calculating turnaround time
    TAT = [ET[i] - d[i][1][0] for i in range(len(d))]

    # Calculating waiting time
    WT = [TAT[i] - d[i][1][1] for i in range(len(d))]

    # Calculating average waiting time
    avg_WT = sum(WT) / n
    avg_TAT = sum(TAT) / n

    return WT, TAT, avg_WT, avg_TAT

def srtf(arrival_times, burst_times):
    n = len(arrival_times)

    # Copy the burst times to a separate list to keep track of remaining burst time
    remaining_burst_time = burst_times[:]

    # Initialize variables
    current_time = 0
    completed = 0
    WT = [0] * n  # Waiting time
    TAT = [0] * n  # Turnaround time

    while completed != n:
        min_burst_time = float('inf')
        shortest_job_index = -1

        # Find the process with the shortest remaining burst time that has arrived
        for i in range(n):
            if arrival_times[i] <= current_time and remaining_burst_time[i] < min_burst_time and remaining_burst_time[i] > 0:
                min_burst_time = remaining_burst_time[i]
                shortest_job_index = i

        if shortest_job_index == -1:
            current_time += 1
            continue

        # Reduce remaining burst time of the selected process
        remaining_burst_time[shortest_job_index] -= 1

        # If a process is completed
        if remaining_burst_time[shortest_job_index] == 0:
            completed += 1
            completion_time = current_time + 1

            # Calculate turnaround time and waiting time for the completed process
            TAT[shortest_job_index] = completion_time - arrival_times[shortest_job_index]
            WT[shortest_job_index] = TAT[shortest_job_index] - burst_times[shortest_job_index]

            # Update current time
            current_time = completion_time
        else:
            # If the process is not completed, move to the next time unit
            current_time += 1

    avg_WT = sum(WT) / n
    avg_TAT = sum(TAT) / n
    return WT, TAT , avg_WT,avg_TAT