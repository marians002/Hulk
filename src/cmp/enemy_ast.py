from cmp.utils import Token

class Node:
    def __init__(self, token):
        self.token = token
    def __repr__(self) -> str:
        return "Node: "+self.token

class ProgramNode(Node):
    def __init__(self, statement_seq, expr):
        self.statement_seq = statement_seq
        self.expr = expr


class StatementNode(Node):
    pass


class ExpressionNode(Node):
    pass


# body_exp = ( <exp> | <block_exp> )
class FuncDefNode(StatementNode):
    def __init__(self, id, params, body_expr, token, return_type='any'):
        self.id = id
        self.params = params
        self.body = body_expr
        self.token = token
        self.return_type = return_type


class TypeDefNode(StatementNode):
    def __init__(self, id, body, token, params=[], parent_id=None, parent_params=[], no_params=False):
        self.id = id
        self.body = body
        self.token = token
        self.params = params
        self.parent = parent_id
        self.parent_params = parent_params
        self.no_params = no_params

class TypeBodyItemNode(Node):
    pass

class TypePropDefNode(TypeBodyItemNode):
    def __init__(self, id, exp, token, type='any'):
        self.id = id
        self.exp = exp
        self.type = type
        self.token = token

class TypeFuncDefNode(TypeBodyItemNode):
    def __init__(self, id, params, body, return_type='any'):
        self.id = id
        self.params = params
        self.return_type = return_type
        self.body = body
        self.token = 'typeFuncNode'



# Use also for <destr_assignation>
class AssignationNode(Node):
    def __init__(self, id, body, token, type='any'):
        self.id = id
        self.body = body
        self.token = token
        self.type = type

class DestructiveAssignationNode(Node):
    def __init__(self, id, body, token, self_assign=False):
        self.id = id
        self.body = body
        self.token = token 
        self.self_assign = self_assign


class LetNode(ExpressionNode):
    def __init__(self, assignations, body, token):
        self.assignations = assignations
        self.body = body
        self.token = token


class IfElseNode(ExpressionNode):
    def __init__(self, condition, then_expr, else_expr, token, elif_list=[]):
        self.condition = condition
        self.then_expr = then_expr
        self.else_expr = else_expr
        self.token = token
        self.elif_list = elif_list


class ElifNode(Node):
    def __init__(self, condition, then_expr, token):
        self.condition = condition
        self.then_expr = then_expr
        self.token = token


class WhileNode(ExpressionNode):
    def __init__(self, condition, body, token):
        self.condition = condition
        self.body = body
        self.token = token


class ForNode(ExpressionNode):
    def __init__(self, id, iterable, body, token):
        self.id = id
        self.iterable = iterable
        self.body = body
        self.token = token


# class BlockNode(ExpressionNode):
#     def __init__(self, expr_list, token):
#         self.expr_list = expr_list
#         self.token = token


class RangeNode(ExpressionNode):
    def __init__(self, start, end, token):
        self.start = start
        self.end = end
        self.token = token


class PrintNode(ExpressionNode):
    def __init__(self, expr, token):
        self.expr = expr
        self.token = token


class InstanceNode(ExpressionNode):
    def __init__(self, id, params, token):
        self.id = id
        self.params = params
        self.token = token


class AtomicNode(ExpressionNode):
    pass


class CallNode(AtomicNode):
    def __init__(self, id, params):
        self.id = id
        self.params = params
        self.token = Token(id, 'functionCall')

class TypePropCallNode(AtomicNode):
    def __init__(self, type_id, prop_id):
        self.type_id = type_id
        self.prop_id = prop_id

class TypeFuncCallNode(AtomicNode):
    def __init__(self, type_id, func_id, params=[]):
        self.instance_id = type_id
        self.func_id = func_id
        self.params = params

class SelfCallPropNode(AtomicNode):
    def __init__(self,token, id):
        self.token = token
        self.id = id

class SelfCallFuncNode(AtomicNode):
    def __init__(self,token, id, params=[]):
        self.token = token
        self.id = id
        self.params = params

class BaseCallNode(AtomicNode):
    def __init__(self, token, params=[]):
        self.token = token
        self.params = params

class VarTyped(AtomicNode):
    def __init__(self, token, id, type='any'):
        self.token = token
        self.id = id
        self.type = type

class AsNode(AtomicNode):
    def __init__(self, token, expr, type):
        self.token = token
        self.expr = expr
        self.type = type

class IsNode(AtomicNode):
    def __init__(self, token, expr, type):
        self.token = token
        self.expr = expr
        self.type = type

class NumNode(AtomicNode):
    pass
class StringNode(AtomicNode):
    pass
class BoolNode(AtomicNode):
    pass
class VarNode(AtomicNode):
    pass
class RanNode(AtomicNode):
    pass


class UnaryNode(ExpressionNode):
    def __init__(self, expr, token):
        self.expr = expr
        self.token = token


class UnaryNumOperationNode(UnaryNode):
    pass
class UnaryLogicOperationNode(UnaryNode):
    pass


class NotNode(UnaryLogicOperationNode):
    pass


class BinaryNode(ExpressionNode):
    def __init__(self, left, right, token):
        self.left = left
        self.right = right
        self.token = token


class BinaryNumOperationNode(BinaryNode):
    pass
class BinaryLogicOperationNode(BinaryNode):
    pass
class BinaryStringOperationNode(BinaryNode):
    pass


class EqualDiffNode(BinaryLogicOperationNode):
    pass

class ComparisonNode(BinaryLogicOperationNode):
    pass

class AndOrNode(BinaryLogicOperationNode):
    pass


class ConcatNode(BinaryStringOperationNode):
    pass
class DoubleConcatNode(BinaryStringOperationNode):
    pass