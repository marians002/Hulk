import sys

sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/src')
from cmp import visitor
from cmp.ast_for_hulk import *
from cmp.semantic import *


class TypeBuilder(object):
    def __init__(self, context, errors=None):
        if errors is None:
            errors = []
        self.context: Context = context
        self.current_type: Type = None
        self.errors = errors

    def __call__(self, ast : ProgramNode):
        self.visit(ast)
        return self.context, self.errors

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
        param_names, param_types = self.get_params_names_and_types(node)

        if node.ret_type:
            # Attempt to get the return type from the context.
            try:
                ret_type = self.context.get_type(node.ret_type)
            except SemanticError as ex:
                # If a SemanticError occurs (e.g., the return type is not defined), log the error
                # and use a generic ErrorType as the return type to continue the type checking process.
                self.errors.append(ex.text)
                ret_type = ErrorType()
        else:
            # If no return type is specified, default to the IntrinsicType
            ret_type = IntrinsicType()

        if self.current_type:
            # If there is a current type being processed, attempt to define a new method for it.
            try:
                self.current_type.define_method(node.identifier, param_names, param_types, ret_type)
            except SemanticError as ex:
                self.errors.append(ex.text)
        else:
            # If there is no current type, the method is considered a global function.
            try:
                # Define a global function in the 'Function' type with the given name, parameters, and return type.
                self.context.create_function(node.identifier, param_names, param_types, ret_type, node)
            except SemanticError as ex:
                self.errors.append(ex.text)


    def get_params_names_and_types(self, node):
        param_names, param_types = [], []
        
        if hasattr(node, 'params') and node.params:
            for param in node.params:
                p_name, p_type_name = param.identifier, param.type_name
                if p_name in param_names:
                    self.errors.append(f"Parameter '{p_name}' is already defined in the method signature")
                    param_types[param_names.index(p_name)] = ErrorType()
                else:
                    try:
                        param_type = self.context.get_type(p_type_name)
                    except SemanticError as ex:
                        if p_type_name:
                            self.errors.append(ex.text)
                        param_type = IntrinsicType()
                    param_types.append(param_type)
                    param_names.append(p_name)
        return param_names, param_types



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
            # Attempt to retrieve the type for the current node identifier from the context.
            self.current_type = self.context.get_type(node.identifier)
        except SemanticError as ex:
            self.errors.append(ex.text)
            self.current_type = ErrorType()
            return

        if node.inherits:
            if node.inherits in ['String', 'Number', 'Boolean']:
                self.errors.append(f"Type '{node.identifier}' cannot inherit from '{node.inherits}' because it is a built-in type")
            else:
                try:
                    # Attempt to retrieve the parent type from the context.
                    parent = self.context.get_type(node.inherits)
                    curr = parent

                    # Loop through the inheritance chain to check for inheritance cycles.
                    while curr:
                        if curr.name == self.current_type.name:
                            self.errors.append(f"Type '{self.current_type.name}' cannot inherit from itself")
                            parent = ErrorType()  # Use ErrorType to indicate an error in the type system.
                            break
                        curr = curr.inherits  # Move up the inheritance chain.

                except SemanticError as ex:
                    # If a SemanticError occurs (e.g., the parent type does not exist), log the error message.
                    self.errors.append(ex)
                    parent = ErrorType()

                try:
                    # Attempt to set the parent type for the current type.
                    self.current_type.set_parent(parent)
                except SemanticError as ex:
                    # If setting the parent fails due to a semantic error (e.g., already has a parent),
                    # log the error message.
                    self.errors.append(ex)

        else:
            # If no specific inheritance is defined for the current type,
            # set its parent to the default 'Object' type.
            self.current_type.set_parent(self.context.get_type('Object'))

        for attr in node.attr_list:
            self.visit(attr)
        self.current_type = None

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode):

        if node.identifier.startswith('<error>'):
            return

        try:
            # Attempt to retrieve the type for the current node identifier from the context.
            self.current_type = self.context.get_type(node.identifier)
        except SemanticError as ex:
            # If the type cannot be found (SemanticError is raised), log the error message.
            self.errors.append(ex)
            self.current_type = ErrorType()
            return

        if node.extends:
            try:
                # Attempt to retrieve the parent type based on 'extends' attribute of the node.
                parent = self.context.get_protocol(node.extends)
                curr = parent

                # Iterate through the inheritance chain to check for inheritance cycles.
                while curr:
                    # If the current type's name matches the parent's name, an inheritance cycle is detected.
                    if curr.name == self.current_type.name:
                        # Log an error indicating that a type cannot extend from itself or its descendants.
                        self.errors.append(f"Type '{self.current_type.name}' cannot extend from '{node.extends}'")
                        parent = ErrorType()
                        break
                    # Move up the inheritance chain.
                    curr = curr.inherits

            except SemanticError as ex:
                # If a SemanticError occurs (e.g., the parent type does not exist), log the error message.
                self.errors.append(ex)
                parent = ErrorType()

            try:
                # Set the parent type for the current type.
                self.current_type.set_parent(parent)

                # Iterate through all methods of the parent type to inherit them.
                for m in parent.all_methods():
                    # Define the inherited method in the current type with the same elements as in the parent type.
                    self.current_type.define_method(m[0].name, m[0].param_names, m[0].param_types, m[0].ret_type)

            except SemanticError as ex:
                self.errors.append(ex)

        for method in node.method_decl_col:
            self.visit(method)
        self.current_type = None

    @visitor.when(DeclareVarNode)
    def visit(self, node: DeclareVarNode):

        if node.identifier.startswith('<error>'):
            return

        try:
            # Attempt to retrieve the type of the variable from the context.
            var_t = self.context.get_type(node.type_name)
        except SemanticError as ex:
            # If a SemanticError is raised (e.g., the specified type name does not exist in the context),
            # log the error message.
            if node.type_name:
                self.errors.append(ex)
            # Default to the 'Object' type if the specified type name is invalid or not found.
            var_t = IntrinsicType()
        try:
            # Define the attribute (variable) in the current type context with the identifier and type retrieved.
            self.current_type.define_attribute(node.identifier, var_t)
        except SemanticError as ex:
            # If defining the attribute raises a SemanticError, (e.g., a duplicate attribute name)
            # Only log the error if the variable type is not already set to ErrorType, to avoid redundant error logging.
            if var_t != ErrorType():
                self.errors.append(ex)
