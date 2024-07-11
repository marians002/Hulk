import sys
sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/src')
from cmp import visitor
from cmp.ast_for_hulk import *
from cmp.semantic import *


def check_id(node):
    return node.identifier.startswith('<error>')


class TypeInferer:

    def assign_auto_type(self, node: Node, scope: Scope, inf_t: Type | Protocol):
        if isinstance(node, VarNode) and scope.is_defined(node.identifier):
            var = scope.find_variable(node.identifier)
            if var.type != IntrinsicType() or var.type == ErrorType():
                return
            var.type = inf_t
            if not isinstance(inf_t, IntrinsicType):
                self.upd = True
        if isinstance(node, IndexNode):
            self.assign_auto_type(node.exp, scope, VectorType(inf_t))
        

    def __init__(self, context, errors=None):
        self.context: Context = context
        if errors is None:
            errors = []
        self.errors = errors
        self.current_function = None
        self.current_type = None
        self.upd = False


    @visitor.on('node')
    def visit(self, node):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        for decl in node.decl_list:
            self.visit(decl)
        self.visit(node.global_exp)

        if self.upd:
            self.upd = False
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
        # if within a type, get it from the current type; otherwise, from the global context.
        if self.current_type:
            func = self.current_type.get_method(node.identifier)
        else:
            func = self.context.get_function(node.identifier)

        # Visit the body of the function to determine its return type.
        b_type = self.visit(node.body)

        # Set the function's return type in its scope. If a specific return type is declared
        # and it's not 'IntrinsicType', use the declared type.
        # Otherwise, use the inferred type from the function body.
        if node.ret_type and node.ret_type != IntrinsicType():
            node.scope.ret_type = self.context.get_type(node.ret_type)
        else:
            node.scope.ret_type = b_type
            func.return_type = b_type

        # If it is a global function, process its parameters:
        if not self.current_type:
            for param in node.params:
                local_var = node.body.scope.find_variable(param.identifier)
                p_type = local_var.type = self.context.get_type(param.type_name)
                
                # Check if the parameter type can be inferred in the body:
                if isinstance(p_type, IntrinsicType):
                    try:
                        new_t = get_common_type(p_type, self.visit(local_var.value))
                    except SemanticError:
                        self.errors.append(f'Parameter "{param.identifier}" type cannot be inferred.')
                        new_t = ErrorType()
                    func.param_types.append(new_t)
                    if not isinstance(new_t, IntrinsicType):
                        self.upd = True
                    local_var.type = new_t
                
                # Check if the parameter type can be inferred in any call:
                if isinstance(p_type, IntrinsicType):
                    new_t = get_fca(func.param_types)
                    p_type = new_t
                    if not isinstance(new_t, IntrinsicType):
                        self.upd = True
                    local_var.type = new_t
        # Reset the current function context to None after processing the function.
        self.current_function = None   
        return b_type

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):

        if check_id(node):
            return

        self.current_type = self.context.get_type(node.identifier)
        if len(node.params) == 0 and node.parent:
            try:
                params = self.context.get_type(node.inherits).attributes
            except SemanticError as e:
                self.errors.append(f'Type "{node.inherits}" is not defined.')
                return
            for param in params:
                node.params.append(DeclareVarNode(param.name, param.type.name if param.type != IntrinsicType() else None, None))
                node.args.append(VarNode(param.name))
                try:
                    self.current_type.define_attribute('PS'+param.name+'PE', node.scope.find_variable(param).type)
                except SemanticError as e:
                    self.current_type.define_attribute('PS'+param.name+'PE', IntrinsicType())

            else:
                for param in node.params:
                    add=True
                    if param.identifier in [attr.name for attr in self.current_type.attributes]:
                        add = False
                    try:
                        self.current_type.define_attribute('PS'+param.identifier+'PE', node.scope.find_variable(param.identifier).type)
                    except SemanticError as e:
                        self.current_type.define_attribute('PS'+param.identifier+'PE', IntrinsicType())

        if self.current_type.parent:
            if type(self.current_type.parent) == ErrorType():
                self.errors.append(f'Invalid parent type for {node.identifier}')
        for attr in node.attr_list:
            self.visit(attr)
        self.current_type = None

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode):
        if check_id(node):
            return

        # Set the current type context to the type defined by the node's identifier.
        self.current_type = self.context.get_protocol(node.identifier)

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

        if node.identifier == 'self':
            return self.current_type

        if node.type_name:  
            # Attempt to get the type of the variable from the context.
            try:
                v_type = self.context.get_type(node.type_name)
            except SemanticError:
                # If the type name is not found in the context, assign an ErrorType.
                v_type = ErrorType()
        else:
            # If no type name is provided, default to the 'Object' type.
            v_type = IntrinsicType()

        # Visit the value of the variable to infer its type.
        exp_t = self.visit(node.value)
        var = node.scope.find_variable(node.identifier)
        var.type = var.type if var.type != IntrinsicType() or var.type is not ErrorType() else exp_t
        return var.type

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
        except SemanticError as ex:
            # If the variable is not found, log an error and return an ErrorType.
            self.errors.append(f'Variable "{node.identifier}" is not defined.')
            return ErrorType()
        return var.type

    @visitor.when(InvoqueFuncNode)
    def visit(self, node: InvoqueFuncNode):
        args_t = [self.visit(arg) for arg in node.args]
        function = node.identifier
        current = 'Function'

        if node.identifier == 'base':
            current = self.current_type.parent.name
            function = self.current_function

        try:
            # Attempt to retrieve the function definition from the context using the node's identifier.
            # This includes getting the function's type and method details.
            function = self.context.get_type(current).get_method(function)
        except SemanticError:
            # If the function cannot be found in the context, log an error.
            self.errors.append(f'Function "{node.identifier}" is not defined.')
            for arg in node.args:
                self.visit(arg)
            return ErrorType()

        if len(args_t) != len(function.param_types):
            # Check if the number of arguments provided matches the function's expected parameters.
            self.errors.append(f'Function "{node.identifier}" expects {len(function.param_types)} arguments, '
                               f'but {len(args_t)} were provided.')
            # Return an ErrorType to indicate the type error due to incorrect argument count.
            return ErrorType()
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
                if object_t != IntrinsicType():
                    # If accessing the method raises a SemanticError, log the error.
                    self.errors.append(f'Method "{node.function.identifier}" is not defined in {self.current_type.name}')
                return IntrinsicType()
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
        if iter_t is ErrorType() or iter_t == IntrinsicType():
            for_var.type = iter_t 
        elif not iter_t.conforms_to(self.context.get_type('Iterable')):
            # Append an error message if the inferred type does not conform to 'Iterable'.
            self.errors.append(f'Expression is not iterable.')
            for_var.type = ErrorType()
        else:
            # If the expression type is iterable, assign the type of the current item as the variable's type.
            for_var.type = iter_t.get_method('current').return_type

        return self.visit(node.body)  # Visit the body of the loop to infer and return its type.

    @visitor.when(LetNode)
    def visit(self, node: LetNode):
        for decl in node.var_decl:
            self.visit(decl)
        return self.visit(node.body)

    @visitor.when(AssignNode)
    def visit(self, node: AssignNode):
        if node.identifier == 'self':  #Could cause error because should be node.identifier.identifier
            # Prevent assignment to the special 'self' identifier, which is reserved for object instances.
            self.errors.append('Cannot assign to "self".')
            return self.current_type

        var = node.scope.find_variable(node.identifier)
        if var is None:
            # If the variable is not found in the current scope, log an error and return an ErrorType.
            self.errors.append(f'Variable "{node.identifier}" is not defined.')
            return ErrorType()
        
        exp_t = self.visit(node.exp)
        if var.type.name != IntrinsicType().name:
            return var.type
        var = node.scope.find_variable(var.name)
        var.type = exp_t
        
        return exp_t

    @visitor.when(NewNode)
    def visit(self, node: NewNode):
        try:
            # Attempt to retrieve the type from the context using the node's type_name."
            new_t = self.context.get_type(node.identifier)
            args_t = [self.visit(arg) for arg in node.args]            
        except SemanticError:
            # If the type cannot be found in the context, log an error and return an ErrorType.
            # self.errors.append(f'Type "{node.type_name}" is not defined.')
            return ErrorType()
        
        if new_t is ErrorType():
            return ErrorType()

        newt_attr = [attr for attr in new_t.attributes if (attr.name.startswith('PS') and attr.name.endswith('PE'))]
        if len(args_t) != len(newt_attr):
            self.errors.append(f'Error while instantiating type. Expected {len(newt_attr)} arguments but got {len(args_t)} in "{node.type_name}"')
            return ErrorType()
       
        return new_t

    @visitor.when(IndexNode)
    def visit(self, node: IndexNode):
        object_t = self.visit(node.exp)
        index_t = self.visit(node.index)

        if not isinstance(object_t, VectorType):
            self.errors.append(f'Indexing is only supported on vectors.')
            return ErrorType()
        return object_t.element_type

    @visitor.when(VectorNode)
    def visit(self, node: VectorNode):
        item_t = [self.visit(exp) for exp in node.exp_list]
        fca = get_fca(item_t)
        if type(fca) == ErrorType():
            return ErrorType()
        vtype = VectorType(fca)
        vtype.set_parent(self.context.get_type('Iterable'))
        return vtype

    @visitor.when(VectorComprNode)
    def visit(self, node: VectorComprNode):
        it_t = self.visit(node.iter_exp)

        if not it_t.conforms_to(self.context.get_type('Iterable')):
            self.errors.append(f'Expression is not iterable because it does not conform to Iterable Protocol')
            return ErrorType()

        ret_t = self.visit(node.exp)
        if ret_t is ErrorType():
            return ErrorType()
        return VectorType(ret_t)