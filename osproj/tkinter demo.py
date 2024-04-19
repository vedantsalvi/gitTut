import tkinter as tk

from algos import fcfs, sjf, srtf,prioritys  # Import the fcfs function from scheduling.py
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
        if quantum == 0:
            label.config(text="Time Quantum cant be zero")
            return 
        result_rr = rr.rr(arrival_times, burst_times, quantum)
        wt = result_rr['wt_list']
        tat = result_rr['tat_list']
        avg_wt = result_rr['avg_wt']
        avg_tat = result_rr['avg_tat']
    elif selected_algo == "Priority":
        priority = list(map(int, entry_priority.get().split()))  # Get the priority list from the input
        wt, tat, avg_wt, avg_tat = prioritys(arrival_times, burst_times, priority)
    elif selected_algo == "SRTF":
        wt, tat, avg_wt, avg_tat = srtf(arrival_times, burst_times)
    elif selected_algo == "SJF":
        wt, tat, avg_wt, avg_tat = sjf(arrival_times, burst_times)

    # Check if wt and tat lists contain elements
    if wt and tat:
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
        # Draw Gantt chart
        if selected_algo == "FCFS":
            draw_gantt_chart_fcfs(selected_algo, arrival_times, burst_times, wt)

def draw_gantt_chart_fcfs(selected_algo, arrival_times, burst_times, wt):
    canvas.delete("all")  # Clear canvas before drawing

    x_start = 50
    y = 100  # Fixed y-coordinate for all processes
    bar_height = 30
    text_offset = 5  # Offset for text labels

    total_time = sum(burst_times)
    scaling_factor = 400 / total_time  # Adjust 400 as needed for canvas width

    # Calculate the start and end points for each process
    process_points = []
    current_time = 0
    for i in range(len(arrival_times)):
        start_time = arrival_times[i] + wt[i] if i < len(wt) else arrival_times[i]
        end_time = start_time + burst_times[i]
        x0 = x_start + current_time * scaling_factor
        x1 = x0 + burst_times[i] * scaling_factor
        process_points.append((x0, x1))
        current_time = end_time

    # Draw rectangles for each process and display start/end times
    start =0 
    for i in range(len(arrival_times)):
        x0, x1 = process_points[i]
        y0 = y
        y1 = y0 + bar_height

        # Draw rectangle representing the process
        canvas.create_rectangle(x0, y0, x1, y1, fill="skyblue")
        canvas.create_text(x0, y0 + bar_height / 2, anchor=tk.W, text=f" P{i+1}")

        # Display start and end times
        canvas.create_text(x0, y0 - text_offset, anchor=tk.W, text=f"Start: {start}")
        end = arrival_times[i] + burst_times[i] + (wt[i] if i < len(wt) else 0)
        canvas.create_text(x1, y1 + text_offset, anchor=tk.E, text=f"End: {end}")
        start = end+1

    
def update_interface(*args):
    selected_algo = var.get()
    if selected_algo == "Round Robin":
        # Create a label and entry field for quantum time input (Round Robin)
        quantum_label.grid(row=3, column=0, padx=5, pady=5)
        entry_quantum.grid(row=3, column=1, padx=5, pady=5)
        # Hide the priority input fields if visible
        priority_label.grid_forget()
        entry_priority.grid_forget()
        canvas.delete("all")
    elif selected_algo == "Priority":
        # Create a label and entry field for priority input (Priority)
        priority_label.grid(row=4, column=0, padx=5, pady=5)
        entry_priority.grid(row=4, column=1, padx=5, pady=5)
        # Hide the quantum input field if visible
        quantum_label.grid_forget()
        entry_quantum.grid_forget()
        canvas.delete("all")
    else:
        # Hide both quantum and priority input fields for other algorithms
        quantum_label.grid_forget()
        entry_quantum.grid_forget()
        priority_label.grid_forget()
        entry_priority.grid_forget()
        canvas.delete("all")

root = tk.Tk()
root.title("Scheduling Simulator")

font_size = 12
algo_label = tk.Label(root, text="Select an algorithm:")
algo_label.grid(row=0, column=0, padx=5, pady=5)

algos = ["FCFS", "Priority", "Round Robin", "SJF", "SRTF"]
var = tk.StringVar(root)
var.set(algos[0])
dropdown = tk.OptionMenu(root, var, *algos, command=update_interface)
dropdown.grid(row=0, column=1, padx=5, pady=5)

arrival_label = tk.Label(root, text="Enter arrival times separated by spaces:",font=("Arial", font_size))
arrival_label.grid(row=1, column=0, padx=5, pady=5)

entry_arrival = tk.Entry(root, width=30,font=("Arial", font_size))
entry_arrival.grid(row=1, column=1, padx=5, pady=5)

burst_label = tk.Label(root, text="Enter burst times separated by spaces:",font=("Arial", font_size))
burst_label.grid(row=2, column=0, padx=5, pady=5)

entry_burst = tk.Entry(root, width=30,font=("Arial", font_size))
entry_burst.grid(row=2, column=1, padx=5, pady=5)

# Initialize the quantum and priority input fields
quantum_label = tk.Label(root, text="Enter quantum time:",font=("Arial", font_size))
entry_quantum = tk.Entry(root, width=10,font=("Arial", font_size))

priority_label = tk.Label(root, text="Enter priority if applicable separated by spaces:",font=("Arial", font_size))
entry_priority = tk.Entry(root, width=30,font=("Arial", font_size))


# Create a button
button = tk.Button(root, text="Get Schedule", command=on_button_click,font=("Arial", font_size))
button.grid(row=5, columnspan=2, padx=5, pady=5)


# Create a label for displaying the result
label = tk.Label(root, text="",font=("Arial", font_size))
label.grid(row=6, columnspan=2, padx=5, pady=5)

# Create a canvas for drawing Gantt chart
canvas = tk.Canvas(root, width=600, height=300)
canvas.grid(row=7, columnspan=2, padx=5, pady=5)


# Run the Tkinter event loop
root.mainloop()
