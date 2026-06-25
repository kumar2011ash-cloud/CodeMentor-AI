import json
import re
import os

def camel_to_snake(name):
    s1 = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', s1).lower()

def main():
    with open("agent_examples.json", "r") as f:
        results = json.load(f)

    for agent_name, example in results.items():
        file_name = f"agents/{camel_to_snake(agent_name)}.py"
        if agent_name == "TestCaseAgent":
            file_name = "agents/testcase_agent.py"
        if os.path.exists(file_name):
            with open(file_name, "r") as f:
                content = f.read()
            
            # Format the example as a pretty JSON string
            example_str = json.dumps(example, indent=4)
            
            class_def = f"class {agent_name}(BaseAgent):"
            
            if "EXAMPLE_OUTPUT" in content:
                print(f"Already injected in {file_name}")
                continue
                
            replacement = f'{class_def}\n\n    EXAMPLE_OUTPUT = """\n{example_str}\n    """\n'
            content = content.replace(class_def, replacement, 1)
            
            with open(file_name, "w") as f:
                f.write(content)
            print(f"Injected into {file_name}")
        else:
            print(f"Could not find file: {file_name}")

if __name__ == "__main__":
    main()
