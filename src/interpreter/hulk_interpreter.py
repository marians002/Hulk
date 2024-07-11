
import sys
sys.path.append('/home/carlosbreso/Data/Code/Python/HulkCompiler/Hulk/src/'
                )
import cmp.visitor as visitor
from cmp.ast_for_hulk import *
from cmp.semantic import *
from interpreter.mytools import *

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
        self.current_type: TypeDefNode = None
        self.current_func: TypeFuncDefNode = None
        self.types = types
        
    @visitor.on('node')
    def visit(self, node, scope=None):
        pass
    
    
    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode):
        program_scope = self.context.scope

        statements = to_list(node.statement_seq)
        for stat in statements:
            self.visit(stat, program_scope)
        
        body = to_list(node.expr)
        expr_value =  self.get_last_value(body, program_scope)
        return expr_value
    ####################### BUILT-IN METHODS ########################
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
        return scope.get_value(node.identifier)
    
    @visitor.when(InvoqueFuncNode)
    def visit(self, node: InvoqueFuncNode, scope: Scope):
        #Search function definition
        function = self.context.get_func[node.identifier]
        # visit arguments
        function_scope = scope.create_child()
        body = to_list[node.args]
        self.get_last_value(body, function_scope)
        
        body = to_list(function.body)
        
        return_value = self.get_last_value(body, function_scope)
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
        return left_value * right_value#
    
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
    def get_last_value(self, body, scope):
        #Evaluates body and return last statement value 
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
            value_type = self.types['bool']
        elif isinstance(value, str):
            value_type = self.types['string']
        elif isinstance(value, int) or isinstance(value, float):
            value_type = self.types['number']
        else:
            value_type_name = value.type_name

            self.types[value.type_name]
        return self.types[value.type_name]
    
    def get_brothers(self, node, scope):
        left_body = to_list(node.left)
        right_body = to_list(node.right)
        
        left_value = self.get_last_value(left_body, scope)
        right_value = self.get_last_value(right_body, scope)
        
        return left_value, right_value
