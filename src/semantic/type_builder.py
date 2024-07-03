import sys
sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/')
from src.cmp import visitor
from src.cmp.ast_for_hulk import *
from src.cmp.semantic import *


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

        if node.params is not None and hasattr(node, 'params'):
            for param in node.params:
                p_name = param.identifier
                p_type = param.type_name
                if p_name in param_names:
                    self.errors.append(f"Parameter '{p_name}' already defined in method '{node.identifier}'")
                    param_types[param_names.index(p_name)] = ErrorType()
                    continue
                try:
                    param_type = self.context.get_type(p_type)
                except SemanticError as ex:
                    self.errors.append(ex.text)
                    param_type = ErrorType()
                param_types.append(param_type)
                param_names.append(p_name)
        # try:
        #     type = self.context.get_type(node.type_name)
        # except SemanticError as ex:
        #     self.errors.append(ex.text)
        #     type = ErrorType()
        # try:
        #     self.current_type.define_method(node.identifier, param_names, param_types, type)
        # except SemanticError as ex:
        #     self.errors.append(ex.text)
        return param_names, param_types

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):

        if node.identifier.startswith('<error>'):
            return
        
        try:
            self.current_type = self.context.get_type(node.identifier)
        except SemanticError as ex:
            self.errors.append(ex.text)
            self.current_type = ErrorType()
            return

        if node.inherits in ['String', 'Number', 'Boolean']:
            self.errors.append(f"Type '{node.identifier}' cannot inherit from '{node.inherits}'")
        elif node.inherits is not None:
            try:
                parent = self.context.get_type(node.inherits)
                curr = parent

                while curr is not None:
                    if curr.name == self.current_type.name:
                        self.errors.append(f"Type '{self.current_type.name}' cannot inherit from '{node.inherits}'")
                    curr = curr.inherits

            except SemanticError as ex:
                self.errors.append(ex.text)
                parent = ErrorType()

            try:
                self.current_type.set_parent(parent)
            except SemanticError as ex:
                self.errors.append(ex.text)

        else:
            self.current_type.set_parent(self.context.get_type('Object'))

        for attr in node.attr_list:
            self.visit(attr)

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode):

        if node.identifier.startswith('<error>'):
            return

        try:
            self.current_type = self.context.get_type(node.identifier)
        except SemanticError as ex:
            self.errors.append(ex.text)
            self.current_type = ErrorType()
            return

        if node.extends is not None:
            try:
                parent = self.context.get_type(node.extends)
                curr = parent

                while curr is not None:
                    if curr.name == self.current_type.name:
                        self.errors.append(f"Type '{self.current_type.name}' cannot inherit from '{node.inherits}'")
                    curr = curr.inherits

            except SemanticError as ex:
                self.errors.append(ex.text)
                parent = ErrorType()

            try:
                self.current_type.set_parent(parent)
            except SemanticError as ex:
                self.errors.append(ex.text)

        for method in node.method_decl_col:
            self.visit(method)

    @visitor.when(DeclareVarNode)
    def visit(self, node: DeclareVarNode):

        if node.identifier.startswith('<error>'):
            return

        try:
            var_t = self.context.get_type(node.type_name)
        except SemanticError as ex:
            self.errors.append(ex.text)
            var_t = ErrorType()
        try:
            self.current_type.define_attribute(node.identifier, var_t)
        except SemanticError as ex:
            self.errors.append(ex.text)
