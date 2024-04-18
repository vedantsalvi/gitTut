from typing import List, Dict, Any

def rr(arrival_time: List[int], burst_time: List[int], time_quantum: int) -> Dict[str, Any]:
    if time_quantum<1:
        return {'tat_list': list(0), 'wt_list': list(0), 'avg_tat': list(0), 'avg_wt': list(0)}
    processes_info = [
        {'job': f'P{i+1}' if len(arrival_time) > 26 else chr(i + 10 + ord('A')),
         'at': arrival_time[i],
         'bt': burst_time[i]} for i in range(len(arrival_time))
    ]
    processes_info.sort(key=lambda x: (x['at'], x['job']))

    solved_processes_info = []
    gantt_chart_info = []

    ready_queue = []
    current_time = processes_info[0]['at']
    unfinished_jobs = processes_info.copy()

    remaining_time = {process['job']: process['bt'] for process in processes_info}

    ready_queue.append(unfinished_jobs[0])
    while sum(remaining_time.values()) > 0 and unfinished_jobs:
        if not ready_queue and unfinished_jobs:
            ready_queue.append(unfinished_jobs[0])
            current_time = ready_queue[0]['at']

        process_to_execute = ready_queue[0]

        if remaining_time[process_to_execute['job']] <= time_quantum:
            remaining_t = remaining_time[process_to_execute['job']]
            remaining_time[process_to_execute['job']] -= remaining_t
            prev_current_time = current_time
            current_time += remaining_t

            gantt_chart_info.append({
                'job': process_to_execute['job'],
                'start': prev_current_time,
                'stop': current_time
            })
        else:
            remaining_time[process_to_execute['job']] -= time_quantum
            prev_current_time = current_time
            current_time += time_quantum

            gantt_chart_info.append({
                'job': process_to_execute['job'],
                'start': prev_current_time,
                'stop': current_time
            })

        process_to_arrive_in_this_cycle = [p for p in processes_info if
                                           p['at'] <= current_time and
                                           p != process_to_execute and
                                           p not in ready_queue and
                                           p in unfinished_jobs]

        ready_queue.extend(process_to_arrive_in_this_cycle)
        ready_queue.append(ready_queue.pop(0))

        if remaining_time[process_to_execute['job']] == 0:
            unfinished_jobs.remove(process_to_execute)
            ready_queue.remove(process_to_execute)

            solved_processes_info.append({
                **process_to_execute,
                'ft': current_time,
                'tat': current_time - process_to_execute['at'],
                'wt': current_time - process_to_execute['at'] - process_to_execute['bt']
            })

    solved_processes_info.sort(key=lambda x: (x['at'], x['job']))

    # Calculate total TAT and WT
    total_tat = sum(process['tat'] for process in solved_processes_info)
    total_wt = sum(process['wt'] for process in solved_processes_info)

    # Calculate average TAT and WT
    avg_tat = total_tat / len(solved_processes_info)
    avg_wt = total_wt / len(solved_processes_info)

    # Extracting only the TAT and WT values
    tat_list = [process['tat'] for process in solved_processes_info]
    wt_list = [process['wt'] for process in solved_processes_info]

    return {'tat_list': tat_list, 'wt_list': wt_list, 'avg_tat': avg_tat, 'avg_wt': avg_wt}
