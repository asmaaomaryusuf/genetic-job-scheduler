import customtkinter as ctk
from tkinter import filedialog
import random
import matplotlib.pyplot as plt

# ============ Genetic Algorithm ============

def load_jobs(file_path):
    with open(file_path, 'r') as f:
        machines = int(f.readline())
        num_jobs = int(f.readline())
        job_times = list(map(int, f.readline().split()))
    return machines, num_jobs, job_times

def random_individual(num_jobs, num_machines):
    return [random.randint(0, num_machines - 1) for _ in range(num_jobs)]

def fitness(individual, job_times, num_machines):
    machine_loads = [0] * num_machines
    for job_index, machine_index in enumerate(individual):
        machine_loads[machine_index] += job_times[job_index]
    makespan = max(machine_loads)
    return 1 / (1 + makespan)

def crossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:]

def mutate(individual, num_machines, rate=0.1):
    for i in range(len(individual)):
        if random.random() < rate:
            individual[i] = random.randint(0, num_machines - 1)
    return individual

def genetic_algorithm(job_times, num_machines, generations=100, pop_size=30):
    num_jobs = len(job_times)
    population = [random_individual(num_jobs, num_machines) for _ in range(pop_size)]

    for _ in range(generations):
        population = sorted(population, key=lambda x: fitness(x, job_times, num_machines), reverse=True)
        next_gen = population[:5]
        while len(next_gen) < pop_size:
            p1 = random.choice(population[:15])
            p2 = random.choice(population[:15])
            child = crossover(p1, p2)
            child = mutate(child, num_machines)
            next_gen.append(child)
        population = next_gen

    best = population[0]
    best_fitness = fitness(best, job_times, num_machines)
    best_makespan = int(1 / best_fitness - 1)
    return best, best_fitness, best_makespan

# ============ Gantt Chart ============

def plot_gantt(individual, job_times, num_machines):
    machine_schedules = [[] for _ in range(num_machines)]
    machine_current_time = [0] * num_machines

    for job_id, machine_id in enumerate(individual):
        start_time = machine_current_time[machine_id]
        duration = job_times[job_id]
        end_time = start_time + duration
        machine_schedules[machine_id].append((job_id, start_time, duration))
        machine_current_time[machine_id] = end_time

    colors = plt.cm.get_cmap('tab20', len(job_times))

    fig, ax = plt.subplots(figsize=(10, 5))
    for machine_id, schedule in enumerate(machine_schedules):
        for job_id, start, duration in schedule:
            ax.barh(y=machine_id, width=duration, left=start, height=0.5,
                    color=colors(job_id), edgecolor='black')
            ax.text(start + duration / 2, machine_id, f"Job {job_id}",
                    va='center', ha='center', fontsize=8, color='white')

    ax.set_yticks(range(num_machines))
    ax.set_yticklabels([f"Machine {i}" for i in range(num_machines)])
    ax.set_xlabel("Time")
    ax.set_title("Gantt Chart - Job Scheduling")
    ax.grid(True)
    plt.tight_layout()
    plt.show()

# ============ GUI ============

ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

app = ctk.CTk()
app.title("Genetic Algorithm - Job Scheduling")
app.geometry("700x600")

file_path_var = ctk.StringVar()

def browse_file():
    path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if path:
        file_path_var.set(path)
        path_entry.configure(placeholder_text=path.split("/")[-1])

def run_algorithm():
    path = file_path_var.get()
    if not path:
        result_textbox.delete("0.0", "end")
        result_textbox.insert("0.0", "⚠ Please select a file first.")
        return

    try:
        machines, num_jobs, job_times = load_jobs(path)
        best, best_fitness, best_makespan = genetic_algorithm(job_times, machines)

        result_textbox.delete("0.0", "end")
        result_textbox.insert("end", f"Machines: {machines}\n")
        result_textbox.insert("end", f"Jobs: {num_jobs}\n")
        result_textbox.insert("end", f"Fitness: {best_fitness:.4f}\n")
        result_textbox.insert("end", f"Makespan: {best_makespan}\n\n")
        result_textbox.insert("end", "Job → Machine assignment:\n")
        for i, m in enumerate(best):
            result_textbox.insert("end", f"  Job {i} → Machine {m}\n")

        # Show Gantt chart
        plot_gantt(best, job_times, machines)

    except Exception as e:
        result_textbox.delete("0.0", "end")
        result_textbox.insert("0.0", f"Error: {str(e)}")

# ============ Layout ============

ctk.CTkLabel(app, text="Select Job Instance File", font=("Arial", 16)).pack(pady=15)

frame = ctk.CTkFrame(app)
frame.pack(pady=5)

path_entry = ctk.CTkEntry(frame, width=400, placeholder_text="No file selected")
path_entry.pack(side="left", padx=10)

browse_btn = ctk.CTkButton(frame, text="Browse", command=browse_file)
browse_btn.pack(side="left")

run_btn = ctk.CTkButton(app, text="▶ Run Genetic Algorithm", command=run_algorithm, width=300, height=40)
run_btn.pack(pady=20)

result_textbox = ctk.CTkTextbox(app, width=650, height=350, corner_radius=10)
result_textbox.pack(pady=10)

app.mainloop()
