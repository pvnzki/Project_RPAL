class Node:
    """Node class for representing syntax tree nodes."""
    
    def __init__(self):
        """Initialize a node with default values."""
        self.data = None
        self.depth = 0
        self.parent = None
        self.children = []
        self.is_standardized = False

    def set_data(self, data):
        """Set the data value for the node."""
        self.data = data

    def get_data(self):
        """Get the data value stored in the node."""
        return self.data

    def get_degree(self):
        """Get the number of children for this node."""
        return len(self.children)
    
    def get_children(self):
        """Return the list of child nodes."""
        return self.children

    def set_depth(self, depth):
        """Set the depth of this node in the tree."""
        self.depth = depth

    def get_depth(self):
        """Get the depth of this node in the tree."""
        return self.depth

    def set_parent(self, parent):
        """Set the parent node for this node."""
        self.parent = parent

    def get_parent(self):
        """Get the parent node of this node."""
        return self.parent

    def standardize(self):
        """Standardize the AST by applying transformation rules."""
        if self.is_standardized:
            return
            
        # First standardize all children
        for child in self.children:
            child.standardize()

        # Apply transformation rules based on node type
        if self.data == "let":
            # Standardize LET node
            #       LET              GAMMA
            #     /     \           /     \
            #    EQUAL   P   ->   LAMBDA   E
            #   /   \             /    \
            #  X     E           X      P 
            
            # Extract needed nodes
            equal_node = self.children[0]
            P_node = self.children[1]
            E_node = equal_node.children[1]
            X_node = equal_node.children[0]
            
            # Restructure the tree
            E_node.set_parent(self)
            E_node.set_depth(self.depth + 1)
            P_node.set_parent(equal_node)
            P_node.set_depth(self.depth + 2)
            
            # Update children
            self.children[1] = E_node
            equal_node.set_data("lambda")
            equal_node.children[1] = P_node
            self.set_data("gamma")
            
        elif self.data == "where":
            #       WHERE               LET
            #       /   \             /     \
            #      P    EQUAL   ->  EQUAL   P
            #           /   \       /   \
            #          X     E     X     E
            
            # Swap children and transform to LET
            P_node = self.children[0]
            equal_node = self.children[1]
            
            self.children[0] = equal_node
            self.children[1] = P_node
            self.set_data("let")
            
            # Apply LET standardization
            self.standardize()
            
        elif self.data == "function_form":
            
            #       FCN_FORM                EQUAL
            #       /   |   \              /    \
            #      P    V+   E    ->      P     +LAMBDA
            #                                    /     \
            #                                    V     .E
                
            # Get the expression node (last child)
            Ex = self.children[-1]
            
            # Create a new lambda node
            current_lambda = NodeFactory.create_lambda_node(self.depth + 1, self)
            self.children.insert(1, current_lambda)

            # Process variable nodes between P and E
            i = 2
            while self.children[i] != Ex:
                # Extract variable node
                V = self.children[i]
                self.children.pop(i)
                
                # Attach to lambda
                V.set_depth(current_lambda.depth + 1)
                V.set_parent(current_lambda)
                current_lambda.children.append(V)

                # Create nested lambda if needed
                if len(self.children) > 3:
                    new_lambda = NodeFactory.create_lambda_node(current_lambda.depth + 1, current_lambda)
                    current_lambda.children.append(new_lambda)
                    current_lambda = new_lambda

            # Attach expression to innermost lambda
            current_lambda.children.append(Ex)
            self.children.pop(2)
            self.set_data("=")
            
        elif self.data == "lambda":
            
            #     LAMBDA        LAMBDA
            #      /   \   ->   /    \
            #     V++   E      V     .E
            
            if len(self.children) > 2:
                # Extract expression node (last child)
                Ey = self.children[-1]
                
                # Create nested lambda structure
                current_lambda = NodeFactory.create_lambda_node(self.depth + 1, self)
                self.children.insert(1, current_lambda)

                # Process variables
                i = 2
                while self.children[i] != Ey:
                    V = self.children[i]
                    self.children.pop(i)
                    V.set_depth(current_lambda.depth + 1)
                    V.set_parent(current_lambda)
                    current_lambda.children.append(V)

                    # Create nested lambda if needed
                    if len(self.children) > 3:
                        new_lambda = NodeFactory.create_lambda_node(current_lambda.depth + 1, current_lambda)
                        current_lambda.children.append(new_lambda)
                        current_lambda = new_lambda

                # Attach expression to innermost lambda
                current_lambda.children.append(Ey)
                self.children.pop(2)
                
        elif self.data == "within":
            
            #           WITHIN                  EQUAL
            #          /      \                /     \
            #        EQUAL   EQUAL    ->      X2     GAMMA
            #       /    \   /    \                  /    \
            #      X1    E1 X2    E2               LAMBDA  E1
            #                                      /    \
            #                                     X1    E2
            
            # Extract components
            X1 = self.children[0].children[0]
            X2 = self.children[1].children[0]
            E1 = self.children[0].children[1]
            E2 = self.children[1].children[1]
            
            # Create new structure
            gamma = NodeFactory.create_gamma_node(self.depth + 1, self)
            lambda_ = NodeFactory.create_lambda_node(self.depth + 2, gamma)
            
            # Update node relationships
            X1.set_depth(X1.get_depth() + 1)
            X1.set_parent(lambda_)
            X2.set_depth(X1.get_depth() - 1)
            X2.set_parent(self)
            E1.set_depth(E1.get_depth())
            E1.set_parent(gamma)
            E2.set_depth(E2.get_depth() + 1)
            E2.set_parent(lambda_)
            
            # Build new tree structure
            lambda_.children.append(X1)
            lambda_.children.append(E2)
            gamma.children.append(lambda_)
            gamma.children.append(E1)
            self.children.clear()
            self.children.append(X2)
            self.children.append(gamma)
            self.set_data("=")
            
        elif self.data == "@":
            
            #         AT              GAMMA
            #       / | \    ->       /    \
            #      E1 N E2          GAMMA   E2
            #                       /    \
            #                      N     E1
            
            # Extract components
            e1 = self.children[0]
            n = self.children[1]
            e2 = self.children[2]
            
            # Create new gamma node
            gamma1 = NodeFactory.create_gamma_node(self.depth + 1, self)
            
            # Update relationships
            e1.set_depth(e1.get_depth() + 1)
            e1.set_parent(gamma1)
            n.set_depth(n.get_depth() + 1)
            n.set_parent(gamma1)
            
            # Build new structure
            gamma1.children.append(n)
            gamma1.children.append(e1)
            self.children = [gamma1, e2]
            self.set_data("gamma")
            
        elif self.data == "and":
            
            #         SIMULTDEF            EQUAL
            #             |               /     \
            #           EQUAL++  ->     COMMA   TAU
            #           /   \             |      |
            #          X     E           X++    E++
            
            # Create tuple structure nodes
            comma = NodeFactory.get_node_with_parent(",", self.depth + 1, self, [], True)
            tau = NodeFactory.get_node_with_parent("tau", self.depth + 1, self, [], True)

            # Process each equal node
            for equal in self.children:
                # Extract X and E from each equal
                X = equal.children[0]
                E = equal.children[1]
                
                # Connect to comma and tau
                X.set_parent(comma)
                E.set_parent(tau)
                comma.children.append(X)
                tau.children.append(E)

            # Replace children with tuple structure
            self.children = [comma, tau]
            self.set_data("=")
            
        elif self.data == "rec":
            
            #        REC                 EQUAL
            #         |                 /     \
            #       EQUAL     ->       X     GAMMA
            #      /     \                   /    \
            #     X       E                YSTAR  LAMBDA
            #                                     /     \
            #                                     X      E
            
            # Extract components
            X = self.children[0].children[0]
            E = self.children[0].children[1]
            
            # Create new structure
            F = NodeFactory.get_node_with_parent(X.get_data(), self.depth + 1, self, X.children, True)
            G = NodeFactory.create_gamma_node(self.depth + 1, self)
            Y = NodeFactory.get_node_with_parent("<Y*>", self.depth + 2, G, [], True)
            L = NodeFactory.create_lambda_node(self.depth + 2, G)

            # Update relationships
            X.set_depth(L.depth + 1)
            X.set_parent(L)
            E.set_depth(L.depth + 1)
            E.set_parent(L)
            
            # Build new structure
            L.children = [X, E]
            G.children = [Y, L]
            self.children = [F, G]
            self.set_data("=")

        # Mark as standardized
        self.is_standardized = True

class NodeFactory:
    """Factory class for creating nodes."""
    
    @staticmethod
    def get_node(data, depth):
        """Create a new node with the given data and depth."""
        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        node.children = []
        return node

    @staticmethod
    def get_node_with_parent(data, depth, parent, children=None, is_standardized=False):
        """Create a new node with the given attributes."""
        node = Node()
        node.set_data(data)
        node.set_depth(depth)
        node.set_parent(parent)
        node.children = children or []
        node.is_standardized = is_standardized
        return node
        
    @staticmethod
    def create_lambda_node(depth, parent):
        """Create a standardized lambda node."""
        return NodeFactory.get_node_with_parent("lambda", depth, parent, [], True)
        
    @staticmethod
    def create_gamma_node(depth, parent):
        """Create a standardized gamma node."""
        return NodeFactory.get_node_with_parent("gamma", depth, parent, [], True)