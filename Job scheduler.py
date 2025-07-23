import random

# read data from file
def load_jobs(file_path):
    with open(file_path, 'r') as f:
        machines = int(f.readline())
        num_jobs = int(f.readline())
        job_times = list(map(int, f.readline().split()))
    return machines, num_jobs, job_times

# random indevedual
def random_individual(num_jobs, num_machines):
    return [random.randint(0, num_machines - 1) for _ in range(num_jobs)]

# calc fitness
def fitness(individual, job_times, num_machines):
    machine_loads = [0] * num_machines
    for job_index, machine_index in enumerate(individual):
        machine_loads[machine_index] += job_times[job_index]
    makespan = max(machine_loads)
    return 1 / (1 + makespan)

# crossover
def crossover(p1, p2):
    point = random.randint(1, len(p1) - 1)
    return p1[:point] + p2[point:]

# mutation
def mutate(individual, num_machines, rate=0.1):
    for i in range(len(individual)):
        if random.random() < rate:
            individual[i] = random.randint(0, num_machines - 1)
    return individual

# GA loop
def genetic_algorithm(job_times, num_machines, generations=100, pop_size=30):
    num_jobs = len(job_times)
    population = [random_individual(num_jobs, num_machines) for _ in range(pop_size)]

    for gen in range(generations):
        population = sorted(population, key=lambda x: fitness(x, job_times, num_machines), reverse=True)
        next_gen = population[:5]  # save best 5
        while len(next_gen) < pop_size:
            p1 = random.choice(population[:15])
            p2 = random.choice(population[:15])
            child = crossover(p1, p2)
            child = mutate(child, num_machines)
            next_gen.append(child)

        population = next_gen
        best = population[0]
        best_fitness = fitness(best, job_times, num_machines)
        print(f"Gen {gen}: Fitness = {best_fitness:.4f}, Makespan = {1 / best_fitness - 1:.0f}")

    return population[0]

# main
if __name__ == "__main__":
    machines, num_jobs, job_times = load_jobs("jsp-instance.txt")
    best = genetic_algorithm(job_times, machines)
    print("\n Best Assignment (Job → Machine):")
    for job, machine in enumerate(best):
        print(f"Job {job} → Machine {machine}")
