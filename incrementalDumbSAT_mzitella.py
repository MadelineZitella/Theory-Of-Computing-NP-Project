#!/usr/bin/env python3
# DumbSAT re-write with an incremental search through all possible solutions. 
# Madeline Zitella | FA24-CSE-30151-01 Theory of Computing
# Teamname: mzitella 

import matplotlib.pyplot as plt
import time
import csv
import sys

# check if given assignment satisfies all clauses given in the test file for a problem
def satisfied(clauses, assignment):
    for clause in clauses:
        if not any((lit > 0 and assignment[lit - 1]) or (lit < 0 and not assignment[abs(lit) - 1]) for lit in clause):
            return False # assignment does not my_satisfy clause
    return True

# do an incremental search using backtracking to find a variable assignment that is satisfying 
def search_incremental(clauses):
    num_vars = max(abs(lit) for clause in clauses for lit in clause)
    assignment = [None] * num_vars  # initialize to be unassigned 

    # explore all assignments 
    def backtrack(i):
        if i == num_vars: 
            return satisfied(clauses, assignment)# check to see if assignment satisfies clause (call function)

        # try both true 
        assignment[i] = True 
        if backtrack(i + 1):
            return True
        # and false 
        assignment[i] = False
        if backtrack(i + 1):
            return True
        # re-initalize 
        assignment[i] = None
        return False

    return backtrack(0)

# Using kSAT.cnf.csv file given, parse data in order to check satisfiability
def process_tests(file_name):
    input = []
    # Specify encoding because byte order mark was off in the csv file
    with open(file_name, mode='r', encoding='utf-8-sig') as file:
        reader = csv.reader(file)  # Renamed 'csv' to 'reader'
        satisfiability = None  # Initialize to None
        clause_arr = []
        for row in reader:
            row = [element for element in row if element] 
            # Skip empty rows
            if len(row) == 0:
                continue
            # If the row starts with 'c', it's a comment
            if row[0].startswith('c'):
                satisfiability = row[3] if len(row) > 3 else None  # 'U' or 'S'
            # If the row starts with 'p', it's the start of a problem
            elif row[0].startswith('p'):
                num_vars = int(row[2])
                num_clauses = int(row[3])
                clause_arr = []
            # Otherwise, it's a clause, so add it to the clause array
            else:
                clause = [int(lit) for lit in row if lit != '0']
                clause_arr.append(clause)
                if len(clause_arr) == num_clauses:
                    input.append({
                        'num_vars': num_vars,
                        'num_clauses': num_clauses,
                        'clauses': clause_arr,
                        'satisfiability': satisfiability
                    })
                    clause_arr = []
                    satisfiability = None
    return input

# time how long the incremental search takes
# return elapsed time and whether or not satisfiable 
def measure_time(clauses):
    start = time.time()
    satisfiable = search_incremental(clauses)
    end = time.time()
    return end - start, satisfiable

# run the test file and save results into output csv file 
def run_test(file_name, output_file):
    input = process_tests(file_name) # process the csv test file 
    # I am using kSAT.cnf.csv given in Canvas
    sizes, times, results = [], [], []

    # configure a output file to collect results 
    with open(output_file, mode='w', newline='') as file:
        csv_writer = csv.writer(file)
        for problem in input:
            num_vars = problem['num_vars']
            num_clauses = problem['num_clauses']
            clauses = problem['clauses']
            satisfiability = problem['satisfiability']
            # call measure_time function in order to return the time the run takes and either U or S 
            elapsed_time, my_satisfy = measure_time(clauses)
            sizes.append(num_vars)
            times.append(elapsed_time)
            results.append(my_satisfy)

            # printed to space out nicely in terminal 
            print(f"Time: {elapsed_time:>10.6f} seconds | "
            f"# of Variables: {num_vars:>5} | "
            f"Satisfiable?: {str(my_satisfy):<5} | "
            f"Expected Result: {satisfiability:<5}")
            
            if (my_satisfy and satisfiability == 'U') or (not my_satisfy and satisfiability == 'S'):
                # if results do not match we exit the program 
                sys.exit("Stopping.")
            # write to output file
            csv_writer.writerow([num_vars, num_clauses, elapsed_time, my_satisfy, satisfiability])

    return sizes, times, results


# plot results using matplotlib
def plot_results(sizes, times, results):
    plt.figure(figsize=(10, 6))
    # number of variables and time for satisfiable and unsatisfiable (S, U)
    size_S = []
    size_U = []
    time_S = []
    time_U = []

    for size, time, result in zip(sizes, times, results):
        if result:
            size_S.append(size)
            time_S.append(time)
        else:
            size_U.append(size)
            time_U.append(time)
    
    # plot details 
    plt.scatter(size_S, time_S, color='green', marker='o', label='Satisfiable')
    plt.scatter(size_U, time_U, color='red', marker='o', label='Unsatisfiable')
    plt.xlabel('# of Variables')
    plt.ylabel('Time (seconds)')
    plt.title('Incremental Search DumbSAT: Time Per Variable')
    plt.grid(True)
    plt.savefig("plot_mzitella.png") # saving plot into external file 
    plt.legend(loc='upper left')
    plt.show()

def main():
    CSV_OUTPUT_FILE = "output_mzitella.csv" # teamname = mzitella 
    CSV_TEST_FILE = "kSatTestData_mzitella.cnf.csv"
    sizes, times, results = run_test(CSV_TEST_FILE, CSV_OUTPUT_FILE)
    plot_results(sizes, times, results)

if __name__ == '__main__':
    main()
