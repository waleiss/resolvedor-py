from ..interfaces import Observer
from ..expression import Expression

class ConstructiveDilemma(Observer):
    def __init__(self):
        pass

    def update(self, memory):
        for implication1 in memory:
            if implication1.operator == '→':
                antecedent1 = implication1.left
                consequent1 = implication1.right

                for implication2 in memory:
                    if implication2.operator == '→' and implication2 != implication1:
                        antecedent2 = implication2.left
                        consequent2 = implication2.right

                        for disjunction in memory:
                            if disjunction.operator == '∨' and (
                                {antecedent1, antecedent2} == {disjunction.left, disjunction.right}
                            ):
                                new_disjunction = Expression(operator='∨', left=consequent1, right=consequent2)

                                if new_disjunction not in memory:
                                    memory.append(new_disjunction)
                                    print(f"Aplicando Dilema Construtivo: {implication1}, {implication2}, {disjunction} ⇒ {new_disjunction}")
                                    return

    def verify(self, memory):
        for implication1 in memory:
            if implication1.operator == '→':
                antecedent1 = implication1.left

                for implication2 in memory:
                    if implication2.operator == '→' and implication2 != implication1:
                        antecedent2 = implication2.left

                        for disjunction in memory:
                            if disjunction.operator == '∨' and (
                                {antecedent1, antecedent2} == {disjunction.left, disjunction.right}
                            ):
                                consequent1 = implication1.right
                                consequent2 = implication2.right
                                new_disjunction = Expression(operator='∨', left=consequent1, right=consequent2)

                                if new_disjunction not in memory:
                                    return True

        return False
