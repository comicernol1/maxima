import os,subprocess
try:
    MaximaProcessID = subprocess.check_output("pgrep -f ~/maxima/index.py", shell=True).rstrip().decode("utf-8")
    os.system("kill "+MaximaProcessID)
except subprocess.CalledProcessError:
    pass
os.system("rm -r maxima")
os.system("git clone https://www.github.com/comicernol1/maxima.git")
os.system("python3 ~/maxima/index.py &")
NewMaximaProcessID = subprocess.check_output("pgrep -f ~/maxima/index.py", shell=True).rstrip().decode("utf-8")
print("\nProcess "+NewMaximaProcessID+"\n")
