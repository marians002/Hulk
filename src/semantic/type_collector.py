from ..cmp.ast_for_hulk import *
from .format_visitor import *
from cmp.semantic import *

class TypeCollector(object):
    def __init__(self, errors=[]):
        self.context = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    @visitor.when(ProgramNode)
    def visit(self, node):
        self.context = Context()
        # Your code here!!!
        self.context.types['int'] = IntType()        
        self.context.types['void'] = VoidType()
        self.context.types['error'] = ErrorType()
        for class_declaration in node.declarations:
            self.visit(class_declaration)
        
    # Your code here!!!
    # wtf
    # @visitor.when(ClassDeclarationNode)
    # def visit(self, node):
    #     try:
    #         self.context.create_type(node.id)   
    #     except SemanticError as ex:
    #         self.errors.append(ex.text)