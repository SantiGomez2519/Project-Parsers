from prettytable import PrettyTable
from shared_data import *
from utils import *

# Compute the closure of an item set
def closure(grammar, item_set):
    # Copy the item set to check if it changes
    J = item_set.copy()
    while True:
        # Copy the item set to check if it changes
        prev_J = J.copy()
        
        # Iterate over all items in the item set
        for item in J.copy():
            # For each item A -> α•Bβ in J
            if '•' in item:
                # Split the item in the non-terminal, the production, and the part after the dot
                item_splitted = item.split(' -> ')
                non_terminal = item_splitted[0]
                production = item_splitted[1]
                after_dot = production.split('•')[1]
                
                # If B is a non-terminal
                if len(after_dot) > 0 and after_dot[0] in grammar:
                    # For each production B -> γ
                    for production in grammar[after_dot[0]]:

                        # If the production is epsilon, add the item B -> • to J
                        if 'e' in production:
                            new_item = f"{after_dot[0]} -> •"

                        # Add the item B -> •γ to J
                        else:
                            new_item = f"{after_dot[0]} -> •{''.join(production)}"

                        # Add the new item to J if it is not already in J
                        if new_item not in J:
                            # print(f"J before add: {J}, new item: {new_item}")
                            J.append(new_item)

        # If the item set doesn't change, stop
        if prev_J == J:
            break
    return J

# Compute the goto of an item set
def goto(grammar, items, symbol):
    # Initialize the new state
    new_state = []

    # Iterate over all items in the item set
    for item in items:
        if '•' in item:
            nonterminal, production = item.split(" -> ")
            dot_pos = production.index('•')
            
            # Check if the symbol is after the dot
            if dot_pos + 1 < len(production) and production[dot_pos + 1] == symbol:

                # Create the new production with the dot moved one position to the right
                new_production = production[:dot_pos] + symbol + '•' + production[dot_pos + 2:]

                new_state.append(f"{nonterminal} -> {new_production}")
    
    # Compute the closure of the new state
    if new_state:
        return closure(grammar, new_state)
    return []

# Method to create all the possible items of the grammar
# def initialize_items_set(grammar):
#     items = []
#     for non_terminal in grammar:
#         for production in grammar[non_terminal]:
#             print(production)
#             for i in range(len(production) + 1):
#                 if 'e' in production:
#                     item = (f"{non_terminal} -> •")
#                     items.append(item)
#                 else:
#                     dot = production[:i] + ['•'] + production[i:]
#                     item = (f"{non_terminal} -> {''.join(dot)}")
#                     items.append(item)
#     return items
    

# CANONICAL COLLECTION OF LR(0) ITEMS (States of the LR(0) automaton)
def sets_of_items(grammar):
    # Create the augmented grammar
    augmented_grammar = {'S\'': [['S']]}
    for non_terminal in grammar:
        augmented_grammar[non_terminal] = grammar[non_terminal]

    # Create the initial state of the canonical collection of LR(0) items
    C = [closure(augmented_grammar, ["S' -> •S"])]

    # Create a set with all the symbols of the grammar
    all_symbols = set()
    for non_terminal in grammar:
        all_symbols.add(non_terminal)
        for production in grammar[non_terminal]:
            for symbol in production:
                all_symbols.add(symbol)
                
    while True:
        # Copy the item set to check if it changes
        prev_C = C.copy()

        # Iterate over all the states in the canonical collection of LR(0) items
        for item_set in C:
            # For each symbol in the grammar
            for symbol in all_symbols:
                # Compute the goto of the item set with the symbol (new state)
                goto_result = goto(augmented_grammar, item_set, symbol)

                # If the goto is not empty and not already in C, add it to C
                if goto_result and goto_result not in C:
                    C.append(goto_result)
        if prev_C == C:
            break
    return C


# Method to initialize the parsing table
def initialize_parsing_table(grammar):
    nonterminals = []
    terminals = []
    states = sets_of_items(grammar)
    
    for nonterminal in grammar:
        for production in grammar[nonterminal]:
            for symbol in production:
                if symbol not in grammar and symbol != 'e':
                    if symbol not in terminals:
                        terminals.append(symbol)
        nonterminals.append(nonterminal)
    terminals.append('$')

    table_row = terminals + nonterminals

    table = [["-" for _ in range(len(table_row) + 1)] for _ in range(len(states) + 1)]

    for i in range(len(table)):
        for j in range(len(table[0])):
            if i == 0 and j == 0:
                table[i][j] = "STATES"
            elif i == 0:
                table[i][j] = list(table_row)[j - 1]
            elif j == 0:
                table[i][j] = i - 1
    return table
    

