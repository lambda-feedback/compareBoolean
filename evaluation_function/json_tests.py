import json

class TestData:
    def __init__(self, test_dict: dict):
        self.response = test_dict["response"]
        self.answer = test_dict["answer"]
        self.params = test_dict["params"]
        expected_result = test_dict["expectedResult"]
        self.is_correct = expected_result["is_correct"]
        self.results = expected_result
        self.desc = test_dict["description"]

    def evaluate(self, func) -> dict:
        return func(self.response, self.answer, self.params)
    
    def compare(self, eval_result: dict) -> tuple[bool, str]:
        eval_correct = eval_result["is_correct"]
            
        if eval_correct != self.is_correct:
            return (
                False,
                f"response \"{self.response}\" with answer \"{self.answer}\" was {'' if eval_correct else 'in'}correct: {eval_result['feedback']}\nTest description: {self.desc}"
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
                        f"expected {key} = \"{value}\", got {key} = \"{actual_result_val}\"\nTest description: {self.desc}"
                    )
        
        return (True, "")
        

def get_tests_from_json(filename: str) -> list[TestData]:
    out = []
    questions = []
    with open(filename, "r") as test_file:
        test_json = test_file.read()
        questions = json.loads(test_json)
    # Convert the structured test data into a flat list of tests
    for question in questions:
        for part in question["parts"]:
            for response_area in part["responseAreas"]:
                params = response_area["params"]
                answer = response_area["answer"]
                for test in response_area["tests"]:
                    test.update({"answer": answer})
                    test.update({"params": params})
                    out.append(TestData(test))
    
    return out

def auto_test(path, func):
    def _auto_test(orig_class):
        def test_auto(self):
            tests = get_tests_from_json(path)
            for test in tests:
                results = test.evaluate(func)
                self.assertTrue(*test.compare(results.to_dict()))

        orig_class.test_auto = test_auto # Add the test_auto function to the class
        return orig_class
    return _auto_test
