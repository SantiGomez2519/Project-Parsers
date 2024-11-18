from top_down_parser import *
from bottom_up_parser import *
from shared_data import *
from utils import *
from original_project import *


def menu_bonus():
    while True:
        print('\n------------------------------')
        print('1. Print FIRST and FOLLOW.')
        print('2. Top-Down Parser')
        print('3. Bottom-Up Parser')
        print('4. Print grammar')
        print('0. Exit')

        option = int(input('Choose an option: '))

        if option == 0:
            break
        
        # Print FIRST and FOLLOW
        elif option == 1:
            print('\n------------------------------')
            print_first_set()
            print_follow_set()

        # Top-Down Parser
        elif option == 2:
            while True:
                print('\n-----------------------------')
                print("1. Verify if the grammar is LL(1): ")
                print('2. Compute the FIRST of a string')
                print('3. Print parsing table')
                print('4. Parse a string')
                print('0. Exit')

                choice = int(input('Choose an option: '))

                if choice == 1:
                    is_LL1(grammar)
                elif choice == 2:
                    print("Enter the string to compute the FIRST: ")
                    string = input()
                    print(compute_first_of_string(string))
                elif choice == 3:
                    print_predicting_parsing_table(grammar)
                elif choice == 4:
                    print("Enter the string to be parsed: ")
                    w = input()
                    top_down_parser(grammar, w)
                elif choice == 0:
                    break
                else:
                    print("Invalid choice, please try again")

        # Bottom-Up Parser
        elif option == 3:
            while True:
                print('\n-----------------------------')
                print('1. Print the states of the LR(1) automaton')
                print('2. Print the SLR(1) parsing table')
                print('3. Parse a string')
                print('0. Exit')

                choice = int(input('Choose an option: '))

                if choice == 1:
                    print_states()
                elif choice == 2:
                    print_SLR_parsing_table(grammar)
                elif choice == 3:
                    print("Enter the string to be parsed: ")
                    w = input()
                    LR_parsing(grammar, w)
                elif choice == 0:
                    break
                else:
                    print("Invalid choice, please try again")
        
        elif option == 4:
            print_grammar(grammar)

        else:
            print("Invalid choice, please try again")

# Main function to run the program
def main():
    while True:
        print('\n-----------------------------------------------')
        print('Final Project - Formal Languages and Compilers')
        print('Santiago Gómez Ospina - Miguel Ángel Ortiz')
        print('-----------------------------------------------\n')

        print('1. Original Project')
        print('2. Bonus')
        print('3. Print grammar')
        print('0. Exit')

        option= int(input('Choose an option: '))        

        # Original Project
        if option == 1:
            print("Enter the number of cases: ")
            number_of_cases = int(input())
            for _ in range(number_of_cases):
                original_project_grammar = read_grammar()
                original_project(original_project_grammar)
        # Bonus
        elif option == 2:
            compute_first(grammar)
            compute_follow(grammar)
            menu_bonus()

        # Print grammar
        elif option == 3:
            print_grammar(grammar)
            
        elif option == 0:
            break
        else:
            print("Invalid choice, please try again")
            continue
    
if __name__ == "__main__":
    main()