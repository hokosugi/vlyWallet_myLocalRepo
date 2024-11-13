import os
import requests
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def setup_branch_protection():
    """Setup branch protection rules for the main branch"""
    try:
        github_token = os.environ.get('GITHUB_TOKEN')
        if not github_token:
            logger.error("GitHub token not found in environment variables")
            return False

        # API endpoint for branch protection
        repo_owner = "hokosugi"
        repo_name = "VlyWalletLeadersboard"
        branch = "main"
        url = f"https://api.github.com/repos/{repo_owner}/{repo_name}/branches/{branch}/protection"

        # Headers for authentication
        headers = {
            "Accept": "application/vnd.github.v3+json",
            "Authorization": f"token {github_token}",
        }

        # Simplified protection rules for personal repository
        protection_rules = {
            "required_status_checks": None,  # Disable status checks initially
            "enforce_admins": True,
            "required_pull_request_reviews": {
                "required_approving_review_count": 1,
                "dismiss_stale_reviews": True,
                "require_code_owner_reviews": True
            },
            "restrictions": None,  # Required field but set to None for personal repos
            "required_linear_history": True,
            "allow_force_pushes": False,
            "allow_deletions": False
        }

        # Send request to GitHub API
        response = requests.put(url, headers=headers, json=protection_rules)
        
        if response.status_code in [200, 201]:
            logger.info("Branch protection rules set successfully")
            return True
        elif response.status_code == 403:
            logger.error("Permission denied. Make sure the token has the necessary permissions.")
            return False
        elif response.status_code == 404:
            logger.error("Repository or branch not found. Please verify the repository and branch names.")
            return False
        else:
            logger.error(f"Failed to set branch protection rules: {response.status_code} - {response.text}")
            
            # If we get a rate limit error, wait and retry
            if response.status_code == 429:
                reset_time = int(response.headers.get('X-RateLimit-Reset', 0))
                wait_time = max(reset_time - time.time(), 0)
                logger.info(f"Rate limited. Waiting {wait_time} seconds before retrying...")
                time.sleep(wait_time)
                return setup_branch_protection()
            
            return False

    except requests.exceptions.RequestException as e:
        logger.error(f"Network error occurred: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Error setting up branch protection: {str(e)}")
        return False

if __name__ == "__main__":
    if setup_branch_protection():
        print("Branch protection rules have been set up successfully")
    else:
        print("Failed to set up branch protection rules")
