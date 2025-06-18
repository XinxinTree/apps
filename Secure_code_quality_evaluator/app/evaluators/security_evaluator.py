from typing import Dict, Any
from .base_evaluator import BaseEvaluator
import bandit
import ast
import json

class SecurityEvaluator(BaseEvaluator):
    """Evaluator for code security."""
    
    def evaluate(self, code: str) -> Dict[str, Any]:
        """
        Evaluate code security by checking:
        - Common security vulnerabilities
        - Best practices violations
        - Security patterns
        """
        try:
            # Parse code into AST
            tree = ast.parse(code)
            
            # Run Bandit security checks
            config = bandit.config.BanditConfig()
            b_mgr = bandit.manager.BanditManager(config, 'file')
            b_mgr.discover_files(['temp.py'], 'file')
            b_mgr.run_tests()
            
            # Get results
            results = b_mgr.get_issue_list()
            
            return self._format_results({
                "security_issues": [
                    {
                        "test_id": issue.test_id,
                        "issue_text": issue.text,
                        "severity": issue.severity,
                        "confidence": issue.confidence,
                        "line_number": issue.lineno
                    }
                    for issue in results
                ],
                "security_score": self._calculate_security_score(results)
            })
            
        except Exception as e:
            return self._format_results({
                "error": str(e),
                "security_issues": [],
                "security_score": None
            })
    
    def _calculate_security_score(self, issues):
        """Calculate a security score based on issues found."""
        if not issues:
            return 100
            
        scores = []
        for issue in issues:
            severity = issue.severity.lower()
            if severity == 'high':
                scores.append(20)
            elif severity == 'medium':
                scores.append(40)
            else:
                scores.append(60)
        
        return max(0, 100 - sum(scores) / len(issues))
