from shared_data import *
from utils import *
from prettytable import PrettyTable

# Compute the first set of a string, considering the grammar
def compute_first_of_string(string):
    # Initialize the first set with the string and empty set
    first_of_string = {string: set()}

    # Flag to check if all symbols in the string can derive ε
    epsilon_in_all = True

    # Iterate over all symbols in the string
    for symbol in range(len(string)):
        # If the symbol is a terminal, add it to the FIRST set and stop
        if string[symbol] not in grammar:
            first_of_string[string].add(string[symbol])
            epsilon_in_all = False
            break

        # If the symbol is a non-terminal, add the FIRST set of the symbol to the FIRST set of the string without ε
        else:
            first_of_string[string] |= first[string[symbol]] - {'e'}
            if 'e' not in first[string[symbol]]:
                epsilon_in_all = False
                break
    # If all symbols in the string can derive ε, add ε to the FIRST set of the string
    if epsilon_in_all:
        first_of_string[string].add('e')
    return first_of_string

# Method to check if the grammar is LL(1)
def is_LL1(grammar):
    # Iterate over all non-terminals
    for non_terminal in grammar:
        # Create a list with the productions of the non-terminal as strings
        production_string = [''.join(production) for production in grammar[non_terminal]]

        # If there are more than one production in the non-terminal
        if len(production_string) > 1:
            # print(production_string)

            # Order the production at the form A -> α|β
            # With two iterators i and j, iterate over all productions per pairs checking all the possible cases to the conditions
            for i in range(len(production_string)):
                for j in range(i + 1, len(production_string)):
                    # First condition
                    # 1. First(α) ∩ First(β ) = 0.
                    if (compute_first_of_string(production_string[i])[production_string[i]] & compute_first_of_string(production_string[j])[production_string[j]]) != set():
                        print("Grammar is not LL(1)")
                        return False
                    
                    # Second condition
                    # 2. If e ∈ First(β), then First(α) ∩ Follow(A) = 0.
                    #    If e ∈ First(α), then First(β) ∩ Follow(A) = 0.
                    if 'e' in compute_first_of_string(production_string[j])[production_string[j]]:
                        if (compute_first_of_string(production_string[i])[production_string[i]] & follow[non_terminal]) != set():
                            print("Grammar is not LL(1)")
                            return False
                    if 'e' in compute_first_of_string(production_string[i])[production_string[i]]:
                        if (compute_first_of_string(production_string[j])[production_string[j]] & follow[non_terminal]) != set():
                            print("Grammar is not LL(1)")
                            return False
                        
    # If all conditions are satisfied, the grammar is LL(1)
    print("Grammar is LL(1)")
    return True

# Method to initialize the parsing table
def construct_table_M(grammar):
    nonterminals = []
    terminals = []
    for nonterminal in grammar:
        for production in grammar[nonterminal]:
            for symbol in production:
                if symbol not in grammar and symbol != 'e' and symbol not in terminals:
                    terminals.append(symbol)
        nonterminals.append(nonterminal)
    terminals.append('$')
    # print(nonterminals)
    # print(f"Terminals: {terminals}")
    table = [["-" for _ in range(len(terminals) + 1)] for _ in range(len(nonterminals) + 1)]
    for i in range(len(table)):
        for j in range(len(table[0])):
            if i == 0 and j == 0:
                table[i][j] = " "
            elif i == 0:
                table[i][j] = list(terminals)[j - 1]
            elif j == 0:
                table[i][j] = list(nonterminals)[i - 1]
    return table

