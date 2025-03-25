def load_dimacs(file_name):
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

def branching_sat_solve(clause_set, partial_assignment):
    branch = None
    for clause in clause_set:
        for literal in partial_assignment:
            if literal in clause:
                break
        else:
            branch = clause
            break
    if branch is None:
        return partial_assignment
    chosen_var = None
    for literal in branch:
        if (literal * -1 not in partial_assignment) and (literal not in partial_assignment):
            chosen_var = literal
            break
    if chosen_var is None:
        return False
    new_assignment = partial_assignment + [chosen_var]
    result = branching_sat_solve(clause_set, new_assignment)
    if result:
        return result
    new_assignment = partial_assignment + [-chosen_var]
    return branching_sat_solve(clause_set, new_assignment)

def unit_propagate(clause_set):
    no_unit_clause = False
    while no_unit_clause == False:
        for clause in clause_set:
            if len(clause) == 1:
                unit = clause[0]
                break
        else:
            no_unit_clause = True
        c = 0
        while c < len(clause_set) and no_unit_clause == False:
            if unit in clause_set[c]:
                clause_set.pop(c)
                c -= 1
            elif (unit * -1) in clause_set[c]:
                clause_set[c].remove((unit * -1))
            c += 1
    return clause_set

def dpll_sat_solve(clause_set,partial_assignment):
    def unit_propagate(temp_clause_set):
        temp_clause_set = [clause[:] for clause in temp_clause_set]
        true_assignments = []
        no_unit_clause = False
        while no_unit_clause == False:
            for clause in temp_clause_set:
                if len(clause) == 1:
                    unit = clause[0]
                    true_assignments.append(unit)
                    break
            else:
                no_unit_clause = True
            c = 0
            while c < len(temp_clause_set) and no_unit_clause == False:
                if unit in temp_clause_set[c]:
                    temp_clause_set.pop(c)
                    c -= 1
                elif (unit * -1) in temp_clause_set[c]:
                    temp_clause_set[c].remove((unit * -1))
                c += 1
        return temp_clause_set, true_assignments
    if clause_set == []:
        return partial_assignment
    elif [] in clause_set:
        return False    
    new_clause_set, new_assignments = unit_propagate(clause_set)
    if new_assignments != []:
        return dpll_sat_solve(new_clause_set, partial_assignment + new_assignments)
    new_clause_set.append([new_clause_set[0][0]])
    branch = dpll_sat_solve(new_clause_set, partial_assignment)
    if branch:
        return branch
    new_clause_set.pop()
    new_clause_set.append([(new_clause_set[0][0] * -1)])
    branch = dpll_sat_solve(new_clause_set, partial_assignment)
    return branch