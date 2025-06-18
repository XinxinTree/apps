from typing import Dict, Any
from .base_evaluator import BaseEvaluator
import radon.complexity as cc
import radon.metrics as metrics
import ast

class MaintainabilityEvaluator(BaseEvaluator):
    """Evaluator for code maintainability."""
    
    def evaluate(self, code: str) -> Dict[str, Any]:
        """
        Evaluate code maintainability by checking:
        - Cyclomatic complexity
        - Maintainability index
        - Code metrics
        """
        try:
            # Calculate cyclomatic complexity
            blocks = cc.cc_visit(code)
            avg_complexity = sum(b.complexity for b in blocks) / len(blocks) if blocks else 0
            
            # Calculate maintainability index
            mi = metrics.mi_visit(code, True)
            
            # Calculate lines of code
            lines = code.split('\n')
            
            return self._format_results({
                "cyclomatic_complexity": {
                    "average": avg_complexity,
                    "blocks": len(blocks)
                },
                "maintainability_index": mi,
                "code_metrics": {
                    "lines_of_code": len(lines),
                    "logical_lines_of_code": len([line for line in lines if line.strip()]),
                    "blank_lines": len([line for line in lines if not line.strip()])
                }
            })
            
        except Exception as e:
            return self._format_results({
                "error": str(e),
                "cyclomatic_complexity": None,
                "maintainability_index": None,
                "code_metrics": None
            })
