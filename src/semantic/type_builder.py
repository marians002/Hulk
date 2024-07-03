from ..cmp.visitor import visitor
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
    

    @visitor.when(ProgramNode)
    def visit(self, node):
        for class_declaration in node.declarations:
            self.visit(class_declaration)

        return self.context, self.errors

    
    @visitor.when(FunctionNode)
    def visit(self, node):
        param_names = []
        param_types = []
        for param in node.params:
            p_name = param.identifier
            p_type = param.type_name
            try:
                param_type = self.context.get_type(p_type)
            except SemanticError as ex:
                self.errors.append(ex.text)
                param_type = ErrorType()
            param_types.append(param_type)
        try:
            type = self.context.get_type(node.type_name)
        except SemanticError as ex:
            self.errors.append(ex.text)
            type = ErrorType()
        try:
            self.current_type.define_method(node.identifier, param_names, param_types, type) 
        except SemanticError as ex:
            self.errors.append(ex.text)



    @visitor.when(TypeNode)
    def visit(self, node):
        try:
            self.current_type = self.context.get_type(node.identifier)
        except SemanticError as ex:
            self.errors.append(ex.text)
            self.current_type = ErrorType()
            return
        for attr in node.attr_list:
            self.visit(attr)
        self.current_type = None


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

        