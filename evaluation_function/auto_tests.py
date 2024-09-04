import json
import yaml
from typing import Union

class TestFile:
    """An abstraction over a test file, which may be in one of several different formats.
    Currently, JSON and YAML are supported.
    """

    def __init__(self, path: str) -> None:
        self.groups = []

        # Attempt to open the given file. Exit with an error if this
        # is not possible.
        file_content = ""
        try:
            with open(path, "r") as test_file:
                file_content = test_file.read()
        except IOError as e:
            raise Exception(f'Failed to open test file: "{e}"')

        # Get the file extension to determine which format should be used.
        extension = path.split(".")[-1]
        if extension == "json":
            try:
                questions = json.loads(file_content)

                for question in questions:
                    out = []
                    title = question["title"]
                    for part in question["parts"]:
                        for response_area in part["responseAreas"]:
                            params = response_area["params"]
                            answer = response_area["answer"]
                            for test in response_area["tests"]:
                                test.update({"answer": answer})
                                test.update({"params": params})
                                out.append(SingleTest(test))
                    self.groups.append({"title": title, "tests": out})

            except KeyError as e:
                raise Exception(f'The key "{e.args[0]}" doesn\'t exist, or is in the wrong place.')
            except json.JSONDecodeError as e:
                raise Exception(f'Error parsing JSON: "{e}"')
        elif extension == "yaml":
            try:
                # Tests are organised in groups of separate YAML documents (separated by "---")
                docs = yaml.safe_load_all(file_content)
                for test_group in docs:
                    tests = []
                    title = test_group.get("title", "")
                    for test in test_group.get("tests", []):
                        # Add an empty params field if none was provided.
                        if test.get("params") == None:
                            test["params"] = {}

                        # Does this test have sub-tests?
                        sub_tests = test.get("sub_tests")
                        if sub_tests != None:
                            params = test["params"]
                            answer = test["answer"]

                            for sub_test in sub_tests:
                                sub_test["params"] = params
                                sub_test["answer"] = answer
                                tests.append(SingleTest(sub_test))
                        else:
                            tests.append(SingleTest(test))

                    self.groups.append({"title": title, "tests": tests})
            except yaml.YAMLError as e:
                raise Exception(f'Error parsing YAML: {e}')
        else:
            raise Exception(f'"{extension}" files are not supported as a test format.')

class SingleTest:
    def __init__(self, test_dict: dict):
        self.response = test_dict.get("response", "")
        self.answer = test_dict.get("answer", "")
        self.params = test_dict.get("params", {})
        expected_result = test_dict.get("expected_result")
        if not expected_result:
            raise Exception("No expected result given for test")
        self.is_correct = expected_result.get("is_correct")
        self.results = expected_result
        self.desc = test_dict.get("description", "")

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


def auto_test(path, func):
    """A decorator that adds the necessary infrastructure to run tests defined
    in an external data file.\n
    `path`: the path to the data file, relative to the eval function root.\n
    `func`: the function to test. Should usually be `evaluation_function`.
    """
    def _auto_test(orig_class):
        def test_auto(self):
            # Creating a TestFile can fail for several reasons.
            # If so, an exception is raised with a suitable error message
            try:
                tests = TestFile(path)
            except Exception as e:
                self.fail(e)

            # Successfully loaded 
            for group in tests.groups:
                for test in group["tests"]:
                    results = test.evaluate(func)
                    self.assertTrue(*test.compare(results.to_dict()))

        orig_class.test_auto = test_auto # Add the test_auto function to the class
        return orig_class
    return _auto_test
