import os
import git
import requests
from git import RemoteProgress

class Progress(RemoteProgress):
    def update(self, op_code, cur_count, max_count=None, message=''):
        print(self._cur_line)

def check_for_new_commits(local_repo_path, github_repo_url):
    try:
       
        if not os.path.exists(local_repo_path):
            repo = git.Repo.clone_from(github_repo_url, local_repo_path)
            print(f"Cloned repository to {local_repo_path}")
        else:
            repo = git.Repo(local_repo_path)
            print(f"Opened existing repository at {local_repo_path}")

        # Fetch latest changes
        origin = repo.remotes.origin
        origin.fetch()
        print("Fetched latest changes from origin")

        # Get local and remote HEAD commit hashes
        local_head = repo.head.commit
        remote_head = repo.commit('origin/main')  # Adjust 'main' to 'master' if needed

        print(f"Local HEAD: {local_head}")
        print(f"Remote HEAD: {remote_head}")

        if local_head == remote_head:
            print("No new commits.")
        else:
            print("New commits found.")
            new_commits = list(repo.iter_commits(f'{local_head}..{remote_head}'))

            for commit in new_commits:
                print(f"Commit: {commit.hexsha}")
                print(f"Author: {commit.author.name} <{commit.author.email}>")
                print(f"Date: {commit.authored_datetime}")
                print(f"Message: {commit.message}")
                print("-" * 50)

    except git.exc.GitCommandError as e:
        print(f"GitCommandError: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")

    # except git.exc.GitCommandError as e:
    #     print(f"Error: {e}")
    # except Exception as e:
    #     print(f"Unexpected error: {e}")

if __name__ == "__main__":
    local_repo_path = r"C:\JUL-13_CI_CD" 
    github_repo_url = "git@github.com:debrej2021/Jul-13_CI_CD.git"  # Replace with your GitHub repository URL

    check_for_new_commits(local_repo_path, github_repo_url)
