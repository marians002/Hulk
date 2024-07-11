import sys

sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/src')
from cmp import visitor
from cmp.ast_for_hulk import *
from cmp.semantic import *

INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
INCOMPATIBLE_ARGS = 'Incompatible argument type "%s" for parameter type "%s"'

def check_id(node):
    return node.identifier.startswith('<error')

class TypeChecker:

    def __init__(self, context, errors=None):
        if errors is None:
            errors = []
        self.context = context
        self.errors = errors
        self.current_type = None
        self.current_function = None


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
        self.current_function = node.identifier
        if check_id(node):
            return node.ret_type
        if self.current_type:
            method = self.current_type.get_method(node.identifier)
        else:
            method = self.context.get_type('Function').get_method(node.identifier)
        b_type = self.visit(node.body)
        if node.ret_type and node.ret_type is not IntrinsicType().name:
            node.scope.ret_type = self.context.get_type(node.ret_type)
        else:
            node.scope.ret_type = b_type

        # Checking covariance
        if node.body:
            is_covariant = b_type == IntrinsicType() or node.scope.ret_type == IntrinsicType() or node.scope.ret_type.conforms_to(b_type)
            if not is_covariant:
                self.errors.append(f'Incompatible return type in method "{node.identifier}"')
        self.current_function = None
                 
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode):
        if check_id(node):
            return
        self.current_type = self.context.get_type(node.identifier)
        for attr in node.attr_list:
            self.visit(attr)
        self.current_type = None

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode):
        if check_id(node):
            return
        self.current_type = self.context.get_type(node.identifier)
        for method in node.method_list:
            self.visit(method)
        self.current_type = None

    @visitor.when(DeclareVarNode)
    def visit(self, node: DeclareVarNode):
        if check_id(node):
            return
        if node.identifier == 'self':
            return self.current_type
        
        if node.type_name:
            try:
                var_t = node.scope.find_variable(node.identifier).type
            except SemanticError as e:
                self.errors.append(e)
                var_t = ErrorType()
        else:
            var_t = IntrinsicType()
        
        exp_t = self.visit(node.value)
        if not exp_t.conforms_to(var_t):
            self.errors.append(f'Incompatible types in variable "{node.identifier}". {INCOMPATIBLE_TYPES % (exp_t, var_t)}')
            var_t = ErrorType()
        return var_t

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode):
        exp_t = ErrorType()
        for statement in node.statement_list:
            exp_t = self.visit(statement)
        return exp_t
    
    @visitor.when(AndNode)
    def visit(self, node: AndNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        bool_t = self.context.get_type('Boolean')
        if left_t != bool_t or right_t != bool_t:
            self.errors.append('Both sides of the AND expression must be boolean. Left: %s, Right: %s' % (left_t.name, right_t.name))
            return ErrorType()
        return bool_t

    @visitor.when(OrNode)
    def visit(self, node: OrNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        bool_t = self.context.get_type('Boolean')
        if left_t != bool_t or right_t != bool_t:
            self.errors.append('Both sides of the OR expression must be boolean. Left: %s, Right: %s' % (left_t.name, right_t.name))
            return ErrorType()
        return bool_t

    @visitor.when(NotNode)
    def visit(self, node: NotNode):
        exp_t = self.visit(node.exp)
        bool_t = self.context.get_type('Boolean')
        if exp_t != bool_t:
            self.errors.append('Expression inside NOT must be boolean instead of %s' % exp_t.name)
            return ErrorType()
        return bool_t
            
    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)

        str_t = self.context.get_type('String')
        num_t = self.context.get_type('Number')
        concat_list = [str_t, num_t, IntrinsicType()]
        if left_t not in concat_list or right_t not in concat_list:
            self.errors.append(f'Cannot concatenate {left_t.name} and {right_t.name}')
            return ErrorType()
        return str_t

    @visitor.when(EqualNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot compare {left_t.name} and {right_t.name}')
            return ErrorType()
        return self.context.get_type('Boolean')

    @visitor.when(NotEqualNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot compare {left_t.name} and {right_t.name}')
            return ErrorType()
        return self.context.get_type('Boolean')

    @visitor.when(LessEqualNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot compare {left_t.name} and {right_t.name}')
            return ErrorType()
        return self.context.get_type('Boolean')

    @visitor.when(LessThanNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot compare {left_t.name} and {right_t.name}')
            return ErrorType()
        return self.context.get_type('Boolean')

    @visitor.when(LessEqualNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot compare {left_t.name} and {right_t.name}')
            return ErrorType()
        return self.context.get_type('Boolean')

    @visitor.when(GreaterThanNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot compare {left_t.name} and {right_t.name}')
            return ErrorType()
        return self.context.get_type('Boolean')

    @visitor.when(GreaterEqualNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot compare {left_t.name} and {right_t.name}')
            return ErrorType()
        return self.context.get_type('Boolean')

    @visitor.when(PlusNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot add {left_t.name} and {right_t.name}')
            return ErrorType()
        return num_t

    @visitor.when(MinusNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot subtract {left_t.name} and {right_t.name}')
            return ErrorType()
        return num_t

    @visitor.when(ProductNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot multiply {left_t.name} and {right_t.name}')
            return ErrorType()
        return num_t

    @visitor.when(DivisionNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot divide {left_t.name} and {right_t.name}')
            return ErrorType()
        return num_t

    @visitor.when(ModNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot apply modulo to {left_t.name} and {right_t.name}')
            return ErrorType()
        return num_t

    @visitor.when(PowNode)
    def visit(self, node):
        left_t = self.visit(node.left_exp)
        right_t = self.visit(node.right_exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if left_t not in valid_t or right_t not in valid_t:
            self.errors.append(f'Cannot raise {left_t.name} to the power of {right_t.name}')
            return ErrorType()
        return num_t

    @visitor.when(NegativeNode)
    def visit(self, node):
        exp_t = self.visit(node.exp)
        num_t = self.context.get_type('Number')
        valid_t = [num_t, IntrinsicType()]
        if exp_t not in valid_t:
            self.errors.append(f'Cannot negate {exp_t.name}')
            return ErrorType()
        return num_t

    @visitor.when(NumberNode)
    def visit(self, node):
        return self.context.get_type('Number')

    @visitor.when(StringNode)
    def visit(self, node):
        return self.context.get_type('String')

    @visitor.when(BoolNode)
    def visit(self, node):
        return self.context.get_type('Boolean')

    @visitor.when(IsNode)
    def visit(self, node: IsNode):
        self.visit(node.exp)
        return self.context.get_type('Boolean')

    @visitor.when(AsNode)
    def visit(self, node: AsNode):
        exp_t = self.visit(node.exp)
        try:
            cast_t = self.context.get_type(node.type_name)
        except SemanticError as e:
            self.errors.append(e)
            cast_t = ErrorType()

        if not exp_t.conforms_to(cast_t) and not cast_t.conforms_to(exp_t):
            self.errors.append(f'Incompatible types in cast. Cannot cast {exp_t.name} to {cast_t.name}')
            return ErrorType()
        return cast_t

    @visitor.when(VarNode)
    def visit(self, node: VarNode):
        if node.identifier == 'self':
            return self.current_type
        try:
            var_t = node.scope.find_variable(node.identifier).type
        except SemanticError as e:
            self.errors.append(e)
            var_t = ErrorType()
        return var_t

    @visitor.when(InvoqueFuncNode)
    def visit(self, node: InvoqueFuncNode):
        args_t = [self.visit(arg) for arg in node.args]
        
        if node.identifier == 'base':
            if not self.current_type.parent:
                self.errors.append(f'Cannot use "base" in class "{self.current_type.name}"')
                return ErrorType()
            else:
                current_name = self.current_type.parent.name
                function_name = self.current_function
        else:
            current_name = 'Function'
            function_name = node.identifier
        
        try:
            function = self.context.get_type(current_name).get_method(function_name)
        except SemanticError as e:
            self.errors.append(e)
            self.visit(arg for arg in node.args)
            return ErrorType()
        
        for arg_t, param_t in zip(args_t, function.param_types):
            is_contravariant = arg_t == IntrinsicType() or param_t == IntrinsicType() or arg_t.conforms_to(param_t)
            if not is_contravariant:
                self.errors.append(INCOMPATIBLE_ARGS % (arg_t, param_t))
                return ErrorType()
        
        return function.return_type

    @visitor.when(AttrCallNode)
    def visit(self, node: AttrCallNode):
        try:
            attr = self.visit(node.exp).get_attribute(node.identifier)
            return attr.type
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

    @visitor.when(PropCallNode)
    def visit(self, node: PropCallNode):
        obj_t = self.visit(node.exp)
        try:
            return obj_t.get_method(node.function).return_type
            
        except SemanticError as e:
            if obj_t != IntrinsicType():                
                self.errors.append(e)
            return ErrorType()

    @visitor.when(IfNode)
    def visit(self, node):
        types_list = []
        for cond, body in node.conditions:
            cond_t = self.visit(cond)
            if cond_t != self.context.get_type('Boolean'):
                self.errors.append('Condition must be a boolean expression')           
            types_list.append(self.visit(body))  # Can contain Error Types
        return get_fca(types_list)
    
    @visitor.when(WhileNode)
    def visit(self, node: WhileNode):
        cond_t = self.visit(node.condition)
        if cond_t != self.context.get_type('Boolean'):
            self.errors.append('Condition must be a boolean expression')
        return self.visit(node.body)

    @visitor.when(ForNode)
    def visit(self, node: ForNode):
        it_t = self.visit(node.exp)
        it_prot = self.context.get_type('Iterable')
        if not it_t.conforms_to(it_prot):
            self.errors.append(f'Cannot iterate over {it_t.name} because it does not conform to Iterable Protocol')

        try:
            var_t = self.context.get_type(node.var.identifier)
        except SemanticError as e:
            var_t = IntrinsicType()
        return self.visit(node.body)

    @visitor.when(LetNode)
    def visit(self, node: LetNode):
        for decl in node.var_decl:
            self.visit(decl)
        return self.visit(node.body)

    @visitor.when(NewNode)
    def visit(self, node: NewNode):
        try:
            new_t = self.context.get_type(node.type_name)
        except SemanticError as e:
            self.errors.append(e)
            return ErrorType()

        args_t = [self.visit(arg) for arg in node.args]

        if len(args_t) != len(new_t.param_types):
            self.errors.append(f'Incorrect number of arguments for type "{new_t.name}"')
            return ErrorType()

        for arg_t, param_t in zip(args_t, new_t.param_types):
            if not arg_t.conforms_to(param_t):
                self.errors.append(INCOMPATIBLE_ARGS % (arg_t, param_t))
                return ErrorType()
            
        return new_t

    @visitor.when(IndexNode)
    def visit(self, node: IndexNode):
        index_t = self.visit(node.index)
        if index_t != self.context.get_type('Number'):
            self.errors.append('Index must be a number instead of %s' % index_t.name)
            return ErrorType()
        obj_t = self.visit(node.exp)
        if not isinstance(obj_t, VectorType):
            self.errors.append('Cannot index over %s' % obj_t.name)
            return ErrorType()
        
        return obj_t.element_type

    @visitor.when(VectorNode)
    def visit(self, node: VectorNode):
        exps_t = [self.visit(exp) for exp in node.exp_list]
        fca = get_fca(exps_t)
        if type(fca) == ErrorType:
            return ErrorType()
        vector_t = VectorType(fca).set_parent(self.context.get_type('Iterable'))
        return vector_t

    @visitor.when(VectorComprNode)
    def visit(self, node: VectorComprNode):
        it_t = self.visit(node.iter_exp)
        it_prot = self.context.get_type('Iterable')
        if not it_t.conforms_to(it_prot):
            self.errors.append(f'Cannot iterate over {it_t.name} because it does not conform to Iterable Protocol')
            return ErrorType()
        
        ret_t = self.visit(node.exp)
        if ret_t == ErrorType:
            return ErrorType()
        return VectorType(ret_t)
