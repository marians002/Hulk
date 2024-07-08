class Node:
    line = '0'


class ProgramNode(Node):
    def __init__(self, decl_list, global_exp):
        self.decl_list = decl_list
        self.global_exp = global_exp


class DeclarationNode(Node):
    pass


class ExpNode(Node):
    pass


class FunctionNode(DeclarationNode):
    def __init__(self, identifier, params, ret_type, body):
        self.identifier = identifier
        self.params = params
        self.ret_type = ret_type
        self.body = body


class TypeNode(DeclarationNode):
    def __init__(self, identifier, inherits, params, args, attr_list):
        self.identifier = identifier
        self.inherits = inherits
        self.params = params
        self.args = args
        self.attr_list = attr_list


class ProtocolNode(DeclarationNode):
    def __init__(self, identifier, extends, method_decl_col):
        self.identifier = identifier
        self.extends = extends
        self.method_decl_col = method_decl_col


class DeclareVarNode(Node):
    def __init__(self, identifier, type_name, value):
        self.identifier = identifier
        self.type_name = type_name
        self.value = value


class BlockNode(ExpNode):
    def __init__(self, statement_list):
        self.statement_list = statement_list


class AndNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class OrNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class NotNode(ExpNode):
    def __init__(self, exp):
        self.exp = exp


class ConcatNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class EqualNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class NotEqualNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class LessThanNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class LessEqualNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class GreaterThanNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class GreaterEqualNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class PlusNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class MinusNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class ProductNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class DivisionNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class ModNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class PowNode(ExpNode):
    def __init__(self, left_exp, right_exp):
        self.left_exp = left_exp
        self.right_exp = right_exp


class NegativeNode(ExpNode):
    def __init__(self, exp):
        self.exp = exp


class NumberNode(ExpNode):
    def __init__(self, value):
        self.value = value


class StringNode(ExpNode):
    def __init__(self, value):
        self.value = value


class BoolNode(ExpNode):
    def __init__(self, value):
        self.value = value


class IsNode(ExpNode):
    def __init__(self, exp, type_name):
        self.exp = exp
        self.type_name = type_name


class AsNode(ExpNode):
    def __init__(self, exp, type_name):
        self.exp = exp
        self.type_name = type_name


class VarNode(ExpNode):
    def __init__(self, identifier):
        self.identifier = identifier


class InvoqueFuncNode(ExpNode):
    def __init__(self, identifier, args):
        self.identifier = identifier
        self.args = args


class AttrCallNode(ExpNode):
    def __init__(self, exp, attribute):
        self.exp = exp
        self.attribute = attribute


class PropCallNode(ExpNode):
    def __init__(self, exp, function):
        self.exp = exp
        self.function = function


class IfNode(ExpNode):
    def __init__(self, conditions):
        self.conditions = conditions


class WhileNode(ExpNode):
    def __init__(self, condition, body):
        self.condition = condition
        self.body = body


class ForNode(ExpNode):
    def __init__(self, var, exp, body):
        self.var = var
        self.exp = exp
        self.body = body


class LetNode(ExpNode):
    def __init__(self, var_decl, body):
        self.var_decl = var_decl
        self.body = body


class AssignNode(ExpNode):
    def __init__(self, identifier, exp):
        self.identifier = identifier
        self.exp = exp


class NewNode(ExpNode):
    def __init__(self, type_name, args):
        self.type_name = type_name
        self.args = args


class IndexNode(ExpNode):
    def __init__(self, exp, index):
        self.exp = exp
        self.index = index


class VectorNode(ExpNode):
    def __init__(self, exp_list):
        self.exp_list = exp_list


class VectorComprNode(ExpNode):
    def __init__(self, exp, var, iter_exp):
        self.exp = exp
        self.var = var
        self.iter_exp = iter_exp
