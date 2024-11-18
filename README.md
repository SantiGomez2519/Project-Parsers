# Project Parsers

## Contents
- [Authors](#authors)
- [Description](#description)
- [Operating System and Programming Language](#operating-system-and-programming-language)
- [Running instructions](#running-instructions)

## Authors
- Santiago Gómez Ospina
- Miguel Ángel Ortiz Puerta

## Description
Final project of the course Formal Languages and Compilers, the original project consists of the design and implementation of the First and Follow algorithms for all non-terminal symbols of a given context-free grammar and the bonus consists in the implementation of the Top Down and Bottom Up Parsers.

## Operating System and Programming Language
**Operating System**
  - Windows 11 Pro
  - Linux ubuntu

**Programing language**
  - Python version 13.13.0


## Running instructions

**Requirement**

To run the program, you need to install the Pretty table library in your pyhton version for a correct output of the tables, to do this, open the terminal and type the following command:

```
 python3 -m pip install --upgrade pip
```

**Running**

To run the program, clone it on your local machine with the following command:

```
git clone <repository-url>
```

Then, enter into the folder of the project and run the main.py file, in case you want to run it by terminal you can execute the following command:

```
 python main.py
```

**Menu management**

***To choose an option from any of our menus, enter the number that accompanies the option***

**Example**

```
1. Print First
2. Print Follow
----------------
Choose option: 1

> Running: showing first...
```

**Executing the main.py file, the following menu will appear**

```
-----------------------------------------------
Choose a grammar for the bonus:
1. Read user grammar
2. Read grammar from file
Choose an option:
```

**Explanation**

- The function of this first menu is to choose how you want to get the grammar to be used in the parsers.
- In this menu you can choose if you want to enter a grammar readed from the user or one of the grammars available in the txt file.
- This grammar will be saved and left recursion will be removed if it has it.
- Once you choose an option and saved the grammar, continue to the following menu.
  
 ***Option 1 Read user grammar***
 
- 1.1 Enter the number of nonterminals your grammar will have.
  
- 1.2 Enter the grammar in the following format:
- nonterminal - derivation alternatives of the nonterminal separated by blank spaces -

**Example**

```
S AS A
A a
```

***Option 2 Read grammar from file***

**Example**

```
Gramática 17:
  S -> A a | b
  A -> B c | d
  B -> S r | f
----------------------------------------

Seleccione una gramática (1 - 17): 17
```

**Main Menu**

```
-----------------------------------------------
Final Project - Formal Languages and Compilers
Santiago Gómez Ospina - Miguel Ángel Ortiz
-----------------------------------------------

1. Original Project
2. Bonus
3. Print grammar
0. Exit
Choose an option:
```

**Explanation**
This menu show the main options of our code

***Original Project***

To use the original project option to calculate the First and Follow of a given grammars, these are the steps:

- Enter the number of cases (understood as the number of grammars you are going to enter).

```
  -----------------------------------------------
Final Project - Formal Languages and Compilers
Santiago Gómez Ospina - Miguel Ángel Ortiz
-----------------------------------------------

1. Original Project
2. Bonus
3. Print grammar
0. Exit
Choose an option: 1
Enter the number of cases: 2
```


- Enter the number of nonterminals for your first graph:

```
Number of non-terminals: 2
``` 

- Enter the grammar to be parsed with the following structure:
\<non-terminal> \<non-terminal derivation alternatives separated by blanks spaces>

```
S aA
A l
```

- You will be shown the first and follow of the entered grammar, repeat step 2 and 3 many times as you have entered the number of cases. 

***Bonus***

```
  -----------------------------------------------
Final Project - Formal Languages and Compilers
Santiago Gómez Ospina - Miguel Ángel Ortiz
-----------------------------------------------

1. Original Project
2. Bonus
3. Print grammar
0. Exit
Choose an option: 2

```

Choosing the bonus option you will be directed to the following menu:

```
------------------------------
1. Print FIRST and FOLLOW.
2. Top-Down Parser
3. Bottom-Up Parser
4. Print grammar
0. Exit
```

**Print FIRST and Follow**.

The chosen grammar is displayed
  
**Top-Down Parser**

In this option you can do everything related to the Top Down Parser, follow the steps of each of the options:

```
1. Verify if the grammar is LL(1):
2. Compute the FIRST of a string
3. Print parsing table
4. Parse a string
0. Exit
```
**Bottom-Up Parser**
  
In this option you can do everything related to the Bottom.Up Parser.

```
-----------------------------
1. Print the states of the LR(1) automaton
2. Print the SLR(1) parsing table
3. Parse a string
0. Exit
```

**Print grammar**
The chosen grammar for the bonus is displayed.


## Project Structure

#### The project is divided into the following files:
 
- `bottom_up_parser.py` and `top_down_parser.py` contain the necessary functions for managing their respective parsers, from implementation to table printing and string analysis.

- `grammars.txt` contains grammars that can be analyzed by the parsers or used to compute the `FIRST` and `FOLLOW` sets.

- `shared_data.py` serves as a global file for the rest of the files. It loads grammars from `grammars.txt`, reads and configures grammars entered by the user into a structure compatible with the functions in other files, and includes a global function that other files can use to implement necessary functions for grammar creation and manipulation. Additionally, it eliminates left recursion in this file.

- `original_project.py` contains essential functions for the original project.

- `utils.py` contains functions related to computing the FIRST and FOLLOW sets implemented for the grammar chosen in the bonus.

- `main.py` is the main file that starts the program, allowing the user to either run the original project or use the parsers for the bonus.

#### Explanation of fuctions:
***bottom_up_parser.py***

- `closure`: Performs the closure of the kernel with symbols next to the dot for the given production.
- `goto`: Generates new states by simulating the movement of the dot to the right.
- `initialize_items_set`: Initializes the set of items for each production in the grammar, placing a dot in every possible position.
- `sets_of_items`: Builds the canonical collection of LR(0) item sets from an augmented grammar.
- `initialize_parsing_table`: Initializes a parsing table with rows for each state and columns for each terminal and non-terminal symbol.
- `SLR_parsing_table`: Generates an SLR(1) parsing table using the item sets and FOLLOW sets of the grammar.
- `print_SLR_parsing_table`: Prints the generated SLR(1) parsing table using the PrettyTable library.
- `LR_parsing`: Implements the LR parsing process using the parsing table to verify if an input string is accepted.
- `print_states`: Prints the states generated in the LR(0) item sets collection for the grammar.
  
***top_down_parser.py***

- `compute_first_of_string`: Calculates the FIRST set of a specific string in the grammar, considering the presence of epsilon (empty production).
- `is_LL1`: Checks if the grammar is LL(1) by verifying uniqueness conditions in the FIRST set and the relationship between FIRST and FOLLOW.
- `construct_table_M`: Builds an initial empty table for predictive parsing, with rows for non-terminals and columns for terminals.
- `predicting_parsing_table`: Fills the predictive parsing table using the FIRST and FOLLOW sets of the grammar's productions.
- `print_predicting_parsing_table`: Prints the generated predictive parsing table, using the PrettyTable library for formatting.
- `predicting_parsing_algorithm`: Implements the predictive parsing algorithm, processing an input string and verifying if it is accepted by the grammar.
- `top_down_parser`: Executes top-down parsing; first checks if the grammar is LL(1), then uses the predictive parsing algorithm to evaluate the input string..

***shared_data.py***

- `load_grammars`: Loads multiple grammars from grammars.txt and converts them into interpretable data structures.
- `print_grammar`: Prints a given grammar in a readable format, displaying alternative productions separated by |.
- `choose_grammar`: Displays the list of available grammars and allows the user to select one for use.
- `grammar_from_file`: Loads a grammar from grammars.txt and lets the user select one.
- `configure_grammar`: Reconfigures a given grammar by breaking down each production into individual symbols and eliminating left recursion.
- `read_grammar`: Allows the user to enter a grammar from the console, then configures it for use.
- `eliminate_left_recursion_general`: Eliminates general left recursion from a grammar, processing each non-terminal in order.
- `eliminate_immediate_left_recursion`: Eliminates immediate left recursion in a specific non-terminal, creating a new non-terminal if necessary.
- `global_grammar`: Allows the user to select a grammar, either by entering it manually or loading it from a file, and removes any left recursion.

***original_project.py***

- `original_project`: Initializes the grammar and calculates the FIRST and FOLLOW sets, then prints and clears them.
- `compute_first_project`: Calculates the FIRST set for each non-terminal in the grammar, using an auxiliary function to handle productions.
- `compute_first_util_project`: Auxiliary function that calculates the FIRST set for a specific non-terminal, considering each symbol in its productions and the rules for ε.
- `compute_follow_project`: Calculates the FOLLOW set for each non-terminal in the grammar, iterating until the FOLLOW sets stabilize.
- `compute_follow_util_project`: Auxiliary function that applies the rules for calculating the FOLLOW set, including adding FIRST symbols and handling ε.
- `print_first_set_project`: Prints the FIRST set of each non-terminal, displaying elements without quotes.
- `print_follow_set_project`: Prints the FOLLOW set of each non-terminal, also displaying elements without quotes.


***utils\.py***

- `compute_first`: Calculates the FIRST set for each non-terminal in the grammar, using an auxiliary function to process productions.
- `compute_first_util`: Auxiliary function that calculates the FIRST set for a specific non-terminal, following the rules for ε derivation and terminals.
- `compute_follow`: Calculates the FOLLOW set for each non-terminal in the grammar, starting with the start symbol and repeating until the FOLLOW sets stabilize.
- `compute_follow_util`: Auxiliary function that applies the rules for calculating the FOLLOW set, adding FIRST elements and handling derivations that contain ε.
- `print_first_set`: Prints the FIRST set of each non-terminal, displaying elements without quotes.
- `print_follow_set`: Prints the FOLLOW set of each non-terminal, also displaying elements without quotes.

***main\.py***

- `menu_bonus`: Displays the menu related to the bonus features.
- `main`: The main function that displays the primary menu.
