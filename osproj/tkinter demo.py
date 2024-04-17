import tkinter as tk
from algos import fcfs, sjf, srtf, priority  # Import the fcfs function from scheduling.py
import rr

# Function to perform FCFS scheduling and calculate waiting time, turnaround time, and average waiting time
def on_button_click():
    selected_algo = var.get()
    priority = list(map(int,entry_priority.get().split()))
    arrival_times = list(map(int, entry_arrival.get().split()))  # Convert input arrival times to integers
    burst_times = list(map(int, entry_burst.get().split()))  # Split the input string into a list of burst times

    if selected_algo == "FCFS":
        wt, tat, avg_wt, avg_tat = fcfs(arrival_times, burst_times)  # Calculate the total burst time 
    elif selected_algo == "Round Robin":
        quantum = int(entry_quantum.get())
        result_rr = rr.rr(arrival_times, burst_times, quantum)
        wt = result_rr['wt_list']
        tat = result_rr['tat_list']
        avg_wt = result_rr['avg_wt']
        avg_tat = result_rr['avg_tat']
    elif selected_algo == "Priority":
        li = [2, 1, 3, 5]  # Priority list example, you may need to adjust it according to your requirement
        wt, tat, avg_wt, avg_tat = priority(arrival_times, burst_times, li)
    elif selected_algo == "SRTF":
        wt, tat, avg_wt, avg_tat = srtf(arrival_times, burst_times)
    elif selected_algo == "SJF":
        wt, tat, avg_wt, avg_tat = sjf(arrival_times, burst_times)

    # Prepare the text to display in the label
    label_text = f"Total arrival time for {selected_algo}: {sum(wt)}\n"
    label_text += f"Total burst time for {selected_algo}: {sum(burst_times)}\n"
    label_text += "Process | Arrival | Burst | Exit | Turn Around | Wait |\n"
    for i in range(len(wt)):
        label_text += f"  P{i+1:3d}     |   {arrival_times[i]:7d}   |    {burst_times[i]:5d}   |    {wt[i]+burst_times[i]:4d}   |    {tat[i]:10d}   |   {wt[i]:4d}   |\n"

    label_text += f"Average Waiting Time: {avg_wt}\n"
    label_text += f"Average Turnaround Time: {avg_tat}"

    # Update the label text
    label.config(text=label_text)


# Create the main window
root = tk.Tk()
root.title("Scheduling Simulator")

# Create a label for the dropdown menu
algo_label = tk.Label(root, text="Select an algorithm:")
algo_label.grid(row=0, column=0, padx=5, pady=5)

# Create a dropdown menu for selecting algorithms
algos = ["FCFS", "Priority", "Round Robin", "SJF", "SRTF"]
var = tk.StringVar(root)
var.set(algos[0])  # default value
dropdown = tk.OptionMenu(root, var, *algos)
dropdown.grid(row=0, column=1, padx=5, pady=5)

# Create a label for arrival times input
arrival_label = tk.Label(root, text="Enter arrival times separated by spaces:")
arrival_label.grid(row=1, column=0, padx=5, pady=5)

# Create an entry field for arrival times input
entry_arrival = tk.Entry(root, width=30)
entry_arrival.grid(row=1, column=1, padx=5, pady=5)

# Create a label for burst times input
burst_label = tk.Label(root, text="Enter burst times separated by spaces:")
burst_label.grid(row=2, column=0, padx=5, pady=5)

# Create an entry field for burst times input
entry_burst = tk.Entry(root, width=30)
entry_burst.grid(row=2, column=1, padx=5, pady=5)

# Create a label and entry field for quantum time input (Round Robin)
quantum_label = tk.Label(root, text="Enter quantum time:")
quantum_label.grid(row=3, column=0, padx=5, pady=5)

entry_quantum = tk.Entry(root, width=10)
entry_quantum.grid(row=3, column=1, padx=5, pady=5)

priority_label = tk.Label(root, text="Enter priority if applicable separated by spaces:")
priority_label.grid(row=4, column=0, padx=5, pady=5)
#Create a label and entry field for priority time input (Round Robin)
entry_priority = tk.Entry(root, width=30)
entry_priority.grid(row=4, column=1, padx=5, pady=5)


# Create a button
button = tk.Button(root, text="Calculate Total Times", command=on_button_click)
button.grid(row=5, columnspan=2, padx=5, pady=5)


# Create a label for displaying the result
label = tk.Label(root, text="")
label.grid(row=6, columnspan=2, padx=5, pady=5)


# Run the Tkinter event loop
root.mainloop()
