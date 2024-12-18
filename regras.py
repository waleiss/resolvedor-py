simbolos = ['→', '↔', '~', '∧', '∨']

"""

Rules of inference in propositional logic:

1. Modus Ponens (MP): From a conditional statement (p → q) and its antecedent (p), infer the consequent (q). Formally: (p → q), p ⊢ q

2. Modus Tollens (MT): From a conditional statement (p → q) and its negation (¬q), infer the negation of the antecedent (¬p). Formally: (p → q), ¬q ⊢ ¬p

3. Hypothetical Syllogism (HS): From two conditional statements (p → q) and (q → r), infer a new conditional statement (p → r). Formally: (p → q), (q → r) ⊢ (p → r)

4. Disjunctive Syllogism (DS): From a disjunction (p ∨ q) and its negation (¬p), infer the other disjunct (q). Formally: (p ∨ q), ¬p ⊢ q

5. Exportation: From a conditional statement (p → q) and a disjunction (r ∨ s), infer a new conditional statement (p → (r ∨ s)). Formally: (p → q), (r ∨ s) ⊢ (p → (r ∨ s))

6. Simplification: From a conjunction (p ∧ q), infer either conjunct (p or q). Formally: (p ∧ q) ⊢ p or (p ∧ q) ⊢ q

7. Conjunction Elimination: From a conjunction (p ∧ q), infer the other conjunct (q). Formally: (p ∧ q) ⊢ q

8. Disjunction Introduction: From two statements (p and q), infer their disjunction (p ∨ q). Formally: p, q ⊢ p ∨ q

9. Biconditional Introduction: From two conditional statements (p → q) and (q → p), infer their biconditional (p ↔ q). Formally: (p → q), (q → p) ⊢ p ↔ q

Regras Restritas: elim dupla negacao, conjunction association 


LISTA DE REGRAS USADAS NO SISTEMA ANTERIOR: 

public class RuleNames {

	public static List<String> list() {
		List<String> all = new ArrayList<String>();
		all.add("Associatividade");
		all.add("Comutacao");
		all.add("Conjuncao");// Conjunção
		all.add("De Morgan");
		all.add("Dilema Construtivo");// Dilema Construtivo
		all.add("Distributividade");
		all.add("Dupla Negacao");
		all.add("Equivalencia Material");
		all.add("Exportacao");
		all.add("Implicacao Material");
		all.add("Modus Ponens");// Modus Ponens
		all.add("Modus Tollens");
		all.add("Silogismo Disjuntivo");// Silogismo Disjuntivo
		all.add("Silogismo Hipotetico");// Silogismo Hipotético
		all.add("Simplificacao");
		all.add("Transposicao");
		return all;
	}

}
"""