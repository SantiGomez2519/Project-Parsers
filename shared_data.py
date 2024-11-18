# Description: This file contains the shared data between the different files of the project.
# The shared data includes the first and follow sets of the grammar, the grammar itself, and the methods to compute the first and follow sets.

# We used AI to extract the grammar from a txt file and to the input of the user to get the grammar in the format required by the project

import random
import string
import ast

# Load grammars from a file
def load_grammars(filename):
    # Initialize list of grammars
    grammars = []

    # Read grammars from file
    with open(filename, 'r') as file:
        current_grammar = ""
        for line in file:
            line = line.strip()
            if line.startswith("#"):  # Nueva gramática
                if current_grammar:
                    grammars.append(ast.literal_eval(current_grammar))
                    current_grammar = ""
            else:
                current_grammar += line
        if current_grammar:
            grammars.append(ast.literal_eval(current_grammar))
    return grammars

def print_grammar(grammar):
    for non_terminal, productions in grammar.items():
        print(f"  {non_terminal} -> ", end="")
        formatted_productions = [" ".join(prod) for prod in productions]
        print(" | ".join(formatted_productions))

def choose_grammar(grammars):
    print("\nLista de gramáticas disponibles:")
    for i, grammar in enumerate(grammars):
        print(f"Gramática {i + 1}:")
        print_grammar(grammar)
        print("-" * 40)
    
    # Seleccionar gramática
    while True:
        try:
            choice = int(input(f"\nSeleccione una gramática (1 - {len(grammars)}): ")) - 1
            if 0 <= choice < len(grammars):
                return grammars[choice]
            else:
                print("Selección fuera de rango, intente nuevamente.")
        except ValueError:
            print("Entrada inválida, intente nuevamente.")

def grammar_from_file():
    # Cargar gramáticas
    filename = "grammars.txt"
    grammars = load_grammars(filename)

    # Permitir que el usuario elija una gramática
    selected_grammar = choose_grammar(grammars)
    
    return selected_grammar


# Methos to configure the grammar in the format required by the project
def configure_grammar(input_grammar):
    new_grammar = {}
    
    # Iterate over the input grammar
    for key, productions in input_grammar.items():
        new_productions = []
        
        for production in productions:
            # Join the production into a single string
            combined = ''.join(production)

            # Split the production into a list of symbols individually
            new_production = list(combined)
            new_productions.append(new_production)

        # Add the new production to the new grammar
        new_grammar[key] = new_productions
    
    return eliminate_left_recursion_general(new_grammar)

def read_grammar():
    # Number of non_terminals
    num_non_terminals = int(input())
    
    # Initialize the grammar dictionary
    grammar = {}
    
    print()

    # Read the productions for each non-terminal
    for _ in range(num_non_terminals):
        # Read the line and split it into the non-terminal and its productions
        line = input().strip().split()

        # Get the non-terminal and its productions
        non_terminal = line[0]
        productions = line[1:]
        
        # Add the production to the grammar
        grammar[non_terminal] = [[production] for production in productions]
    
    return configure_grammar(grammar)

# Method to eliminate left recursion
def eliminate_left_recursion_general(grammar):
    non_terminals_array = list(grammar.keys())
    new_grammar = grammar.copy()

    for i in range(len(non_terminals_array)):
        Ai = non_terminals_array[i]
        
        for j in range(i):  # Para cada no terminal anterior Aj
            Aj = non_terminals_array[j]
            new_productions = []

            # Reemplazar A_i -> A_jα por A_i -> δα donde A_j -> δ
            for production in new_grammar[Ai]:
                if production[0] == Aj:  # Si Ai -> Ajα
                    for production2 in new_grammar[Aj]:  # Para cada Aj -> δ
                        new_productions.append(production2 + production[1:])  # Reemplazar con δα
                else:
                    new_productions.append(production)

            # Actualizar las producciones de Ai con las nuevas producciones
            new_grammar[Ai] = new_productions

        # Eliminar recursión inmediata de Ai después de procesar los Aj anteriores
        result = eliminate_immediate_left_recursion(new_grammar, Ai, non_terminals_array)
        new_grammar.update(result)  # Actualizar la gramática completa con el resultado

    return new_grammar

def eliminate_immediate_left_recursion(grammar, non_terminal, non_terminals_array):
    recursive_productions = []
    non_recursive_productions = []
    
    # Separar producciones recursivas y no recursivas
    for production in grammar[non_terminal]:
        if production[0] == non_terminal:
            recursive_productions.append(production[1:])
        else:
            non_recursive_productions.append(production)
    
    # Si hay producciones recursivas, eliminarlas
    if recursive_productions:
        # Elegir una letra no utilizada para el nuevo no terminal
        while True:
            aleatory_non_terminal = random.choice(string.ascii_uppercase)
            if aleatory_non_terminal not in non_terminals_array:
                new_non_terminal = aleatory_non_terminal
                non_terminals_array.append(new_non_terminal)  # Agregar a la lista para evitar reutilización
                break

        grammar_without_lr = {
            non_terminal: [],
            new_non_terminal: []
        }


        for production in non_recursive_productions:
            grammar_without_lr[non_terminal].append(production + [new_non_terminal])

        for production in recursive_productions:
            grammar_without_lr[new_non_terminal].append(production + [new_non_terminal])

        # Añadir producción epsilon para el nuevo no terminal
        grammar_without_lr[new_non_terminal].append(['e'])
    else:
        # Si no hay recursión, retornar las producciones originales
        grammar_without_lr = {non_terminal: grammar[non_terminal]}

    return grammar_without_lr


# Method to choice the grammar for the bonus (required by the all files to work the project)
def global_grammar():
    print('\n-----------------------------------------------')
    print('Choose a grammar for the bonus:')
    print('1. Read user grammar at the format required by the project')
    print('2. Read grammar from file')

    if input('Choose an option: ') == '1':
        grammar = read_grammar()
        
    else:
        grammar = grammar_from_file()
        grammar= eliminate_left_recursion_general(grammar)
      
    return grammar

grammar = global_grammar()

# Initialize the global first and follow sets for the bonus project
first = {non_terminal: set() for non_terminal in grammar}
follow = {non_terminal: set() for non_terminal in grammar}