import sys

sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/')
from src.cmp import visitor
from src.cmp.ast_for_hulk import *
from src.cmp.semantic import *

WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
SELF_IS_READONLY = 'Variable "self" is read-only.'
LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'


class TypeChecker:
    def __init__(self, context, errors=[]):
        self.context = context
        self.current_type = None
        self.current_method = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope):
        pass

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope=None):
        scope = Scope()
        for declaration in node.decl_list:
            self.visit(declaration, scope.create_child())
        return scope

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode, scope):
        node.scope = scope
        f_scope = scope.create_child()

        for param in node.params:
            f_scope.define_variable(param.identifier, self.context.get_type(param.type_name))
            if param.identifier == "self":
                self.errors.append(SELF_IS_READONLY)

        self.visit(node.body, f_scope)

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope):
        node.scope = scope
        t_scope = scope.create_child()
        self.current_type = self.context.get_type(node.identifier)
        # attributes = self.current_type.all_attributes()
        for attr in node.attr_list:
            self.visit(attr, scope)
        self.current_type = None

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode, scope):
        pass

    @visitor.when(DeclareVarNode)
    def visit(self, node, scope):
        pass

    @visitor.when(BlockNode)
    def visit(self, node, scope):
        pass

    @visitor.when(AndNode)
    def visit(self, node, scope):
        pass

    @visitor.when(OrNode)
    def visit(self, node, scope):
        pass

    @visitor.when(NotNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ConcatNode)
    def visit(self, node, scope):
        pass

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        pass

    @visitor.when(LessEqualNode)
    def visit(self, node, scope):
        pass

    @visitor.when(LessThanNode)
    def visit(self, node, scope):
        pass

    @visitor.when(LessEqualNode)
    def visit(self, node, scope):
        pass

    @visitor.when(GreaterThanNode)
    def visit(self, node, scope):
        pass

    @visitor.when(GreaterEqualNode)
    def visit(self, node, scope):
        pass

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        pass

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ProductNode)
    def visit(self, node, scope):
        pass

    @visitor.when(DivisionNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ModNode)
    def visit(self, node, scope):
        pass

    @visitor.when(PowNode)
    def visit(self, node, scope):
        pass

    @visitor.when(NegativeNode)
    def visit(self, node, scope):
        pass

    @visitor.when(NumberNode)
    def visit(self, node, scope):
        pass

    @visitor.when(StringNode)
    def visit(self, node, scope):
        pass

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        pass

    @visitor.when(IsNode)
    def visit(self, node, scope):
        pass

    @visitor.when(AsNode)
    def visit(self, node, scope):
        pass

    @visitor.when(VarNode)
    def visit(self, node, scope):
        pass

    @visitor.when(InvoqueFuncNode)
    def visit(self, node, scope):
        pass

    @visitor.when(AttrCallNode)
    def visit(self, node, scope):
        pass

    @visitor.when(PropCallNode)
    def visit(self, node, scope):
        pass

    @visitor.when(IfNode)
    def visit(self, node, scope):
        pass

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        pass

    @visitor.when(ForNode)
    def visit(self, node, scope):
        pass

    @visitor.when(LetNode)
    def visit(self, node, scope):
        pass

    @visitor.when(NewNode)
    def visit(self, node, scope):
        pass

    @visitor.when(IndexNode)
    def visit(self, node, scope):
        pass

    @visitor.when(VectorNode)
    def visit(self, node, scope):
        pass

    @visitor.when(VectorComprNode)
    def visit(self, node, scope):
        pass

