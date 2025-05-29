import argparse
import sys
from contextlib import contextmanager
from Parser.parser_1 import Parser
from Lexical_Analyzer.lexical_analyzer import tokenize
from Standardizer.ast_factory import ASTFactory
from CSE_Machine.csemachine import CSEMachine
from CSE_Machine.cse_factory import CSEMachineFactory

@contextmanager
def smart_open(filename=None, mode='r'):
    """Context manager that handles file operations safely."""
    if filename and filename != '-':
        file = open(filename, mode)
        try:
            yield file
        finally:
            file.close()
    else:
        yield sys.stdin if mode.startswith('r') else sys.stdout

class RPALProcessor:
    """Class to process RPAL programs with improved structure and error handling."""
    
    def __init__(self):
        self._setup_argument_parser()
    
    def _setup_argument_parser(self):
        """Set up command line argument parser."""
        self.arg_parser = argparse.ArgumentParser(description='RPAL Language Processor')
        self.arg_parser.add_argument('file_name', type=str, help='The RPAL program input file (use - for stdin)')
        self.arg_parser.add_argument('-ast', action='store_true', help='Print the abstract syntax tree')
        self.arg_parser.add_argument('-sast', action='store_true', help='Print the standardized abstract syntax tree')
        self.arg_parser.add_argument('-v', '--verbose', action='store_true', help='Enable verbose output')
    
    def process(self, cmd_args=None):
        """Process RPAL program according to command line arguments."""
        args = self.arg_parser.parse_args(cmd_args)
        
        # Read input with improved error handling
        try:
            with smart_open(args.file_name) as input_file:
                input_text = input_file.read()
        except FileNotFoundError:
            print(f"Error: File '{args.file_name}' not found")
            return 1
        except IOError as e:
            print(f"Error reading file: {e}")
            return 1
            
        # Process the RPAL program
        try:
            if args.verbose:
                print("Tokenizing input...")
            tokens = tokenize(input_text)
            
            if args.verbose:
                print("Parsing tokens...")
            parser = Parser(tokens)
            ast_nodes = parser.parse()
            if ast_nodes is None:
                print("Error: Parsing failed")
                return 1
                
            # Handle AST output
            if args.verbose:
                print("Converting to string AST...")
            string_ast = parser.convert_ast_to_string_ast()
            if args.ast:
                for string in string_ast:
                    print(string)
                return 0
            
            # Handle SAST output
            if args.verbose:
                print("Building and standardizing AST...")
            ast_factory = ASTFactory()
            ast = ast_factory.get_abstract_syntax_tree(string_ast)
            ast.standardize()
            if args.sast:
                ast.print_ast()
                return 0
            
            # Execute program
            if args.verbose:
                print("Building CSE machine...")
            cse_machine_factory = CSEMachineFactory()
            cse_machine = cse_machine_factory.get_cse_machine(ast)
            
            if args.verbose:
                print("Executing program...")
            result = cse_machine.get_answer()
            
            # Output result
            print("Output of the RPAL program:")
            print(result)
            return 0
            
        except Exception as e:
            print(f"Error: {e}")
            if args.verbose:
                import traceback
                traceback.print_exc()
            return 1

def main():
    """Entry point for the RPAL interpreter."""
    processor = RPALProcessor()
    return processor.process()

if __name__ == "__main__":
    sys.exit(main())