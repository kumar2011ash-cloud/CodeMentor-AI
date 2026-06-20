import json
from typing import Dict, Any, Generator

from agents.base_agent import BaseAgent
from agents.solver_agent import SolverAgent
from agents.debug_agent import DebugAgent
from agents.testcase_agent import TestCaseAgent
from agents.complexity_agent import ComplexityAgent
from agents.explanation_agent import ExplanationAgent
from agents.reflection_agent import ReflectionAgent
from agents.verification_agent import VerificationAgent
from agents.qa_agent import QAAgent

# Competitive Personas
from agents.strategy_agent import StrategyAgent
from agents.interview_agent import InterviewAgent
from agents.code_review_agent import CodeReviewAgent
from agents.company_agent import CompanyAgent
from agents.hidden_test_agent import HiddenTestAgent

from core.security import security_manager

class ManagerAgent(BaseAgent):
    \"\"\"
    Top 1% Kaggle Orchestrator.
    Moves from a basic router to a Pipeline State Machine.
    Supports yielding intermediate states so UI can render timeline progress.
    \"\"\"

    def __init__(self):
        super().__init__()
        # V1 Base Agents
        self.solver = SolverAgent()
        self.debugger = DebugAgent()
        self.testcase = TestCaseAgent()
        self.complexity = ComplexityAgent()
        self.explainer = ExplanationAgent()
        
        # V2 Advanced Pipeline Agents
        self.reflector = ReflectionAgent()
        self.verifier = VerificationAgent()
        self.qa = QAAgent()
        
        # V2 Competitive Advantage Agents
        self.strategy = StrategyAgent()
        self.interview = InterviewAgent()
        self.reviewer = CodeReviewAgent()
        self.company = CompanyAgent()
        self.hidden_test = HiddenTestAgent()

    def run_pipeline(self, task: str, **kwargs) -> Generator[Dict[str, Any], None, None]:
        \"\"\"
        Yields intermediate status updates to the caller before yielding the final result.
        \"\"\"
        sanitized_kwargs = {}
        for k, v in kwargs.items():
            if isinstance(v, str):
                sanitized_kwargs[k] = security_manager.sanitize(v)
            else:
                sanitized_kwargs[k] = v
                
        prob_state = sanitized_kwargs.get("problem_statement", "")

        try:
            if task == "solve_pipeline":
                # State 1: Solver
                yield {"status": "thinking", "message": "[1/4] Solver Agent designing initial algorithm..."}
                solve_res = self.solver.run(prob_state, sanitized_kwargs.get("constraints"))
                if "error" in solve_res:
                    yield solve_res; return
                
                # State 2: Reflection
                yield {"status": "thinking", "message": "[2/4] Reflection Agent critiquing the code..."}
                reflect_res = self.reflector.run(prob_state, solve_res.get("code", ""))
                if "error" in reflect_res:
                    yield reflect_res; return
                
                current_code = reflect_res.get("revised_code", solve_res.get("code", ""))

                # State 3: Verifier
                yield {"status": "thinking", "message": "[3/4] Verification proxy simulating dry-run..."}
                verify_res = self.verifier.run(prob_state, current_code)
                if "error" in verify_res:
                    yield verify_res; return
                
                # State 4: QA Gatekeeper
                yield {"status": "thinking", "message": "[4/4] QA Agent preparing polished final output..."}
                raw_data = json.dumps({
                    "initial_logic": solve_res, 
                    "critique": reflect_res, 
                    "verification": verify_res.get("verification_status")
                })
                qa_res = self.qa.run(raw_data)
                
                # Final Yield
                yield {"status": "complete", "result": qa_res}

            elif task == "debug":
                yield {"status": "thinking", "message": "Debugger Agent analyzing flaws..."}
                res = self.debugger.run(prob_state, sanitized_kwargs.get("incorrect_code", ""))
                yield {"status": "complete", "result": res}
                
            elif task == "complexity":
                yield {"status": "thinking", "message": "Complexity Analyst checking Big O..."}
                res = self.complexity.run(prob_state, sanitized_kwargs.get("code", ""))
                yield {"status": "complete", "result": res}

            elif task == "testcase":
                yield {"status": "thinking", "message": "Generating Test Cases..."}
                res = self.testcase.run(prob_state)
                yield {"status": "complete", "result": res}

            elif task == "explain":
                yield {"status": "thinking", "message": "Building explanation..."}
                res = self.explainer.run(sanitized_kwargs.get("code", ""), sanitized_kwargs.get("mode", "Beginner"))
                yield {"status": "complete", "result": res}
                
            elif task == "strategy":
                yield {"status": "thinking", "message": "Contest Strategist assessing... "}
                res = self.strategy.run(sanitized_kwargs.get("contest_details", ""))
                yield {"status": "complete", "result": res}
                
            elif task == "interview":
                yield {"status": "thinking", "message": "FAANG Interviewer calibrating..."}
                res = self.interview.run(prob_state, sanitized_kwargs.get("user_code", ""))
                yield {"status": "complete", "result": res}
            
            elif task == "review":
                yield {"status": "thinking", "message": "Code Reviewer nitpicking..."}
                res = self.reviewer.run(sanitized_kwargs.get("code", ""))
                yield {"status": "complete", "result": res}
                
            elif task == "company":
                yield {"status": "thinking", "message": "Company Culture Agent mapping..."}
                res = self.company.run(sanitized_kwargs.get("company_name", ""), sanitized_kwargs.get("code", ""))
                yield {"status": "complete", "result": res}
                
            elif task == "hidden_test":
                yield {"status": "thinking", "message": "Hidden Trap Detector scanning..."}
                res = self.hidden_test.run(sanitized_kwargs.get("code", ""))
                yield {"status": "complete", "result": res}

                
            else:
                yield {"error": f"Unknown task type: {task}"}
                
        except Exception as e:
            self.logger.error(f"Pipeline crashed for task {task}: {e}")
            yield {"error": str(e)}

    def run(self, task: str, **kwargs) -> Dict[str, Any]:
        \"\"\"
        Synchronous wrapper for MCP tools which don't support UI generators directly easily.
        Takes the final status event from run_pipeline.
        \"\"\"
        final = {}
        for event in self.run_pipeline(task, **kwargs):
            if "status" in event and event["status"] == "complete":
                final = event.get("result", {})
            elif "error" in event:
                return event
        return final
