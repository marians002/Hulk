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
            self.visit(attr, t_scope)
        self.current_type = None

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode, scope):
        node.scope = scope
        p_scope = scope.create_child()
        self.current_type = self.context.get_type(node.identifier)
        for method in node.method_decl_col:
            self.visit(method, p_scope)
        self.current_type = None

    @visitor.when(DeclareVarNode)
    def visit(self, node: DeclareVarNode, scope):
        node.scope = scope
        try:
            type = self.context.get_type(node.type_name)
        except SemanticError:
            if node.type_name:
                self.errors.append(f"Type {node.type_name} not found.")
            type = self.context.get_type('Object')

        if node.identifier == "self":
            self.errors.append(SELF_IS_READONLY)
            return

        scope.define_variable(node.identifier, type)
        self.visit(node.value, scope)

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope):
        b_scope = scope.create_child()
        node.scope = b_scope

        for statement in node.statement_list:
            self.visit(statement, b_scope.create_child())

    @visitor.when(AndNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(OrNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(NotNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())

    @visitor.when(ConcatNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(EqualNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(LessEqualNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(LessThanNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(LessEqualNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(GreaterThanNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(GreaterEqualNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(PlusNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(MinusNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(ProductNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(DivisionNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(ModNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(PowNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(NegativeNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(NumberNode)
    def visit(self, node, scope):
        node.scope = scope

    @visitor.when(StringNode)
    def visit(self, node, scope):
        node.scope = scope

    @visitor.when(BoolNode)
    def visit(self, node, scope):
        node.scope = scope

    @visitor.when(IsNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())

    @visitor.when(AsNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())

    @visitor.when(VarNode)
    def visit(self, node, scope):
        node.scope = scope

    @visitor.when(InvoqueFuncNode)
    def visit(self, node, scope):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(AttrCallNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())

    @visitor.when(PropCallNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())

    @visitor.when(IfNode)
    def visit(self, node, scope):
        node.scope = scope
        for case, instructions in node.conditions:
            intern_scope = scope.create_child()
            self.visit(case, intern_scope)
            self.visit(instructions, intern_scope)

    @visitor.when(WhileNode)
    def visit(self, node, scope):
        w_scope = scope.create_child()
        node.scope = w_scope
        self.visit(node.condition, w_scope)
        self.visit(node.body, w_scope)

    @visitor.when(ForNode)
    def visit(self, node, scope):
        f_scope = scope.create_child()
        node.scope = f_scope
        f_scope.define_variable(node.var, None)
        self.visit(node.exp, f_scope)
        self.visit(node.body, f_scope)

    @visitor.when(LetNode)
    def visit(self, node, scope):
        l_scope = scope.create_child()
        node.scope = l_scope
        for var_decl in node.var_decl:
            self.visit(var_decl, l_scope)
        self.visit(node.body, l_scope)

    @visitor.when(NewNode)
    def visit(self, node, scope):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(IndexNode)
    def visit(self, node, scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())
        self.visit(node.index, scope.create_child())

    @visitor.when(VectorNode)
    def visit(self, node, scope):
        node.scope = scope
        for exp in node.exp_list:
            self.visit(exp, scope.create_child())

    @visitor.when(VectorComprNode)
    def visit(self, node, scope):
        node.scope = scope
        vc_scope = scope.create_child()
        vc_scope.define_variable(node.var, None)
        self.visit(node.exp, vc_scope)
        self.visit(node.iter_exp, scope.create_child())