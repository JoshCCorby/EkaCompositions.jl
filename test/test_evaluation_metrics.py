"""Independent hand-worked checks for the ranking-evaluation definitions."""

import math
import unittest
from collections import Counter
from fractions import Fraction


def system(formula):
    # The fixture declares systems explicitly below; this function is intentionally
    # independent of Julia's parser and is only a small oracle for metric arithmetic.
    return {
        "LiNaO": "Li-Na-O",
        "Li2NaO": "Li-Na-O",
        "CaTiO3": "Ca-O-Ti",
        "MgAl2O4": "Al-Mg-O",
    }[formula]


def metrics(ranking, relevant, budgets):
    relevant = set(relevant)
    relevant_systems = {system(value) for value in relevant}
    output = []
    for budget in sorted(budgets):
        selected = ranking[:budget]
        hits = [value for value in selected if value in relevant]
        counts = Counter(system(value) for value in hits)
        hit_count = len(hits)
        dcg = sum(1 / math.log2(rank + 1)
                  for rank, value in enumerate(selected, 1) if value in relevant)
        ideal = sum(1 / math.log2(rank + 1)
                    for rank in range(1, min(budget, len(relevant)) + 1))
        output.append({
            "hits": hit_count,
            "fraction": hit_count / budget,
            "recall": hit_count / len(relevant),
            "enrichment": (hit_count / budget) / (len(relevant) / len(ranking)),
            "expected": Fraction(budget * len(relevant), len(ranking)),
            "dcg": dcg,
            "ndcg": dcg / ideal,
            "selected_systems": len({system(value) for value in selected}),
            "hit_systems": len(counts),
            "system_recall": len(counts) / len(relevant_systems),
            "effective_systems": hit_count**2 / sum(value**2 for value in counts.values()) if hits else 0.0,
            "largest_hit_share": max(counts.values()) / hit_count if hits else 0.0,
        })
    return output


class EvaluationMetricTests(unittest.TestCase):
    def test_hand_worked_composition_and_system_metrics(self):
        ranking = ["LiNaO", "Li2NaO", "CaTiO3", "MgAl2O4"]
        rows = metrics(ranking, {"LiNaO", "Li2NaO", "MgAl2O4"}, [4, 1, 3, 2])
        self.assertEqual([row["hits"] for row in rows], [1, 2, 2, 3])
        self.assertEqual([row["fraction"] for row in rows], [1, 1, 2 / 3, 3 / 4])
        self.assertEqual([row["recall"] for row in rows], [1 / 3, 2 / 3, 2 / 3, 1])
        self.assertEqual([row["enrichment"] for row in rows], [4 / 3, 4 / 3, 8 / 9, 1])
        self.assertEqual([row["expected"] for row in rows],
                         [Fraction(3, 4), Fraction(3, 2), Fraction(9, 4), Fraction(3, 1)])
        self.assertEqual([row["selected_systems"] for row in rows], [1, 1, 2, 3])
        self.assertEqual([row["hit_systems"] for row in rows], [1, 1, 1, 2])
        self.assertEqual([row["system_recall"] for row in rows], [.5, .5, .5, 1])
        self.assertEqual([row["effective_systems"] for row in rows], [1, 1, 1, 1.8])
        self.assertEqual([row["largest_hit_share"] for row in rows], [1, 1, 1, 2 / 3])
        self.assertAlmostEqual(rows[2]["ndcg"],
                               (1 + 1 / math.log2(3)) / (1 + 1 / math.log2(3) + .5))
        self.assertAlmostEqual(rows[3]["ndcg"],
                               (1 + 1 / math.log2(3) + 1 / math.log2(5)) /
                               (1 + 1 / math.log2(3) + .5))

    def test_no_hit_concentration_is_zero(self):
        ranking = ["LiNaO", "Li2NaO", "CaTiO3", "MgAl2O4"]
        row = metrics(ranking, {"MgAl2O4"}, [1])[0]
        self.assertEqual((row["hits"], row["ndcg"], row["hit_systems"],
                          row["effective_systems"], row["largest_hit_share"]),
                         (0, 0, 0, 0, 0))


if __name__ == "__main__":
    unittest.main()
