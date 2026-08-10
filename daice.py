import ast
import operator
import random
import re

dice_pattern = re.compile(r'(\d+)d(\d+)', re.IGNORECASE)


class DiceEvaluator:

    def __init__(self):
        self.logs = []

    def roll(self, count, sides):

        count = int(count)
        sides = int(sides)

        if count <= 0:
            raise ValueError("ダイス数は1以上")

        if sides <= 0:
            raise ValueError("面数は1以上")

        if count > 10000:
            raise ValueError("ダイス数が多すぎます")

        results = [
            random.randint(1, sides)
            for _ in range(count)
        ]

        self.logs.append(
            f"{count}d{sides} → {results} = {sum(results)}"
        )

        return str(sum(results))

    def evaluate(self, expression):

        self.logs.clear()

        replaced = dice_pattern.sub(
            lambda m: self.roll(m.group(1), m.group(2)),
            expression
        )

        tree = ast.parse(replaced, mode="eval")

        result = self.eval_ast(tree.body)

        return result, self.logs

    def eval_ast(self, node):

        operators = {
            ast.Add: operator.add,
            ast.Sub: operator.sub,
            ast.Mult: operator.mul,
            ast.Div: operator.truediv,
            ast.USub: operator.neg
        }

        if isinstance(node, ast.Constant):
            return node.value

        if isinstance(node, ast.BinOp):
            return operators[type(node.op)](
                self.eval_ast(node.left),
                self.eval_ast(node.right)
            )

        if isinstance(node, ast.UnaryOp):
            return operators[type(node.op)](
                self.eval_ast(node.operand)
            )

        raise ValueError("使用できない式です")
