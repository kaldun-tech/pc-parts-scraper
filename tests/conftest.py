import os
import sys

# Add lambda directory to Python path
lambda_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'lambda')
sys.path.append(lambda_dir)

# Add project root to Python path
project_root = os.path.dirname(os.path.dirname(__file__))
sys.path.append(project_root)
