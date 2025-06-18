from abc import ABC, abstractmethod
from typing import Dict, Any
from datetime import datetime

class BaseEvaluator(ABC):
    """Base class for all code evaluators."""
    
    @abstractmethod
    def evaluate(self, code: str) -> Dict[str, Any]:
        """Evaluate the code and return results."""
        pass

    def _format_results(self, raw_results: Dict[str, Any]) -> Dict[str, Any]:
        """Format evaluation results into a standardized format."""
        try:
            return {
                "timestamp": datetime.now().isoformat(),
                "results": raw_results,
                "evaluator": self.__class__.__name__
            }
        except Exception as e:
            return {
                "timestamp": datetime.now().isoformat(),
                "error": str(e),
                "evaluator": self.__class__.__name__
            }
