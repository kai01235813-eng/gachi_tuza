import sys
import os

# Add parent directory to sys.path so imports work in Vercel serverless environment
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from web_app import app
