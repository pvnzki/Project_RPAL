class AST:
    def __init__(self, root=None):
        self.root = root

    def set_root(self, root):
        self.root = root

    def get_root(self):
        return self.root

    def standardize(self):
        if self.root and not getattr(self.root, 'is_standardized', False):
            self.root.standardize()

    def pre_order_traverse(self, node, level):
        if not node:
            return
            
        indent = "." * level
        print(f"{indent}{node.get_data()}")
        
        for child in node.get_children() if hasattr(node, 'get_children') else node.children:
            self.pre_order_traverse(child, level + 1)

    def print_ast(self):
        if not self.root:
            print("Empty tree")
            return
            
        self.pre_order_traverse(self.get_root(), 0)
        
    def tree_depth(self):
        def max_depth(node, current=0):
            if not node:
                return current
            
            if not node.children:
                return current + 1
                
            depths = [max_depth(child, current + 1) for child in node.children]
            return max(depths)
            
        return max_depth(self.root)