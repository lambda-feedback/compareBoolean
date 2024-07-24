import json
from .evaluation import evaluation_function

class TestData:
    def __init__(self, test_dict: dict):
        self.response = test_dict["response"]
        self.answer = test_dict["answer"]
        self.params = test_dict["params"]
        self.is_correct = test_dict["is_correct"]
        self.results = test_dict.get("results")

    def evaluate(self) -> dict:
        return evaluation_function(self.response, self.answer, self.params)
    
    def compare(self, eval_result: dict) -> tuple[bool, str]:
        eval_correct = eval_result["is_correct"]
            
        if eval_correct != self.is_correct:
            return (
                False,
                f"response \"{self.response}\" with answer \"{self.answer}\" was {'' if eval_correct else 'in'}correct: {eval_result['feedback']}."
            )
        
        # Are there any other fields in the eval function result that need to be checked?
        if self.results != None:
            # Check each one in turn
            for key, value in self.results.items():
                actual_result_val = eval_result.get(key)
                if actual_result_val == None:
                    return (False, f"No value returned for \"{key}\"")
                
                if actual_result_val != value:
                    return (
                        False,
                        f"expected {key} = \"{value}\", got {key} = \"{actual_result_val}\""
                    )
        
        return (True, "")
        

def get_tests_from_json(filename: str) -> list[TestData]:
    out = []
    tests = []
    with open(filename, "r") as test_file:
        test_json = test_file.read()
        tests = json.loads(test_json)
    for test in tests:  
        out.append(TestData(test))
    
    return out
