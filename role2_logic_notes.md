# Role 2 — Propositional Logic: Strengths and Limitations

## Strengths
1. The knowledge base is explicit and readable: facts such as `PriceOK`, `IsItalian`, `IsDinner` and `HasNuts` are named, and the rule is written out as an IFF.
2. Model checking is simple here: for one meal every fact has a fixed truth value, so only one row of the truth table needs to be checked.
3. The rule is built only from the active requirements, so ignored fields do not create extra facts.
4. The implementation is deterministic and easy to verify against the brute-force answer key — it passed 24/24 tests.
5. The same facts and rule work for every meal and every dataset size, so the code is small and easy to explain.

## Limitations
1. Every fact is computed for every meal; there is no early stopping, so work grows as meals × active requirements.
2. In our tests the Logic solver used more evaluations than CSP — for T1 at 100 meals, 400 evaluations versus 109 for CSP.
3. It only classifies meals as matching or not; it does not rank or score them.
4. The fact names must be rebuilt for each new request, so changing the requirement format requires changing the code.
5. It cannot express uncertainty, which matters because the allergens and meal times in the dataset are only approximate keyword-derived labels.
