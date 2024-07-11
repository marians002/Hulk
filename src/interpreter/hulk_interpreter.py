
import sys
sys.path.append('/home/carlosbreso/Data/Code/Python/HulkCompiler/Hulk/src/'
                )
import cmp.visitor as visitor
from cmp.ast_for_hulk import *
from cmp.semantic import *
from random import uniform

def getBody(body):
    # Para recorrer lista o 
    if not isinstance(body, list):
        return iter([body])
    else:
        return iter(body)
    
class Interpreter:
    def __init__(self, types):
        self.context: Context = Context()
        self.current_props = {}
        self.current_funcs = {}
        self.current_type: TypeNode = None
        # A method
        self.current_func: FunctionNode = None
        self.types = types
        
    @visitor.on('node')
    def visit(self, node, scope=None):
        pass
    
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        program_scope = node.scope

        statements = to_list(node.decl_list)
        for stat in statements:
            self.visit(stat, program_scope)
        
        body = to_list(node.global_exp)
        expr_value =  self.get_last_value(body, program_scope)
        return expr_value
    ####################### DECLARATIONS ############################
    
    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: Scope):
        body_scope : Scope = Scope(scope)

        class defined_type:
            def __init__(self, interpreter : Interpreter,*args):
                interpreter.current_type = node
                self.props = {}
                self.funcs = {}
                self.args = list(args)
                self.parent = None
                self.type_name = node.id

                for i in range(len(node.params)):
                    param_name = node.params[i].token
                    # args already evaluated
                    param_value = self.args[i]
                    body_scope.define_variable(param_name, param_value)

                # Set parent case
                if node.inherits is not None:
                    parent_type = interpreter.context.get_type(node.inherits)

                    parent_params = []
                    for param in node.args:
                        param = to_list(param)
                        value = interpreter.get_last_value(param, body_scope)
                        parent_params.append(value)

                    parent_params = tuple(parent_params)
                    self.parent = parent_type(interpreter, *parent_params)

                
                for item in node.attr_list:
                    value = interpreter.visit(item, body_scope) 
                    
                    # need Ast node for methods  
                    if item is FunctionNode:
                        self.funcs[item.identifier] = value
                        interpreter.current_funcs[item.identifier] = value
                    else:
                        self.props[item.identifier] = value
                        interpreter.current_props[item.identifier] = value

                interpreter.current_type = None
                    

        self.context.create_type(node.identifier, defined_type)
        self.current_props = {}
        self.current_funcs = {}
    
    # @visitor.when(InvoqueFuncNode)
    # def visit(self, node: InvoqueFuncNode, scope: Scope):
    #     body = to_list(node.exp)
    #     prop_value = self.get_last_value(body, scope)
    #     return prop_value
    
    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode, scope: Scope):
        def defined_function(scope, interpreter, current_instance, *args):
            interpreter.current_func = node
            interpreter.current_type = current_instance
            
            body_scope : Scope = Scope(scope)
            for i in range(len(node.params)):
                param_name = node.params[i].token
                param_value = args[i]
                body_scope.define_variable(param_name, param_value)

            body = to_list(node.body)
            return_value = self.get_last_value(body, body_scope)

            interpreter.current_type = None
            interpreter.current_func = None
            return return_value

        return defined_function
    
    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode, scope: Scope):
        
        param_names = []
        param_types = []
        for p in to_list(node.params):
            param_names.append(p.identifier)
            param_types.append(p.type)
        
        return_type = node.ret_type
        body = node.body

        self.context.create_function(node.identifier, param_names, param_types, return_type, body)
    
    ####################### BUILT-IN METHODS ########################
    ####################### SIMPLE EXPRESSIONS ######################
    
    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        child_scope = Scope(scope)

        assignations = to_list(node.var_decl)
        for assign in assignations:
            self.visit(assign, child_scope)

        body = to_list(node.body)
        value = self.get_last_value(body, child_scope)
        return value
    
    @visitor.when(IfNode)
    def visit(self, node: IfNode, scope: Scope):
        for condition, body in node.conditions:
            val = self.get_last_value(condition, scope)
            if val:
                return_val = self.get_last_value(body, scope)
                break
        # return val always get assigned due to else "statement"
        return return_val
    
    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        condition = self.visit(node.condition, scope)
        body = to_list(node.body)
        
        final_value = None
        while condition:
            final_value = self.get_last_value(body, scope)
            condition = self.visit(node.condition, scope)
        
        return final_value
    
    @visitor.when(ForNode)
    def visit(self, node: ForNode, scope: Scope):
        body_scope = Scope(scope)
        
        body = to_list(node.exp)
        iterable = self.get_last_value(node.exp, scope)
        
        
        body = to_list(node.body)
        
        body_scope.define_variable(node.var, None)
        
        return_value = None
        for i in iterable:
            body_scope.reassign_variable(node.var, i)
            return_value = self.get_last_value(body, body_scope)
        
        return return_value
    
    ####################### ASIGN ###################################
    
    @visitor.when(AssignNode)
    def visit(self, node: AssignNode, scope: Scope):
        body = to_list(node.body)

        value = self.get_last_value(body, scope)
        #variables store its value at self.type
        scope.define_variable(node.id, value)
    
    ## chequear el lio del self con la asignacion de destruccion destructor
    @visitor.when(DeclarationNode)
    def visit(self, node: AssignNode, scope: Scope):
        body = to_list(node.body)

        value = self.get_last_value(body, scope)
        #variables store its value at self.type
        scope.define_variable(node.id, value)
    
    ####################### Type EXPRESSIONS ########################
    
    @visitor.when(IsNode)
    def visit(self, node : IsNode, scope: Scope):
        body = to_list(node.exp)
        value : Type = self.get_last_value(body)
        
        type = self.get_type(node.type_name)
        return value.conforms_to(type)
    
    @visitor.when(AsNode)
    def visit(self, node : AsNode, scope: Scope):
        body = to_list(node.exp)
        value : Type = self.get_last_value(body)
        
        type = self.get_type(node.type_name)
        #devolver una instancia de type con los atributos de value o hacer algo similar a un casteo
        #casted_value = type(value)
        return value
    
    ####################### LOGIC EXPRESSIONS #######################
    
    @visitor.when(AndNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value and right_value
    
    @visitor.when(OrNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value or right_value
    
    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        body = to_list(node.exp)
        value = self.get_last_value(body)
        return not value
    
    ####################### STRING EXPRESSIONS #######################
    
    @visitor.when(ConcatNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value + right_value
    
    @visitor.when(PlusNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value + right_value
    
    ####################### ATOMS ####################################
    
    @visitor.when(NumberNode)
    def visit(self, node :NumberNode, scope: Scope):
        return float(node.value)
    
    @visitor.when(BoolNode)
    def visit(self, node :NumberNode, scope: Scope):
        return True if node.value == 'true' else False
    
    @visitor.when(StringNode)
    def visit(self, node :StringNode, scope: Scope):
        return str(node.value[1:-1])
    
    @visitor.when(VarNode)
    def visit(self, node: VarNode, scope: Scope):
        return scope.find_variable(node.identifier).type
    
    # not working yet
    @visitor.when(NewNode)
    def visit(self, node: NewNode, scope: Scope):
        return None
        # args = []
        # node_args = to_list(node.args)
        
        # for arg in node_args:
        #     body = to_list(arg)
        #     value = self.get_last_value(body, scope)
        #     args.append(value)

        # args = tuple(args)
        # current_type = self.context.get_type(node.type_name)
        
        # #get type
        # _type : Type = self.context.get_type(node.type_name)
        # # Recorrer el cuerpo de un type
        # type_scope = scope.create_child()
        # Assign params
        # for idx in range(len(args)):
        #     var_name = tipo.param_names[idx]
        #     var_value = args[idx]
        #     function_scope.define_variable(var_name, var_value)
        
        # # Enter function body
        # body = to_list(function.body)
        
        # return_value = self.get_last_value(body, function_scope)
        
        # instance = current_type(*args)
        # return instance
    
    @visitor.when(InvoqueFuncNode)
    def visit(self, node: InvoqueFuncNode, scope: Scope):
        
        # Evaluate arguments
        args = []
        for arg in to_list(node.args):
            arg = self.get_last_value(arg, function_scope)
            args.append(arg)

        #Search function definition
        try:
            function = self.context.get_function(node.identifier)
        except:
            # try to get a build-in func
            build_in_func = self.get_build_in_func(function.name)            
            if build_in_func != None:
               return build_in_func(*args)
        
        # Assign params
        function_scope = scope.create_child()
        for idx in range(len(args)):
            var_name = function.param_names[idx]
            var_value = args[idx]
            function_scope.define_variable(var_name, var_value)
        
        # Enter function body
        body = to_list(function.body)
        
        return_value = self.get_last_value(body, function_scope)
        return return_value
    
    @visitor.when(PropCallNode)
    def visit(self, node: PropCallNode, scope: Scope):
        #get instance
        instance = to_list(node.exp)
        instance = self.get_last_value(instance, scope)
        #get type
        instance_type = scope.find_variable(instance.name).type
        type : Type= self.context.get_type(instance_type)
        
        f : InvoqueFuncNode = node.function
        # Get args
        args = []
        for arg in to_list(f.args):
            arg = to_list(arg)
            value = self.get_last_value(arg, scope)
            args.append(value)
            
        args = tuple(args)
        
        # assign args to params
        method : Method = type.get_method(f.identifier)
        m_scope = scope.create_child()
        
        for idx in range(len(args)):
            var_name = method.param_names[idx]
            var_value = args[idx]
            m_scope.define_variable(var_name, var_value)
        
        body = to_list(method.body)
        return_value = self.get_last_value(body, m_scope)
        return return_value
    
    ####################### ARITHMETIC ###############################
    
    @visitor.when(NegativeNode)
    def visit(self, node: NegativeNode, scope: Scope):
        body = to_list(node.exp)
        value = self.get_last_value(body)
        return -value
    
    @visitor.when(PlusNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value + right_value
    
    
    @visitor.when(MinusNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value - right_value
    
    @visitor.when(ProductNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value * right_value
    
    @visitor.when(DivisionNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value / right_value
    
    @visitor.when(PowNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value ** right_value 
    
    @visitor.when(ModNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value % right_value

    ####################### COMPARISON ###############################
    
    @visitor.when(GreaterThanNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value > right_value
    
    @visitor.when(LessThanNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value < right_value
    
    @visitor.when(LessEqualNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value <= right_value
    
    @visitor.when(GreaterThanNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value > right_value
    
    @visitor.when(GreaterEqualNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value >= right_value
    
    @visitor.when(EqualNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value == right_value
    
    @visitor.when(NotEqualNode)
    def visit(self, node, scope: Scope):
        left_value, right_value = self.get_brothers(node, scope)
        return left_value != right_value
    
    
    ######################### AUXILIAR METHODS ################################ 
    def get_build_in_func(self, f_name):
        match f_name:
            case 'print':
                return print
            case 'range':
                return range
            case 'rand':
                return uniform(0, 1)
            case _:
                return None
    
    def get_last_value(self, body, scope):
        #Evaluates body and return last statement value or simply evaluates statement and return its value
        return_value = None
        for exp in body:
            if isinstance(exp, list):
                return_value = self.get_last_value(exp, scope)
            else:
                return_value = self.visit(exp, scope)
        return return_value
        
    def get_type(self, value):
        value_type: Type = None
        if isinstance(value, bool):
            value_type = self.context.get_type("Boolean")
        elif isinstance(value, str):
            value_type = self.context.get_type("String")
        elif isinstance(value, int) or isinstance(value, float):
            value_type = self.context.get_type("Number")
        else:
            value_type = value.type_name

        return value_type
    
    def get_brothers(self, node, scope):
        left_body = to_list(node.left)
        right_body = to_list(node.right)
        
        left_value = self.get_last_value(left_body, scope)
        right_value = self.get_last_value(right_body, scope)
        
        return left_value, right_value

def to_list(body):
    if not isinstance(body, list):
        return [body]
    else:
        return body