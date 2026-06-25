import os
import sys

# Ensure modules can be imported
sys.path.append(os.path.abspath(os.path.dirname(__file__)))

from agents.solver_agent import SolverAgent
from agents.reflection_agent import ReflectionAgent
from agents.verification_agent import VerificationAgent
from agents.qa_agent import QAAgent
from agents.debug_agent import DebugAgent
from agents.testcase_agent import TestCaseAgent
from agents.complexity_agent import ComplexityAgent
from agents.explanation_agent import ExplanationAgent
from agents.strategy_agent import StrategyAgent
from agents.interview_agent import InterviewAgent
from agents.code_review_agent import CodeReviewAgent
from agents.company_agent import CompanyAgent
from agents.hidden_test_agent import HiddenTestAgent

def test_agent(name, agent_class, *args, **kwargs):
    print(f"\n--- Testing {name} ---")
    try:
        agent = agent_class()
        result = agent.run(*args, **kwargs)
        if "error" in result:
            print(f"[{name}] ERROR: {result['error']}")
            return {"error": result["error"]}
        else:
            print(f"[{name}] SUCCESS. Result keys: {list(result.keys())}")
            return result
    except Exception as e:
        print(f"[{name}] CRASH: {str(e)}")
        return {"error": str(e)}

def main():
    prob = "Reverse a linked list in O(N) time and O(1) space."
    code = "def reverseList(head):\n  prev = None\n  while head:\n    nxt = head.next\n    head.next = prev\n    prev = head\n    head = nxt\n  return prev"
    
    results = {}
    
    results["SolverAgent"] = test_agent("SolverAgent", SolverAgent, prob, "")
    results["ReflectionAgent"] = test_agent("ReflectionAgent", ReflectionAgent, prob, code)
    results["VerificationAgent"] = test_agent("VerificationAgent", VerificationAgent, prob, code)
    results["QAAgent"] = test_agent("QAAgent", QAAgent, '{"status": "test data"}')
    results["DebugAgent"] = test_agent("DebugAgent", DebugAgent, prob, "def reverseList(head):\n return head", "Does not reverse.")
    results["TestCaseAgent"] = test_agent("TestCaseAgent", TestCaseAgent, prob)
    results["ComplexityAgent"] = test_agent("ComplexityAgent", ComplexityAgent, prob, code)
    results["ExplanationAgent"] = test_agent("ExplanationAgent", ExplanationAgent, code, "Beginner")
    results["StrategyAgent"] = test_agent("StrategyAgent", StrategyAgent, "Codeforces Div 2 Round 100")
    results["InterviewAgent"] = test_agent("InterviewAgent", InterviewAgent, prob, "def reverseList(head): pass")
    results["CodeReviewAgent"] = test_agent("CodeReviewAgent", CodeReviewAgent, code)
    results["CompanyAgent"] = test_agent("CompanyAgent", CompanyAgent, "Google", code)
    results["HiddenTestAgent"] = test_agent("HiddenTestAgent", HiddenTestAgent, code)
    
    failed = [k for k, v in results.items() if "error" in v]
    
    import json
    with open("agent_examples.json", "w") as f:
        json.dump(results, f, indent=4)
        
    print("\n\n=== TEST SUMMARY ===")
    if failed:
        print(f"Failed Agents: {', '.join(failed)}")
        sys.exit(1)
    else:
        print("All agents executed successfully and results saved to agent_examples.json!")
        sys.exit(0)

if __name__ == "__main__":
    main()
