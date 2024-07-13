import os
import git
import requests
from git import RemoteProgress

class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)

def check_for_new_commits(local_repo_path, github_repo_url):
    try:
        # Clone or open the local repository
        if not os.path.exists(local_repo_path):
            repo = git.Repo.clone_from(github_repo_url, local_repo_path, progress=Progress())
        else:
            repo = git.Repo(local_repo_path)

        # Fetch latest changes
        origin = repo.remotes.origin
        origin.fetch()

        # Get local and remote HEAD commit hashes
        local_head = repo.head.commit
        remote_head = repo.commit('origin/main')  # Adjust 'main' to 'master' if needed

        if local_head == remote_head:
            print("No new commits.")
        else:
            print("New commits found.")
            print(f"Local HEAD: {local_head}")
            print(f"Remote HEAD: {remote_head}")
            
            # Optionally, you can pull changes automatically
            # origin.pull()

    except git.exc.GitCommandError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

if __name__ == "__main__":
    local_repo_path = "C:\July 13th - Project\Jul-13_CI_CD"  # Replace with your local repository path
    github_repo_url = "https://github.com/debrej2021/Jul-13_CI_CD.git"  # Replace with your GitHub repository URL

    check_for_new_commits(local_repo_path, github_repo_url)
