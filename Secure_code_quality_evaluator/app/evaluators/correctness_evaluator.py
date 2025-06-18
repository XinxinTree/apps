from typing import Dict, Any
from .base_evaluator import BaseEvaluator
import pycodestyle
import ast

class CorrectnessEvaluator(BaseEvaluator):
    """Evaluator for code correctness."""
    
    def evaluate(self, code: str) -> Dict[str, Any]:
        """
        Evaluate code correctness by checking:
        - Syntax errors
        - PEP 8 compliance
        - Basic code structure
        """
        try:
            # Check if code can be parsed
            ast.parse(code)
            
            # Check PEP 8 compliance
            style_checker = pycodestyle.Checker()
            style_checker.lines = code.splitlines(True)
            style_errors = list(style_checker.check_all())
            
            return self._format_results({
                "syntax_valid": True,
                "style_errors": style_errors,
                "pep8_compliance": len(style_errors) == 0
            })
            
        except SyntaxError as e:
            return self._format_results({
                "syntax_valid": False,
                "syntax_error": str(e),
                "style_errors": [],
                "pep8_compliance": False
            })
