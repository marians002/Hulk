import sys
sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/src')
from cmp import visitor
from cmp.ast_for_hulk import *
from cmp.semantic import *


def check_id(node):
    return node.identifier.startswith('<error')


class TypeInferer:

    def __init__(self, context, errors=None):
        self.context = context
        if errors is None:
            errors = []
        self.errors = errors
        self.current_function = None
        self.current_type = None
        self.i = 0
        self.max_i = 3

    def valid_iters(self):
        if self.i < self.max_i:
            self.i += 1
            return True
        return False

    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for decl in node.decl_list:
            self.visit(decl)
        self.visit(node.global_exp)

        if self.valid_iters():
            self.visit(node)

        return self.context, self.errors

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode):
        # Set the current function to the identifier of the node being visited.
        self.current_function = node.identifier

        # If the function identifier indicates an error, return the node's return type.
        if check_id(node):
            return node.ret_type

        # Determine the function object:
        # if within a type, get it from the current type;
        # otherwise, from the global context.
        if self.current_type:
            func = self.current_type.get_method(node.identifier)
        else:
            func = self.context.get_type("Function").get_method(node.identifier)

        # Visit the body of the function to determine its return type.
        b_type = self.visit(node.body)

        # Set the function's return type in its scope. If a specific return type is declared
        # and it's not 'Object', use the declared type.
        # Otherwise, use the inferred type from the function body.
        if node.ret_type and node.ret_type != self.context.get_type('Object'):
            node.scope.ret_type = self.context.get_type(node.ret_type)
        else:
            node.scope.ret_type = b_type
            func.return_type = b_type

        # Reset the current function context to None after processing the function.
        self.current_function = None

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):

        if check_id(node):
            return

        self.current_type = self.context.get_type(node.identifier)

        if self.current_type.parent and self.current_type.parent is ErrorType():
            self.errors.append(f'Type "{node.identifier}" inherits from an invalid type.')

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode):
        if check_id(node):
            return

        # Set the current type context to the type defined by the node's identifier.
        self.current_type = self.context.get_type(node.identifier)

        # Check if the current type extends another type.
        if self.current_type.parent:
            # Retrieve the type that the current type extends.
            p_type = self.current_type.parent
            # If the extended type is an ErrorType, log an error indicating an invalid extension.
            if p_type is ErrorType():
                self.errors.append(f'Protocol "{node.identifier}" extends from an invalid type.')

        # Iterate over the method declarations of the protocol node.
        for m in node.method_decl_col:
            self.visit(m)

        # Reset the current type context to None after processing the protocol node.
        self.current_type = None

    @visitor.when(DeclareVarNode)
    def visit(self, node: DeclareVarNode):
        if check_id(node):
            return

        # If variable has an invalid name, return the error type.
        # if node.identifier == 'self':
        #     return self.current_type

        if node.type_name:
            # Attempt to get the type of the variable from the context.
            try:
                v_type = self.context.get_type(node.type_name)
            except SemanticError:
                # If the type name is not found in the context, assign an ErrorType.
                v_type = ErrorType()
        else:
            # If no type name is provided, default to the 'Object' type.
            v_type = self.context.get_type('Object')

        # Visit the value of the variable to infer its type.
        e_type = self.visit(node.value)

        # If the variable type is 'Object', it means its type is not explicitly declared.
        # In this case, update the variable's type in its scope to the inferred type from its value.
        if v_type.name == self.context.get_type('Object').name:
            node.scope.find_variable(node.identifier).type = e_type

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode):
        statement_t = ErrorType()
        for statement in node.statement_list:
            statement_t = self.visit(statement)
        return statement_t

    @visitor.when(AndNode)
    def visit(self, node: AndNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Boolean')

    @visitor.when(OrNode)
    def visit(self, node: OrNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Boolean')

    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        left_t = self.visit(node.exp)
        return self.context.get_type('Boolean')

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('String')

    @visitor.when(EqualNode)
    def visit(self, node: EqualNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Boolean')

    @visitor.when(NotEqualNode)
    def visit(self, node: EqualNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Boolean')

    @visitor.when(NotEqualNode)
    def visit(self, node: EqualNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Boolean')

    @visitor.when(LessThanNode)
    def visit(self, node: LessThanNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Boolean')

    @visitor.when(LessEqualNode)
    def visit(self, node: LessEqualNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Boolean')

    @visitor.when(GreaterThanNode)
    def visit(self, node: GreaterThanNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Boolean')

    @visitor.when(GreaterEqualNode)
    def visit(self, node: GreaterEqualNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Boolean')

    @visitor.when(PlusNode)
    def visit(self, node: PlusNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Number')

    @visitor.when(MinusNode)
    def visit(self, node: MinusNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Number')

    @visitor.when(ProductNode)
    def visit(self, node: ProductNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Number')

    @visitor.when(DivisionNode)
    def visit(self, node: DivisionNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Number')

    @visitor.when(ModNode)
    def visit(self, node: ModNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Number')

    @visitor.when(PowNode)
    def visit(self, node: PowNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        return self.context.get_type('Number')

    @visitor.when(NegativeNode)
    def visit(self, node: NegativeNode):
        exp_t = self.visit(node.exp)
        return self.context.get_type('Number')

    @visitor.when(NumberNode)
    def visit(self, node: NumberNode):
        return self.context.get_type('Number')

    @visitor.when(StringNode)
    def visit(self, node: StringNode):
        return self.context.get_type('String')

    @visitor.when(BoolNode)
    def visit(self, node: BoolNode):
        return self.context.get_type('Boolean')

    @visitor.when(IsNode)
    def visit(self, node: IsNode):
        self.visit(node.exp)
        return self.context.get_type('Boolean')

    @visitor.when(AsNode)
    def visit(self, node: AsNode):
        self.visit(node.exp)
        return self.context.get_type(node.type_name)

    @visitor.when(VarNode)
    def visit(self, node: VarNode):
        if check_id(node):
            return ErrorType()

        if node.identifier == 'self':
            # If the identifier of the node is 'self', return the current type context to handle self references.
            return self.current_type

        try:
            # Attempt to find the variable in the current scope by its identifier and return its type.
            var = node.scope.find_variable(node.identifier)
            if not var:
                raise SemanticError
            return self.context.get_type(var.id)
        except SemanticError:
            # If the variable is not found, log an error and return an ErrorType.
            self.errors.append(f'Variable "{node.identifier}" is not defined.')
            return ErrorType()

    @visitor.when(InvoqueFuncNode)
    def visit(self, node: InvoqueFuncNode):
        args_t = []
        for arg in node.args:
            # Iterate through each argument in the node's arguments list and visit them.
            # The result of visiting (type inference or other processing) is appended to args_t.
            args_t.append(self.visit(arg))

        try:
            # Attempt to retrieve the function definition from the context using the node's identifier.
            # This includes getting the function's type and method details.
            function = self.context.get_type('Function').get_method(node.identifier)
        except SemanticError:
            # If the function cannot be found in the context, log an error.
            self.errors.append(f'Function "{node.identifier}" is not defined.')
            return ErrorType()

        if len(args_t) != len(function.param_types):
            # Check if the number of arguments provided matches the function's expected parameters.
            self.errors.append(f'Function "{node.identifier}" expects {len(function.param_types)} arguments, '
                               f'but {len(args_t)} were provided.')
            # Return an ErrorType to indicate the type error due to incorrect argument count.
            return ErrorType()
        # If all checks pass, return the function's return type as the result of this visit.
        return function.return_type

    @visitor.when(AttrCallNode)
    def visit(self, node: AttrCallNode):
        object_t = self.visit(node.exp)

        try:
            # Check if the object's type is not an error type.
            if object_t is not ErrorType():
                # If it's a valid type, return the type of the attribute.
                return object_t.get_attribute(node.attribute).type
        except SemanticError:
            # If accessing the attribute raises a SemanticError, log the error.
            self.errors.append(f'Attribute "{node.attribute}" is not defined in {self.current_type.name}.')
        return ErrorType()

    @visitor.when(PropCallNode)
    def visit(self, node: PropCallNode):
        object_t = self.visit(node.exp)

        if object_t is not ErrorType():
            try:
                # Check if the object's type is not an error type.
                # If it's a valid type, return the type of the method.
                return object_t.get_method(node.function.identifier).return_type
            except SemanticError:
                # If accessing the method raises a SemanticError, log the error.
                self.errors.append(f'Method "{node.function.identifier}" is not defined in {self.current_type.name}')
        else:
            return ErrorType()

    @visitor.when(IfNode)
    def visit(self, node: IfNode):
        types_list = []
        for condition, body in node.conditions:
            _ = self.visit(condition)
            types_list.append(self.visit(body))  # Can contain Error Types
        return get_fca(types_list)

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode):
        self.visit(node.condition)
        return self.visit(node.body)

    @visitor.when(ForNode)
    def visit(self, node: ForNode):
        iter_t = self.visit(node.exp)  # Visit the expression to infer its type.

        # Find the variable in the current scope based on the identifier provided in the node.
        for_var = node.exp.scope.find_variable(node.var.identifier)

        # Check if the inferred type of the expression is an ErrorType, indicating an error.
        if iter_t is ErrorType():
            for_var.type = ErrorType()
        elif iter_t == IntrinsicType():
            for_var.type = IntrinsicType()  # Assign AutoType if the expression type is auto-determined.
        elif not iter_t.conforms_to(self.context.get_type('Iterable')):
            # Append an error message if the inferred type does not conform to 'Iterable'.
            self.errors.append(f'Expression is not iterable.')
            for_var.type = ErrorType()
        else:
            # If the expression type is iterable, assign the type of the current item as the variable's type.
            for_var.type = iter_t.get_method('current').return_type

        return self.visit(node.body)  # Visit the body of the loop to infer and return its type.

        # try:
        #     # print("FOR NODE. TRYING", iter_t)
        #     var_t = self.context.get_type(node.var.identifier)
        # except SemanticError as e:
        #     # print("FOR NODE. ERROR", e)
        #     # self.errors.append(f'Variable "{node.var.identifier}" is not defined.')
        #     var_t = AutoType()
        #
        # return self.visit(node.body)

    @visitor.when(LetNode)
    def visit(self, node: LetNode):
        for decl in node.var_decl:
            self.visit(decl)
        return self.visit(node.body)

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        if node.identifier == 'self':
            # Prevent assignment to the special 'self' identifier, which is reserved for object instances.
            self.errors.append('Cannot assign to "self".')
            return self.current_type

        var = node.scope.find_variable(node.identifier)
        if var is None:
            # If the variable is not found in the current scope, log an error and return an ErrorType.
            self.errors.append(f'Variable "{node.identifier}" is not defined.')
            return ErrorType()

        # Proceed to visit the expression on the right-hand side of the assignment.
        return self.visit(node.exp)

    @visitor.when(NewNode)
    def visit(self, node: NewNode):
        try:
            # Attempt to retrieve the type from the context using the node's type_name."
            t = self.context.get_type(node.type_name)
            args_t = []
            for arg in node.args:
                args_t.append(self.visit(arg))
        except SemanticError:
            # If the type cannot be found in the context, log an error and return an ErrorType.
            self.errors.append(f'Type "{node.type_name}" is not defined.')
            return ErrorType()

        t_attr = []
        for attr in t.attributes:
            if attr.name.startswith('IN') and attr.name.endswith('ESP'):
                t_attr.append(attr)
        if len(args_t) != 0 and len(args_t) != len(t_attr):
            self.errors.append(f'Expected {len(t_attr)} arguments, but {len(args_t)} were provided.')
            return ErrorType()

        for _, attr in zip(args_t, t_attr):
            try:
                self.context.get_type(attr.type.name)
            except SemanticError:
                self.errors.append(f'Type "{attr.type.name}" is not defined.')
                return ErrorType()
        return t

    @visitor.when(IndexNode)
    def visit(self, node: IndexNode):
        object_t = self.visit(node.exp)
        index_t = self.visit(node.index)

        if object_t is not ErrorType():
            try:
                # Check if the object's type is not an error type.
                # If it's a valid type, return the type of the attribute.
                return object_t.get_attribute('current').type
            except SemanticError:
                # If accessing the attribute raises a SemanticError, log the error.
                self.errors.append(f'Attribute "current" is not defined in {self.current_type.name}.')
        return ErrorType()

    @visitor.when(VectorNode)
    def visit(self, node: VectorNode):
        item_t = []

        for exp in node.exp_list:
            item_t.append(self.visit(exp))
        # AAAAAAA
        # NO SE QUE HACER AQUI
        return ErrorType()

    @visitor.when(VectorComprNode)
    def visit(self, node: VectorComprNode):
        it_t = self.visit(node.iter_exp)

        if not it_t.conforms_to(self.context.get_type('Iterable')):
            self.errors.append(f'Expression is not iterable.')
            return ErrorType()

        ret_t = self.visit(node.exp)
        if ret_t is ErrorType():
            return ErrorType()
        return self.context.get_type(f'Vector<{ret_t.name}>')  # ESTO NO VA A FUNCIONAR
