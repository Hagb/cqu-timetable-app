#!/usr/bin/env python3
import ast
import glob
import sys
import os

# From stack overflow https://stackoverflow.com/a/51274274
# by snakecharmerb https://stackoverflow.com/users/5320906/snakecharmerb
class StripDocstring(ast.NodeTransformer):

    def visit_Module(self, node):
        self.generic_visit(node)
        return self._visit_docstring_parent(node)

    def visit_FunctionDef(self, node):
        self.generic_visit(node)
        return self._visit_docstring_parent(node)

    def visit_ClassDef(self, node):
        self.generic_visit(node)
        return self._visit_docstring_parent(node)

    def _visit_docstring_parent(self, node):
        # Common docstring removal code.
        # Assumes docstrings will always be first node in
        # module/class/function body.
        new_body = []
        for i, child_node in enumerate(node.body):
            if isinstance(child_node, ast.Expr) and isinstance(child_node.value, ast.Str):
                pass
            else:
                new_body.append(child_node)
        if not new_body:
            new_body.append(ast.Pass())
        node.body = new_body
        return node

strip_docstring = StripDocstring().visit
os.chdir(sys.argv[1])
for path in glob.glob("**/*.py", recursive=True):
    with open(path) as file:
        ast_ = ast.parse(file.read())
    strip_docstring(ast_)
    with open(path, 'w') as file:
        file.write(ast.unparse(ast_))

