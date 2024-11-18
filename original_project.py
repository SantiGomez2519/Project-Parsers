# This is a file that contains the main program of the project (First and Follow Sets of many grammars as the input required)

# Method to compute and print the first and follow sets of a given grammar
def original_project(grammar):
    # Compute the first and follow sets
    first_project = compute_first_project(grammar)
    follow_project = compute_follow_project(grammar, first_project)

    # Print the first and follow sets
    print_first_set_project(first_project)
    print_follow_set_project(follow_project)

    # Clear the first and follow sets to avoid conflicts of many grammars
    first_project.clear()
    follow_project.clear()


# Compute the first set
def compute_first_project(grammar):
    # Initialize the first set with the nonterminals and empty set
    first_project = {non_terminal: set() for non_terminal in grammar}

    # Iterate to compute the first all non-terminals
    for non_terminal in grammar:
        # If the first set of the non-terminal is not computed, compute it
        if not first_project[non_terminal]:
            compute_first_util_project(non_terminal, grammar, first_project)
    return first_project

# Compute the first set of a non-terminal
def compute_first_util_project(non_terminal, grammar, first_project):
    # Iterate over all productions of the non-terminal
    for production in grammar[non_terminal]:
        epsilon_in_all = True # Flag to check if all symbols in the production can derive ε

        for first_symbol in production:
            # If the production is ε, add it to the FIRST set and stop
            if first_symbol == 'e':  
                first_project[non_terminal].add('e')
                epsilon_in_all = False  # It contains an explicit ε, so stop
                break

            # If it's a terminal, add it to the FIRST set and stop
            if first_symbol not in grammar:
                first_project[non_terminal].add(first_symbol)
                epsilon_in_all = False  # It's a terminal, so stop
                break

            else:
                # If the FIRST set of the symbol is not computed, compute it calling the function recursively
                if not first_project[first_symbol]:
                    compute_first_util_project(first_symbol, grammar, first_project)
                # Add the FIRST set of the symbol to the FIRST set of the non-terminal
                first_project[non_terminal] = first_project[non_terminal].union(first_project[first_symbol] - {'e'})

                # If ε is not in the FIRST set of the symbol, stop
                if 'e' not in first_project[first_symbol]:
                    epsilon_in_all = False
                    break

        # If all symbols in the production can derive ε (epsilon_in_all flag is still True), add ε to the FIRST set of the non-terminal
        if epsilon_in_all:
            first_project[non_terminal].add('e')
    return first_project

# Compute the follow set
def compute_follow_project(grammar, first_project):
    # Initialize the follow set with the nonterminals and empty set
    follow_project = {non_terminal: set() for non_terminal in grammar}
    follow_project['S'].add('$')  # Start symbol FOLLOW set
    
    # Iterate over all non-terminals until no changes
    while True:
        # Copy the follow set to check if it changes
        prev_follow = {key: value.copy() for key, value in follow_project.items()}

        # Compute the follow set of all non-terminals
        for non_terminal in grammar:
            compute_follow_util_project(non_terminal, grammar, follow_project, first_project)

        # If the follow set doesn't change, stop
        if prev_follow == follow_project: 
            break
    return follow_project

# Compute the follow set of a non-terminal
def compute_follow_util_project(non_terminal, grammar, follow_project, first_project):
    # Algorithm to compute the FOLLOW set
    # For each production A -> αBβ
    # Add FIRST(β) - {ε} to FOLLOW(B)
    # If β -> ε, add FOLLOW(A) to FOLLOW(B)
    # If there is a production A -> αB
    # Add FOLLOW(A) to FOLLOW(B)

    # Iterate over all productions of the non-terminal
    for key in grammar:
        for production in grammar[key]:
            for i in range(len(production)):
                if production[i] == non_terminal:
                    # Case: A -> αB (B is the last symbol)
                    if i == len(production) - 1:
                        # Add FOLLOW(A) to FOLLOW(B) with a UNION operation
                        follow_project[non_terminal] |= follow_project[key]
                    else:
                        # Case: A -> αBβ (B is followed by β)
                        for j in range(i + 1, len(production)):
                            # Get the next symbol of the non-terminal we are iterating
                            next_symbol = production[j]

                            # If the next symbol is a terminal, add it to the FOLLOW set and stop
                            if next_symbol not in grammar:
                                follow_project[non_terminal].add(next_symbol)
                                break

                            # If the next symbol is a non-terminal
                            follow_project[non_terminal] |= first_project[next_symbol] - {'e'}

                            # If ε is not in the FIRST set of the next symbol, stop
                            if 'e' not in first_project[next_symbol]:
                                break
                        # If the next symbol is the last symbol and it can derive ε, add FOLLOW(A) to FOLLOW(B)
                        else:
                            follow_project[non_terminal] |= follow_project[key]  # If β -> ε

def print_first_set_project(first_project):
    # print("\nFirst Set:")
    
    for non_terminal in first_project:
        # Store the elements of the first set in a string to print in the required format
        elements = ", ".join(first_project[non_terminal])  
        print(f"First({non_terminal}): {{{elements}}}")

def print_follow_set_project(follow_project):
    # print("\nFollow Set:")

    for non_terminal in follow_project:
        # Store the elements of the follow set in a string to print in the required format
        elements = ", ".join(follow_project[non_terminal])
        print(f"Follow({non_terminal}): {{{elements}}}")