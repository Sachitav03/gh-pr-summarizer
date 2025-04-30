import requests
import os

def get_pr_data(owner, repo, pr_number):
    token = os.getenv("GITHUB_TOKEN")
    if not token:
        raise EnvironmentError("GITHUB_TOKEN not set in environment.")

    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }

    pr_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}"
    files_url = f"{pr_url}/files"

    pr_response = requests.get(pr_url, headers=headers)
    files_response = requests.get(files_url, headers=headers)

    # Debug output
    print(f"PR status: {pr_response.status_code}")
    print(f"PR response: {pr_response.text}")
    
    if pr_response.status_code != 200:
        raise Exception(f"Failed to fetch PR: {pr_response.status_code}, {pr_response.text}")
    
    if files_response.status_code != 200:
        raise Exception(f"Failed to fetch PR files: {files_response.status_code}, {files_response.text}")

    pr_json = pr_response.json()
    files_json = files_response.json()

    return {
        "title": pr_json["title"],
        "body": pr_json["body"],
        "files": [
            {
                "filename": f["filename"],
                "patch": f.get("patch", "")
            } for f in files_json if "patch" in f
        ]
    }
