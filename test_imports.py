import os
import importlib.util
import sys
import glob

def test_imports():
    success = True
    for root, _, files in os.walk('.'):
        for file in files:
            if file.endswith('.py') and file != 'test_imports.py':
                path = os.path.join(root, file)
                # Skip venv or .venv if they exist, and hidden dirs
                if 'venv' in path or '.git' in path or '__pycache__' in path:
                    continue
                
                module_name = path.replace('.\\', '').replace('./', '').replace('\\', '.').replace('/', '.').replace('.py', '')
                
                print(f"Testing import of {module_name}...")
                try:
                    spec = importlib.util.spec_from_file_location(module_name, path)
                    module = importlib.util.module_from_spec(spec)
                    sys.modules[module_name] = module
                    spec.loader.exec_module(module)
                    print(f"  [OK] {module_name}")
                except Exception as e:
                    print(f"  [ERROR] Failed to import {module_name}: {e}")
                    success = False
    
    if not success:
        sys.exit(1)
    print("All imports successful!")

if __name__ == '__main__':
    test_imports()
