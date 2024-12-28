from ..interfaces import Observer
from ..expression import Expression

class ConstructiveDilemma(Observer):
    def __init__(self):
        pass

    def add_to_log(self, log, memory, implication1, implication2, disjunction, new_disjunction):
        log.append(
            f"({len(log) - 1}) {new_disjunction}  Dilema Construtivo  "
            f"{memory.index(implication1) + 1}, {memory.index(implication2) + 1}, {memory.index(disjunction) + 1}"
        )

    def update(self, memory, log, conclusion=None):
        for implication1 in memory:
            if implication1.operator == '→':
                antecedent1 = implication1.left
                consequent1 = implication1.right

                for implication2 in memory:
                    if implication2.operator == '→' and implication2 != implication1:
                        antecedent2 = implication2.left
                        consequent2 = implication2.right

                        for disjunction in memory:
                            if disjunction.operator == '∨' and (antecedent1 == disjunction.left) and (antecedent2 == disjunction.right):
                                new_disjunction = Expression(operator='∨', left=consequent1, right=consequent2)

                                if new_disjunction not in memory:
                                    memory.append(new_disjunction)
                                    self.add_to_log(log, memory, implication1, implication2, disjunction, new_disjunction)
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
