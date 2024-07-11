import sys

sys.path.append('/home/marian/Documents/MATCOM/Compilación/Hulk Repo/Hulk/src')
from cmp import visitor
from cmp.ast_for_hulk import *
from cmp.semantic import *

# WRONG_SIGNATURE = 'Method "%s" already defined in "%s" with a different signature.'
# LOCAL_ALREADY_DEFINED = 'Variable "%s" is already defined in method "%s".'
# INCOMPATIBLE_TYPES = 'Cannot convert "%s" into "%s".'
# VARIABLE_NOT_DEFINED = 'Variable "%s" is not defined in "%s".'
# INVALID_OPERATION = 'Operation is not defined between "%s" and "%s".'


class ScopesFiller:
    """
    A class responsible for filling scopes during the semantic analysis phase of a compiler.

    This class traverses the abstract syntax tree (AST) and assigns scopes to nodes, allowing
    for the identification and management of variable and function declarations and their visibility
    within different parts of the program.

    Attributes:
        context (Context): The context in which the current node is being analyzed.
        current_type (Type): The current type being processed in the AST.
        current_method (Method): The current method being processed in the AST.
        errors (list): A list to accumulate error messages encountered during scope filling.
    """

    def __init__(self, context, errors=None):
        if errors is None:
            errors = []
        self.context = context
        self.current_type = None
        self.errors = errors

    @visitor.on('node')
    def visit(self, node, scope: Scope):
        node.scope = scope

    @visitor.when(ProgramNode)
    def visit(self, node: ProgramNode, scope=None):
        scope = Scope()
        node.scope = scope
        for declaration in node.decl_list:
            self.visit(declaration, scope.create_child())
        self.visit(node.global_exp, scope.create_child())
        return scope

    @visitor.when(FunctionNode)
    def visit(self, node: FunctionNode, scope: Scope):
        node.scope = scope
        f_scope = scope.create_child()

        for param in node.params:
            try:
                f_scope.define_variable(param.identifier, self.context.get_type(param.type_name))
            except SemanticError as ex:
                if param.type_name:
                    self.errors.append(f"Type {param.type_name} not found.")
                else:
                    f_scope.define_variable(param.identifier, IntrinsicType())
        self.visit(node.body, f_scope)

    @visitor.when(TypeNode)
    def visit(self, node: TypeNode, scope: Scope):
        node.scope = scope
        t_scope = scope.create_child()
        self.current_type = self.context.get_type(node.identifier)

        if self.current_type is ErrorType():
            return
        
        # MANEJAR PARAMETROS DEL PADRE
        
        # region TYPE NODE
        
        
        
        
        
        
        # region FIX THIS

        for param in node.params:
            try:
                t_scope.define_variable(param.identifier, self.context.get_type(param.identifier))
            except SemanticError:
                node.scope.define_variable(param.identifier, IntrinsicType())
        for attr in node.attr_list:
            self.visit(attr, t_scope)
        
        # Manejar self:
        m_scope = scope.create_child()
        m_scope.define_variable('self', SelfType(self.current_type))
        # methods = [method for method in node.attr_list if isinstance...]
        
        self.current_type = None

    @visitor.when(ProtocolNode)
    def visit(self, node: ProtocolNode, scope: Scope):
        node.scope = scope
        p_scope = scope.create_child()
        self.current_type = self.context.get_type(node.identifier)
        for method in node.method_decl_col:
            self.visit(method, p_scope)
        self.current_type = None

    @visitor.when(DeclareVarNode)
    def visit(self, node: DeclareVarNode, scope: Scope):
        node.scope = scope
        try:
            type = self.context.get_type(node.type_name)
        except SemanticError:
            if node.type_name:
                self.errors.append(f"Type {node.type_name} not found.")
            type = IntrinsicType()

        scope.define_variable(node.identifier, type)
        self.visit(node.value, scope.create_child())

    @visitor.when(BlockNode)
    def visit(self, node: BlockNode, scope: Scope):
        node.scope = b_scope = scope.create_child()
        for statement in node.statement_list:
            self.visit(statement, b_scope.create_child())

    @visitor.when(AndNode)
    def visit(self, node: AndNode, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(OrNode)
    def visit(self, node: OrNode, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(NotNode)
    def visit(self, node: NotNode, scope: Scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())

    @visitor.when(ConcatNode)
    def visit(self, node: ConcatNode, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(EqualNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(NotEqualNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(LessEqualNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(LessThanNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(LessEqualNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(GreaterThanNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(GreaterEqualNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(PlusNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(MinusNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(ProductNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(DivisionNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(ModNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(PowNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.left_exp, scope.create_child())
        self.visit(node.right_exp, scope.create_child())

    @visitor.when(NegativeNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())

    @visitor.when(NumberNode)
    def visit(self, node, scope: Scope):
        node.scope = scope

    @visitor.when(StringNode)
    def visit(self, node, scope: Scope):
        node.scope = scope

    @visitor.when(BoolNode)
    def visit(self, node, scope: Scope):
        node.scope = scope

    @visitor.when(IsNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())

    @visitor.when(AsNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())

    @visitor.when(VarNode)
    def visit(self, node, scope: Scope):
        node.scope = scope

    @visitor.when(InvoqueFuncNode)
    def visit(self, node: InvoqueFuncNode, scope: Scope):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(AttrCallNode)
    def visit(self, node: AttrCallNode, scope: Scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())

    @visitor.when(PropCallNode)
    def visit(self, node: PropCallNode, scope: Scope):
        node.scope = scope
        # print("visit del property call node")
        self.visit(node.exp, scope.create_child())
        self.visit(node.function, scope.create_child())

    @visitor.when(IfNode)
    def visit(self, node, scope: Scope):
        node.scope = scope
        for case, instruction in node.conditions:
            intern_scope = scope.create_child()
            self.visit(case, intern_scope)
            self.visit(instruction, intern_scope)

    @visitor.when(WhileNode)
    def visit(self, node: WhileNode, scope: Scope):
        node.scope = scope
        self.visit(node.condition, scope.create_child())
        self.visit(node.body, scope.create_child())

    @visitor.when(ForNode)
    def visit(self, node: ForNode, scope: Scope):
        node.scope = scope
        f_scope = scope.create_child()
        f_scope.define_variable(node.var, IntrinsicType())
        self.visit(node.exp, f_scope.create_child())
        self.visit(node.body, f_scope)

    @visitor.when(LetNode)
    def visit(self, node: LetNode, scope: Scope):
        node.scope = l_scope = scope
        for decl in node.var_decl:
            self.visit(decl, l_scope)
            l_scope = decl.scope
        self.visit(node.body, l_scope.create_child())

    @visitor.when(NewNode)
    def visit(self, node: NewNode, scope: Scope):
        node.scope = scope
        for arg in node.args:
            self.visit(arg, scope.create_child())

    @visitor.when(IndexNode)
    def visit(self, node: IndexNode, scope: Scope):
        node.scope = scope
        self.visit(node.exp, scope.create_child())
        self.visit(node.index, scope.create_child())

    @visitor.when(VectorNode)
    def visit(self, node: VectorNode, scope: Scope):
        node.scope = scope
        for exp in node.exp_list:
            self.visit(exp, scope.create_child())

    @visitor.when(VectorComprNode)
    def visit(self, node: VectorComprNode, scope: Scope):
        node.scope = scope
        vc_scope = scope.create_child()
        vc_scope.define_variable(node.var, IntrinsicType())
        self.visit(node.exp, vc_scope)
        self.visit(node.iter_exp, scope.create_child())
