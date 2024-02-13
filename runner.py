import subprocess
from core.kmdv.base.test_base import test_results

parallel_count = 3

commands = [
    f"pytest -s -n {parallel_count}",
]

def pytest_session():    
    for command in commands:
        try:
            subprocess.run(command, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            if not "pytest" in command:
                print(f"Error running command: {command}")
        except Exception as e:
            print(f"An error occurred while running command: {command}")
            
    print("\nTest results:")
    for test_name, result in test_results.items():
        print(f"{test_name} - Status: {result}")


pytest_session()