import pytest
from app.evaluators.correctness_evaluator import CorrectnessEvaluator
from app.evaluators.maintainability_evaluator import MaintainabilityEvaluator
from app.evaluators.security_evaluator import SecurityEvaluator

def test_correctness_evaluator():
    evaluator = CorrectnessEvaluator()
    
    # Test valid code
    valid_code = "def hello():\n    return 'Hello, World!'"
    result = evaluator.evaluate(valid_code)
    assert result["results"]["syntax_valid"] is True
    
    # Test invalid code
    invalid_code = "def hello():\n    print('Hello, World!\n)"
    result = evaluator.evaluate(invalid_code)
    assert result["results"]["syntax_valid"] is False

def test_maintainability_evaluator():
    evaluator = MaintainabilityEvaluator()
    
    # Test simple code
    simple_code = "def add(a, b):\n    return a + b"
    result = evaluator.evaluate(simple_code)
    assert result["results"]["cyclomatic_complexity"]["average"] == 1
    assert result["results"]["maintainability_index"] > 0

def test_security_evaluator():
    evaluator = SecurityEvaluator()
    
    # Test code with potential security issue
    vulnerable_code = "import os\ndef execute_command(cmd):\n    os.system(cmd)"
    result = evaluator.evaluate(vulnerable_code)
    assert len(result["results"]["security_issues"]) > 0
    assert result["results"]["security_score"] < 100
