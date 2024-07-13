import os
import subprocess
from git import Repo, GitCommandError

# Define variables
REPO_URL = "git@github.com:debrej2021/Jul-13_CI_CD.git" 
LOCAL_PATH = r"C:\JUL-13_CI_CD"   

def clone_or_pull_repo(repo_url, local_path):
    try:
        if os.path.exists(local_path):
            print(f"Repository already exists at {local_path}. Pulling latest changes...")
            repo = Repo(local_path)
            origin = repo.remotes.origin
            origin.pull()
        else:
            print(f"Cloning repository into {local_path}...")
            Repo.clone_from(repo_url, local_path)
        print("Repository operation successful.")
    except GitCommandError as e:
        print(f"GitCommandError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

def restart_nginx():
    try:
        print("Restarting Nginx...")
        subprocess.run(["sudo", "systemctl", "restart", "nginx"], check=True)
        print("Nginx restart successful.")
    except subprocess.CalledProcessError as e:
        print(f"Error restarting Nginx: {e}")

if __name__ == "__main__":
    clone_or_pull_repo(REPO_URL, LOCAL_PATH)
    restart_nginx()
