import re
from enum import Enum

class TokenType(Enum):
    # Basic token types for our language
    KEYWORD = 1
    IDENTIFIER = 2
    INTEGER = 3
    STRING = 4
    END_OF_TOKENS = 5
    PUNCTUATION = 6
    OPERATOR = 7

class MyToken:
    def __init__(self, token_type, value):
        # Make sure we get a valid token type
        if not isinstance(token_type, TokenType):
            raise ValueError("token_type must be an instance of TokenType enum")
        self.type = token_type
        self.value = value

    # Simple getters
    def get_type(self):
        return self.type

    def get_value(self):
        return self.value
    
    def __repr__(self):
        # Helpful for debugging
        return f"{self.type.name}:'{self.value}'"

def tokenize(input_str):
    tokens = []
    # All the patterns we'll look for
    patterns = {
        'COMMENT': r'//.*',  # Comments start with // and go to end of line
        'KEYWORD': r'(let|in|fn|where|aug|or|not|gr|ge|ls|le|eq|ne|true|false|nil|dummy|within|and|rec)\b',
        'STRING': r'\'(?:\\\'|[^\'])*\'',  # Strings with quotes
        'IDENTIFIER': r'[a-zA-Z][a-zA-Z0-9_]*',  # Variable names
        'INTEGER': r'\d+',  # Numbers
        'OPERATOR': r'[+\-*<>&.@/:=~|$\#!%^_\[\]{}"\'?]+',  # Math and other operators
        'SPACES': r'[ \t\n]+',  # Whitespace to skip
        'PUNCTUATION': r'[();,]'  # Special characters
    }
    
    # Keep going until we've processed everything
    while input_str:
        matched = False
        # Try each pattern to see what matches next
        for key, pattern in patterns.items():
            match = re.match(pattern, input_str)
            if match:
                # Found a match!
                if key == 'SPACES':
                    # Just skip spaces
                    input_str = input_str[match.end():]
                    matched = True
                    break
                elif key == 'COMMENT':
                    # Skip comments too
                    input_str = input_str[match.end():]
                    matched = True
                    break
                else:
                    # Real token - add it to our list
                    token_type = getattr(TokenType, key)
                    tokens.append(MyToken(token_type, match.group(0)))
                    # Move past what we just processed
                    input_str = input_str[match.end():]
                    matched = True
                    break
        
        # If nothing matched, we have a problem
        if not matched:
            print(f"Error: Couldn't understand '{input_str[:20]}...'")
            break
            
    return tokens

# How to use this code:
# 
# with open("your_program.rpal", "r") as file:
#     code = file.read()
# 
# tokens = tokenize(code)
# 
# for token in tokens:
#     print(f"{token.type}: {token.value}")