import sys

sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/')
from src.cmp import visitor
from src.cmp.ast_for_hulk import *
from src.cmp.semantic import *


class TypeBuilder:
    def __init__(self, context, errors=None):
        if errors is None:
            errors = []
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for decl in node.decl_list:
            self.visit(decl)
        self.visit(node.global_exp)
        return self.context, self.errors

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode):
        param_names, param_types = [], []

        if hasattr(node, 'params') and node.params:
            for param in node.params:
                p_name, p_type = param.identifier, param.type_name
                if p_name in param_names:
                    self.errors.append(f"Parameter '{p_name}' already defined in method '{node.identifier}'")
                    param_types[param_names.index(p_name)] = ErrorType()
                    continue
                try:
                    param_type = self.context.get_type(p_type)
                except SemanticError as ex:
                    if p_type:
                        self.errors.append(ex.text)
                    param_type = self.context.get_type('Object')
                param_types.append(param_type)
                param_names.append(p_name)

        if node.ret_type:
            try:
                ret_type = self.context.get_type(node.ret_type)
            except SemanticError as ex:
                self.errors.append(ex.text)
                ret_type = ErrorType()
        else:
            ret_type = self.context.get_type('Object')

        if self.current_type:
            try:
                self.current_type.define_method(node.identifier, param_names, param_types, ret_type)
            except SemanticError as ex:
                self.errors.append(ex.text)
        else:
            try:
                self.context.get_type('Function').define_method(node.identifier, param_names, param_types, ret_type)
            except SemanticError as ex:
                self.errors.append(ex.text)

    # def check_inheritance_cycle(self, node):
    #     try:
    #         if node is ProtocolNode:
    #             parent = self.context.get_type(node.extends)
    #         else:
    #             parent = self.context.get_type(node.inherits)
    #         curr = parent
    #
    #         while curr:
    #             if curr.name == self.current_type.name:
    #                 self.errors.append(f"Type '{self.current_type.name}' cannot inherit from '{node.inherits}'")
    #                 parent = ErrorType()
    #                 break
    #             curr = curr.inherits
    #
    #     except SemanticError as ex:
    #         self.errors.append(ex.text)
    #         parent = ErrorType()

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
        elif node.inherits:
            try:
                parent = self.context.get_type(node.inherits)
                curr = parent

                while curr:
                    if curr.name == self.current_type.name:
                        self.errors.append(f"Type '{self.current_type.name}' cannot inherit from '{node.inherits}'")
                        parent = ErrorType()
                        break
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
        self.current_type = None

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

        if node.extends:
            try:
                parent = self.context.get_type(node.extends)
                curr = parent

                while curr:
                    if curr.name == self.current_type.name:
                        self.errors.append(f"Type '{self.current_type.name}' cannot inherit from '{node.extends}'")
                        parent = ErrorType()
                        break
                    curr = curr.inherits

            except SemanticError as ex:
                self.errors.append(ex.text)
                parent = ErrorType()

            try:
                self.current_type.set_parent(parent)
                for method in parent.all_methods():
                    first_in_method = method[0]
                    self.current_type.define_method(first_in_method.name, first_in_method.param_names,
                                                    first_in_method.param_types, first_in_method.ret_type)
            except SemanticError as ex:
                self.errors.append(ex.text)

        for method in node.method_decl_col:
            try:
                self.visit(method)
            except SemanticError as ex:
                self.errors.append(ex.text)
        self.current_type = None

    @visitor.when(DeclareVarNode)
    def visit(self, node: DeclareVarNode):

        if node.identifier.startswith('<error>'):
            return

        try:
            var_t = self.context.get_type(node.type_name)
        except SemanticError as ex:
            if node.type_name:
                self.errors.append(ex.text)
            var_t = self.context.get_type('Object')
        try:
            self.current_type.define_attribute(node.identifier, var_t)
        except SemanticError as ex:
            if var_t != ErrorType():
                self.errors.append(ex.text)
