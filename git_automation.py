import os
import subprocess
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='git_operations.log'
)
logger = logging.getLogger(__name__)

def setup_git_config():
    """Setup basic git configuration"""
    try:
        # Set git configurations
        subprocess.run(['git', 'config', '--global', 'user.name', 'GitHub Actions Bot'], check=True)
        subprocess.run(['git', 'config', '--global', 'user.email', 'actions@github.com'], check=True)
        
        # Setup GitHub token for authentication
        github_token = os.environ.get('GITHUB_TOKEN')
        if github_token:
            remote_url = subprocess.check_output(['git', 'remote', 'get-url', 'origin']).decode().strip()
            if 'https://' in remote_url:
                new_url = f"https://x-access-token:{github_token}@github.com/{remote_url.split('github.com/')[1]}"
                subprocess.run(['git', 'remote', 'set-url', 'origin', new_url], check=True)
        return True
    except Exception as e:
        logger.error(f"Error setting up git config: {str(e)}")
        return False

def run_git_command(command):
    """Execute a git command and return the output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=True,
            capture_output=True,
            text=True
        )
        return result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {e.stderr}")
        raise

def git_pull():
    """Pull latest changes from the remote repository"""
    try:
        logger.info("Starting git pull operation")
        output = run_git_command("git pull origin main")
        logger.info(f"Git pull completed: {output}")
        return True, output
    except Exception as e:
        logger.error(f"Error during git pull: {str(e)}")
        return False, str(e)

def git_push(commit_message=None):
    """Push changes to the remote repository"""
    try:
        logger.info("Starting git push operation")
        
        # Check for changes
        status = run_git_command("git status --porcelain")
        if not status:
            logger.info("No changes to commit")
            return True, "No changes to commit"

        # Add all changes
        run_git_command("git add .")
        
        # Create commit message if not provided
        if not commit_message:
            commit_message = f"Automated update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Commit changes
        run_git_command(f'git commit -m "{commit_message}"')
        
        # Push changes
        output = run_git_command("git push origin main")
        
        logger.info(f"Git push completed: {output}")
        return True, output
    except Exception as e:
        logger.error(f"Error during git push: {str(e)}")
        return False, str(e)

def sync_repository():
    """Synchronize repository by pulling and pushing changes"""
    # Setup git configuration first
    if not setup_git_config():
        return False, "Failed to setup git configuration"
    
    pull_success, pull_message = git_pull()
    if not pull_success:
        return False, f"Pull failed: {pull_message}"
    
    push_success, push_message = git_push()
    if not push_success:
        return False, f"Push failed: {push_message}"
    
    return True, "Repository synchronized successfully"

if __name__ == "__main__":
    success, message = sync_repository()
    print(f"{'Success' if success else 'Failed'}: {message}")
