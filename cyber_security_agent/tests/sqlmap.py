import subprocess

# Define the URL with a potential SQL injection vulnerability
target_url = "https://taupe-tanuki-66c44a.netlify.app/?id=1"  # Example parameter that could be injectable

# Run Sqlmap on the URL to detect SQL injection
subprocess.run(['python3', 'sqlmap.py', '-u', target_url, '--batch'])
