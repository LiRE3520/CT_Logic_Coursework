def load_dimacs(file_name):
    #file_name will be of the form "problem_name.txt"
    with open(file_name, "r") as file:
        content = file.read()
    content = content.split("\n")
    clauses = []
    for line in content:
        if line == "":
            continue
        if line[0] == "c" or line[0] == "p":
            continue
        current_clause = []
        split_line = line.split(" ")
        for literal in split_line:
            if literal != "0":
                current_clause.append(int(literal))
        clauses.append(current_clause)
    return clauses

def simple_sat_solve(clause_set):
    def convert_to_list_of_literals(assignment):
        literal_list = []
        for i in range(len(assignment)):
            if assignment[i]:
                literal_list.append(i + 1)
            else:
                literal_list.append((i + 1) * -1)
        return literal_list
    variables = set()
    for clause in clause_set:
        for literal in clause:
            variables.add(abs(literal))
    assignments = []
    for i in range(2 ** len(variables)):
        binary = bin(i)[2:]
        binary = '0' * (len(variables) - len(binary)) + binary
        current_assignment = []
        for bit in binary:
            if bit == "0":
                current_assignment.append(False)
            else:
                current_assignment.append(True)
        assignments.append(current_assignment)
    for assignment in assignments:
        satisfies = True
        for clause in clause_set:
            clause_evaluation = False
            for literal in clause:
                if literal > 0:
                    if assignment[literal - 1]:
                        clause_evaluation = True
                        break
                else:
                    if not assignment[abs(literal) - 1]:
                        clause_evaluation = True
                        break
            if clause_evaluation == False:
                satisfies = False
                break
        if satisfies:
            return convert_to_list_of_literals(assignment)
    return False

def branching_sat_solve(clause_set,partial_assignment):
    c = 0
    while (c < len(clause_set)) or (branch is not None):
        for literal in partial_assignment:
            if literal in clause_set[c]:
                break
        else:
            branch = clause_set[c]
        c += 1
    if branch is None:
        return partial_assignment
    

        

        



                




def unit_propagate(clause_set):
    ...


def dpll_sat_solve(clause_set,partial_assignment):
    ...

test = load_dimacs("sat.txt")
print(simple_sat_solve(test))

# def test():
#     print("Testing load_dimacs")
#     try:
#         dimacs = load_dimacs("sat.txt")
#         assert dimacs == [[1],[1,-1],[-1,-2]]
#         print("Test passed")
#     except:
#         print("Failed to correctly load DIMACS file")

#     print("Testing simple_sat_solve")
#     try:
#         sat1 = [[1],[1,-1],[-1,-2]]
#         check = simple_sat_solve(sat1)
#         assert check == [1,-2] or check == [-2,1]
#         print("Test (SAT) passed")
#     except:
#         print("simple_sat_solve did not work correctly a sat instance")

#     try:
#         unsat1 = [[1, -2], [-1, 2], [-1, -2], [1, 2]]
#         check = simple_sat_solve(unsat1)
#         assert (not check)
#         print("Test (UNSAT) passed")
#     except:
#         print("simple_sat_solve did not work correctly an unsat instance")

#     print("Testing branching_sat_solve")
#     try:
#         sat1 = [[1],[1,-1],[-1,-2]]
#         check = branching_sat_solve(sat1,[])
#         assert check == [1,-2] or check == [-2,1]
#         print("Test (SAT) passed")
#     except:
#         print("branching_sat_solve did not work correctly a sat instance")

#     try:
#         unsat1 = [[1, -2], [-1, 2], [-1, -2], [1, 2]]
#         check = branching_sat_solve(unsat1,[])
#         assert (not check)
#         print("Test (UNSAT) passed")
#     except:
#         print("branching_sat_solve did not work correctly an unsat instance")


#     print("Testing unit_propagate")
#     try:
#         clause_set = [[1],[-1,2]]
#         check = unit_propagate(clause_set)
#         assert check == []
#         print("Test passed")
#     except:
#         print("unit_propagate did not work correctly")


#     print("Testing DPLL") #Note, this requires load_dimacs to work correctly
#     problem_names = ["sat.txt","unsat.txt"]
#     for problem in problem_names:
#         try:
#             clause_set = load_dimacs(problem)
#             check = dpll_sat_solve(clause_set,[])
#             if problem == problem_names[1]:
#                 assert (not check)
#                 print("Test (UNSAT) passed")
#             else:
#                 assert check == [1,-2] or check == [-2,1]
#                 print("Test (SAT) passed")
#         except:
#             print("Failed problem " + str(problem))
#     print("Finished tests")