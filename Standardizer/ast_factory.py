from Standardizer.node import NodeFactory
from .ast import AST

# Factory for creating Abstract Syntax Trees from parser output
class ASTFactory:
    def __init__(self):
        pass

    def get_abstract_syntax_tree(self, data):
        root = NodeFactory.get_node(data[0], 0)
        previous = root
        depth = 0

        # Process each string representation after root
        for node_str in data[1:]:
            dot_count = 0
            for char in node_str:
                if char != '.':
                    break
                dot_count += 1

            # Extract the actual node data (after dots)
            node_data = node_str[dot_count:]
            current = NodeFactory.get_node(node_data, dot_count)

            # Determine where to attach the new node
            if depth < dot_count:
                previous.children.append(current)
                current.set_parent(previous)
            else:
                temp = previous
                while temp.get_depth() != dot_count:
                    temp = temp.get_parent()
                
                parent = temp.get_parent()
                parent.children.append(current)
                current.set_parent(parent)

            # Update for next iteration
            previous = current
            depth = dot_count
            
        return AST(root)