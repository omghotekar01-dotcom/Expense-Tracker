import subprocess
import sys
import time

# Kill any existing streamlit processes
subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
               stderr=subprocess.DEVNULL, stdout=subprocess.DEVNULL)

time.sleep(2)

# Set environment variable
import os
os.environ['STREAMLIT_LOGGER_LEVEL'] = 'error'
os.environ['STREAMLIT_CLIENT_TOOLBARMODE'] = 'minimal'

# Start streamlit
subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'app.py',
                '--logger.level=error'])
