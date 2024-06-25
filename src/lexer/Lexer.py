"""
Grammar:

E => T
    | T + E
    | T - E
T => int
    | T * T
    | T / T
    |(E)

    5 + 3
    625 / 5
    6 - 3 * 8
    (3 + 5) * 10

Tokens:
name <id, type>

keywords < if | while | for | else | let | in , keywords >
identifiers < \s (different from keywords and start with a letter), ID >
numbers : < %d , num >
open_p : < ( , open_p >
close_p : < ) , close_p >
binary operators : < + | - | * | / | ^ | @ , b_op >
constants: < PI | E , const >



"""


class Token:
    def __init__(self, key, type):
        self.key = key
        self.type = type

    def __str__(self):
        return self.key


class Lexer:
    def __init__(self, program):
        self.next_token = 0
        self.keywords = ["if", "while", "for", "else", "let", "in", 'PI', 'E']
        self.Tokens = self.tokenize(program)

    def tokenize(self, program: str):

        """

        This method tokenizes the input program string into a list of Token objects.

        Parameters:
        program (str): The input program string to be tokenized.

        Returns:
        list: A list of Token objects representing the tokenized program.

        """

        # Initialize an empty list to store the tokens
        Tokens = []

        # Loop through the program string until the end is reached
        while self.next_token < program.__len__():
            # Get the current character
            char = program[self.next_token]

            # Match the current character to its corresponding token type
            match char:
                case ' ':
                    # Ignore spaces
                    pass
                case '+':
                    # Append a binary operator token for '+'
                    Tokens.append(Token(char, "b_op"))
                case '-':
                    # Append a binary operator token for '-'
                    Tokens.append(Token(char, "b_op"))
                case '*':
                    # Append a binary operator token for '*'
                    Tokens.append(Token(char, "b_op"))
                case '/':
                    # Append a binary operator token for '/'
                    Tokens.append(Token(char, "b_op"))
                case '^':
                    Tokens.append(Token(char, "b_op"))
                case '@':
                    Tokens.append(Token(char, "b_op"))
                case '(':
                    # Append an open parenthesis token
                    Tokens.append(Token(char, "open_p"))
                case ')':
                    # Append a close parenthesis token
                    Tokens.append(Token(char, "close_p"))

                case _ if char.isalpha() and not char.isdigit():
                    # Initialize an empty string for the identifier
                    id = ""
                    # Loop through the program string until a non-alphabetic character is reached
                    while (char.isalpha() or char.isdigit()) and self.next_token < program.__len__():
                        # Append the current character to the identifier
                        id += char
                        # Move to the next character
                        self.next_token += 1

                        if self.next_token < program.__len__():
                            char = program[self.next_token]

                    # If the identifier is a keyword, append a keyword token
                    if id in self.keywords:
                        Tokens.append(Token(id, "keyword"))
                    # Append an identifier token
                    else:
                        Tokens.append(Token(id, "ID"))
                    continue

                # Identify digits only
                case _ if char.isdigit():
                    # Initialize an empty string for the number
                    num = ""
                    # Loop through the program string until a non-digit character is reached
                    while char.isdigit() and self.next_token < program.__len__():
                        # Append the current character to the number
                        num += char

                        # Move to the next character
                        self.next_token += 1

                        if self.next_token < program.__len__():
                            char = program[self.next_token]
                    # Append a number token
                    Tokens.append(Token(num, "num"))
                    continue
                case _:
                    # Print a syntax error message for unrecognized characters
                    exception = f"Syntax Error: Unrecognized character '{char}'"
                    raise Exception(exception)
            # Move to the next character
            self.next_token += 1

        # Return the list of tokens
        return Tokens


string = "aa2adf3asd(fad)345*E"
Lexer = Lexer(string)

for item in Lexer.Tokens:
    print(item)