# Method to construct the predicting parsing table following the algorithm                      
def predicting_parsing_table(grammar):
    # Initialize the table
    table = construct_table_M(grammar)

    # For each production A -> α do
    for non_terminal in grammar:
        for production in grammar[non_terminal]:
            # Compute the FIRST set of the production as a string
            first_of_production = compute_first_of_string(''.join(production))

            for symbol in first_of_production:
                # for every a ∈ First(α) do
                for a in first_of_production[symbol]:
                    # Add A -> α to the M[A, a] cell
                    if a != 'e':
                        row = next(i for i, row in enumerate(table) if row[0] == non_terminal)
                        column = table[0].index(a)
                        if table[row][column] == '-':
                            table[row][column] = ''.join(production)
                        else:
                            # If the grammar is not LL(1), add the production to the cell with a union operation
                            table[row][column] += ' | ' +''.join(production)
                    
                    # If ε ∈ First(α)
                    if 'e' in first_of_production[symbol]:

                        # for every b ∈ Follow(A) do
                        for b in follow[non_terminal]:
                            # Add A -> α to the M[A, b] cell
                            row = next(i for i, row in enumerate(table) if row[0] == non_terminal)
                            column = table[0].index(b)
                            if table[row][column] == '-':
                                table[row][column] = ''.join(production)
                            else:
                                # If the grammar is not LL(1), add the production to the cell with a union operation
                                table[row][column] += ' | ' + ''.join(production)

                    # If ε ∈ First(α) and $ ∈ Follow(A)
                    if 'e' in first_of_production[symbol] and '$' in follow[non_terminal]:
                        # Add A -> α to the M[A, $] cell
                        row = next(i for i, row in enumerate(table) if row[0] == non_terminal)
                        column = table[0].index('$')
                        if table[row][column] == '-':
                            table[row][column] = ''.join(production)
                        else:
                            table[row][column] = ''.join(production)
    return table

# Method to print the predicting parsing table using the PrettyTable library
def print_predicting_parsing_table(grammar):
    table = predicting_parsing_table(grammar)

    x = PrettyTable()
    x.field_names = table[0]
    for row in table[1:]:
        x.add_row(row)
    print(x)

# Method to parse a string using the predicting parsing algorithm
def predicting_parsing_algorithm(grammar, w):
    # Initialize the table with the predicting parsing table algorithm
    table = predicting_parsing_table(grammar)

    terminals = table[0][1:] # Terminals
    w += '$' # String
    T = ['S', '$'] # Stack
    X = T[0] # Top of the stack symbol

    # While the string hasn't been completely read
    while (X != '$'):
        # Print the string and the stack for each iteration
        print(f"String: {w}, Stack: {T}")

        # If the first symbol of the string is not a terminal of the grammar, return False
        if w[0] not in terminals:
            print("Error 3")
            return False
        
        # Find the cell M[X, a] in the table
        if X in grammar: # If the top of the stack is a non-terminal
            row = next(i for i, row in enumerate(table) if row[0] == X)
        column = table[0].index(w[0])
        # print(row, column)

        # if X is the first symbol of the string
        if X == w[0]:
            # print("Entré")
            T.pop(0)

            # Let a the next symbol of the string
            w = w[1:]
            a = w[0]

            # If a is a terminal not in grammar, return False
            if a not in terminals:
                print("Error 4")
                return False
            
            # Update the top of the stack symbol
            column = table[0].index(a)
            X = T[0]
            # print(T)
        
        # If X is a terminal, return False
        elif X not in grammar:
            print("Error 1")
            return False

        # If the cell M[X, a] is empty, return False
        elif table[row][column] == '-':
            print("Error 2")
            return False
        
        # If the cell M[X, a] contains a production X -> α1 α2 ... αn
        elif table[row][column] != '-':
            # Replace X with α1 α2 ... αn in the stack
            T.pop(0)

            # Add the symbols of the production to the stack
            for symbol in (table[row][column])[::-1]: # Reverse the production to add the symbols in the correct order
                if symbol != 'e':
                    T.insert(0, symbol)
            X = T[0]
            # print(T)

    if w == '$':
        return True
    else:
        return False # The string hasn't been completely read
             
# Method to parse a string using the top-down parser
def top_down_parser(grammar, w):
    # Check if the grammar is LL(1)
    grammar_is_LL1 = is_LL1(grammar)
    if not grammar_is_LL1:
        return
    
    # Parse the string using the predicting parsing algorithm
    syntax_analisis = predicting_parsing_algorithm(grammar, w)

    
    if syntax_analisis == True:
        print("String accepted")
    else:
        print("String not accepted")