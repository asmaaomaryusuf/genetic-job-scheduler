genetic-job-scheduler
A simulation of Genetic Algorithm applied to job scheduling scenarios

Genetic Algorithm for Job Scheduling

This project implements a Genetic Algorithm (GA) to solve the **Job Scheduling Problem** efficiently. The objective is to assign a set of jobs to available machines in a way that minimizes the total completion time (makespan) and improves resource utilization.

---

Problem Statement

The **Job Scheduling Problem (JSP)** involves assigning `n` jobs to `m` machines with the goal of optimizing a scheduling criterion (e.g., minimizing makespan or job lateness). It's an NP-hard problem commonly found in manufacturing, cloud computing, and operations research.

---

Why Genetic Algorithm?

Genetic Algorithms are powerful metaheuristic optimization techniques inspired by natural selection. They are well-suited for solving combinatorial and complex optimization problems like JSP.

Key reasons to use GA:
- Handles large search spaces
- Does not require gradient information
- Flexible and adaptable

---

How It Works

1. **Initialization**: Generate an initial population of random job sequences.
2. **Fitness Evaluation**: Calculate makespan (or other metrics) for each individual.
3. **Selection**: Use roulette wheel / tournament selection.
4. **Crossover**: Apply one-point or order crossover.
5. **Mutation**: Swap or reverse mutation.
6. **Termination**: Repeat for a fixed number of generations or until convergence.

---

Project Structure

genetic-job-scheduler/

jsp-instance.txt          # Input file: number of machines, number of jobs, and job durations

scheduler.py              # Main script that runs the Genetic Algorithm

README.md                 # Project documentation (you are here)

