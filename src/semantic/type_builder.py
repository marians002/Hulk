from .format_visitor import *
from ..cmp.ast_for_hulk import *
from ..cmp.semantic import *


class TypeBuilder:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.errors = errors
    
    @visitor.on('node')
    def visit(self, node):
        pass
    
    # Your code here!!!
    # ????

    @visitor.when(ProgramNode)
    def visit(self, node):
        for class_declaration in node.declarations:
            self.visit(class_declaration)

    # @visitor.when(ClassDeclarationNode)
    # def visit(self, node):
    #     self.current_type = self.context.get_type(node.id)

    #     if node.parent:
    #         try:
    #             parent_type = self.context.get_type(node.parent)
    #             try:
    #                 self.current_type.set_parent(parent_type)
    #             except SemanticError as ex:
    #                 self.errors.append(ex.text)
    #         except SemanticError as ex:
    #             self.errors.append(ex.text)

    #     for feature in node.features:
    #         self.visit(feature)

    @visitor.when(FunctionNode)
    def visit(self, node):
        param_names = []
        param_types = []
        for param_name, param_type_str in node.params:
            param_names.append(param_name)
            try:
                param_type = self.context.get_type(param_type_str)
            except SemanticError as ex:
                self.errors.append(ex.text)
                param_type = ErrorType()
            param_types.append(param_type)
        try:
            type = self.context.get_type(node.type)
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_method(node.id,param_names,param_types,type) 
        except SemanticError as ex:
            self.errors.append(ex.text)

    # @visitor.when(AttrDeclarationNode)
    # def visit(self,node):
    #     try:
    #         type = self.context.get_type(node.type)
    #     except SemanticError as ex:
    #         self.errors.append(ex.text)
    #         type = ErrorType()
    #     try:
    #         self.current_type.define_attribute(node.id,type) 
    #     except SemanticError as ex:
    #         self.errors.append(ex.text)    

        