# Method to construct the SLR parsing table
def SLR_parsing_table(grammar):
    # Compute the canonical collection of LR(0) items
    C = sets_of_items(grammar)

    # Initialize the parsing table
    table = initialize_parsing_table(grammar)

    # Compute the FOLLOW sets
    follow = compute_follow(grammar)

    # Flag to check if the grammar is SLR(1)
    grammar_is_SLR = True

    # Iterate over all states in the canonical collection of LR(0) items
    for state_number, states in enumerate(C):
        # For each item A -> α•β in Ii
        for state in states:
            # Split the production in the non-terminal and the production
            dot_index = state.index('•')
            nonterminal = state.split(' -> ')[0]
            production = ''.join(state.split(' -> ')[1].split('•'))

            # If A → α•aβ ∈ Ii , with a ∈ Σ and GoTo(Ii , a) = Ij , then Action(i, a) ← “shift j”
            if dot_index < len(state) - 1 and state[dot_index + 1] not in grammar:
                new_goto = goto(grammar, states, state[dot_index + 1])
                if new_goto != None:
                    row = next(i for i, row in enumerate(table) if row[0] == state_number)
                    column = table[0].index(state[dot_index + 1])
                    table[row][column] = f"shift {C.index(new_goto)}"
                
            # If A → α• ∈ Ii with A != S' , then Action(i, a) ← “reduce A → α” for all a ∈ Follow(A)
            if dot_index == len(state) - 1 and nonterminal != 'S\'':
                for a in follow[nonterminal]:
                    # Find the row and column of the cell in the parsing table
                    row = next(i for i, row in enumerate(table) if row[0] == state_number)
                    column = table[0].index(a)

                    if table[row][column] == '-':
                        if production == '':
                            table[row][column] = f"reduce {nonterminal} -> e"
                        else:
                            table[row][column] = f"reduce {nonterminal} -> {production}"  
                    else:
                        # If the grammar has a shift/reduce conflict (not SLR(1)), add the production to the cell with a union operation
                        if production == '':
                            table[row][column] += f"/ reduce {nonterminal} -> e"
                        else:
                            table[row][column] += f"/ reduce {nonterminal} -> {production}"
                        grammar_is_SLR = False                      
            if 'S\' -> S•' in state:
                row = next(i for i, row in enumerate(table) if row[0] == state_number)
                column = table[0].index('$')
                table[row][column] = 'accept'

            # If GOTO(Ii , A) = Ij , then Goto(i, A) <- j
            for nonterminal in grammar:
                nonterminal_goto = goto(grammar, states, nonterminal)
                if nonterminal_goto != []:
                    row = next(i for i, row in enumerate(table) if row[0] == state_number)
                    column = table[0].index(nonterminal)
                    table[row][column] = C.index(nonterminal_goto)

    if grammar_is_SLR:
        print("Grammar is SLR(1)")
        return table, True
    else:
        print("The grammar is not SLR(1)")
        return table, False


# Method to print the SLR parsing table using PrettyTable library
def print_SLR_parsing_table(grammar):
    data, is_SLR0 = SLR_parsing_table(grammar)

    # Comprobe if the data is valid
    if not data or len(data) < 2:
        return

    # Set the headers of the table
    headers = data[0]  
    table = PrettyTable()
    table.field_names = headers

    for row in data[1:]:
        table.add_row(row)

    # Imprime la tabla
    print(table)

# Method to parse a string using the SLR parsing algorithm
def LR_parsing(grammar, w):
    # Compute the SLR parsing table
    table, is_SLR0 = SLR_parsing_table(grammar)

    # If the grammar is not SLR(1), stop
    if not is_SLR0:
        return False
    
    # Initialize the stack and the input string
    T = [0, '$']
    w+= '$'

    # First character of the input string
    a = w[0] 

    # Get a list of terminals
    terminals = table[0][1:len(table[0]) - len(grammar)]

    # Iterate over the parsing table
    while True:
        # If the first character of the input string is not a valid terminal, stop
        if a not in terminals:
            print("String not accepted")
            return False
        
        # Let s be the state at the top of the stack
        s = T[0]

        # Print the string and the stack for each iteration
        print(f"string: {w}, stack: {T}")

        # Find the cell ACTION[s, a] in the table
        row = next(i for i, row in enumerate(table) if row[0] == s)
        column = table[0].index(a)

        # If the ACTION[s, a] = shift t (t is the temporary top of the stack)
        if 'shift' in table[row][column]:
            # Split the string to get the state number
            shift_state = int(table[row][column].split(' ')[1])

            # Push the state to the stack
            T.insert(0, shift_state)

            # Let a be the next input symbol of the string
            w = w[1:]
            a = w[0]

        # If the ACTION[s, a] = reduce A -> β
        elif 'reduce' in table[row][column]:
            # Split the string to get the non-terminal and the production
            nonterminal = table[row][column].split('reduce ')[1].split(' -> ')[0]
            production = table[row][column].split(' -> ')[1]

            # Pop |β| symbols of the stack
            if production != 'e': # If the production is epsilon, don't pop anything
                for i in range(len(production)):
                    T.pop(0)

            t = T[0] # Temporary top of the stack

            # Find the cell GOTO[t, A] in the table
            row = next(i for i, row in enumerate(table) if row[0] == t)
            column = table[0].index(nonterminal)

            # Push GOTO[t, A] to the stack
            T.insert(0, int(table[row][column]))

        # If the ACTION[s, a] = accept
        elif table[row][column] == 'accept':
            print("String accepted")
            return True
        else:
            print("String not accepted")
            return False

# Method to print the states of the LR(0) automaton
def print_states():
    C = sets_of_items(grammar)
    for state_number, item_set in enumerate(C):
        print(f"State {state_number}:")
        for item in item_set:
            print("  ", item)
        print()