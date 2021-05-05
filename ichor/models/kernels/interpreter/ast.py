from abc import ABC
from ichor.models.kernels.interpreter.token_type import TokenType
from typing import Dict
from ichor.models.kernels.kernel import Kernel
from ichor.models.kernels.constant import Constant


class ASTNode(ABC):
    def visit(self, global_state: Dict[str, Kernel]) -> Kernel:
        raise NotImplementedError(f"No visit method implemented for '{type(self).__name__}'")


class BinOp(ASTNode):
    def __init__(self, left, op, right):
        self.left = left
        self.token = self.op = op
        self.right = right

    def visit(self, global_state: Dict[str, Kernel]) -> Kernel:
        if self.op.type == TokenType.Plus:
            return self.left.visit(global_state) + self.right.visit(global_state)
        elif self.op.type == TokenType.Minus:
            raise NotImplementedError("Error: Not implemented minus kernel")
        elif self.op.type == TokenType.Mul:
            return self.left.visit(global_state) * self.right.visit(global_state)
        elif self.op.type == TokenType.Div:
            raise NotImplementedError("Error: Not implemented divide kernel")


class UnaryOp(ASTNode):
    def __init__(self, op, expr):
        self.token = self.op = op
        self.expr = expr

    def visit(self, global_state: Dict[str, Kernel]) -> Kernel:
        if self.op.type == TokenType.Plus:
            return self.expr.visit(global_state)
        elif self.op.type == TokenType.Minus:
            raise NotImplementedError("Error: Not implemented minus kernel")


class Var(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def visit(self, global_state: Dict[str, Kernel]) -> Kernel:
        val = global_state.get(self.value)
        if val is not None:
            return val
        else:
            raise NameError(f"{self.value} not defined")


class Num(ASTNode):
    def __init__(self, token):
        self.token = token
        self.value = token.value

    def visit(self, global_state: Dict[str, Kernel]) -> Kernel:
        return Constant(self.value)