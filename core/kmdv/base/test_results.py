import threading


class TestResults:
    results = {}
    lock = threading.Lock()

    @staticmethod
    def add_result(test_name, result) -> None:
        with TestResults.lock:
            TestResults.results[test_name] = result

    @staticmethod
    def print_results() -> None:
        print("\nTest results:")
        with TestResults.lock:
            for test_name, result in TestResults.results.items():
                print(f"{test_name} - Status: {result}")
                
    @staticmethod
    def get_result(test_name) -> str:
        with TestResults.lock:
            return TestResults.results[test_name]