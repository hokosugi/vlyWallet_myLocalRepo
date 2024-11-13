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

def run_git_command(command, check=True):
    """Execute a git command and return the output"""
    try:
        result = subprocess.run(
            command,
            shell=True,
            check=check,
            capture_output=True,
            text=True
        )
        return True, result.stdout.strip()
    except subprocess.CalledProcessError as e:
        logger.error(f"Git command failed: {e.stderr}")
        return False, e.stderr.strip()

def initialize_repository():
    """Initialize git repository if not already initialized"""
    try:
        # Check if git is initialized
        if not os.path.exists('.git'):
            _, output = run_git_command("git init")
            logger.info("Git repository initialized")
            
        # Check remote and add if not exists
        success, output = run_git_command("git remote -v", check=False)
        if 'origin' not in output:
            repo_url = "https://github.com/hokosugi/VlyWalletLeadersboard.git"
            _, output = run_git_command(f"git remote add origin {repo_url}")
            logger.info("Added remote origin")

        # Create and checkout main branch if it doesn't exist
        _, output = run_git_command("git rev-parse --verify main", check=False)
        if not output:
            _, output = run_git_command("git checkout -b main")
            logger.info("Created and checked out main branch")
        else:
            _, output = run_git_command("git checkout main")
            logger.info("Checked out existing main branch")
            
        return True
    except Exception as e:
        logger.error(f"Error initializing repository: {str(e)}")
        return False

def git_pull():
    """Pull latest changes from the remote repository"""
    try:
        logger.info("Starting git pull operation")
        success, output = run_git_command("git pull origin main --allow-unrelated-histories", check=False)
        if not success and "couldn't find remote ref main" in output:
            logger.info("Remote branch doesn't exist yet, skipping pull")
            return True, "No remote branch yet"
        elif success:
            logger.info(f"Git pull completed: {output}")
            return True, output
        else:
            logger.error(f"Git pull failed: {output}")
            return False, output
    except Exception as e:
        logger.error(f"Error during git pull: {str(e)}")
        return False, str(e)

def git_push(commit_message=None):
    """Push changes to the remote repository"""
    try:
        logger.info("Starting git push operation")
        
        # Check for changes
        success, status = run_git_command("git status --porcelain")
        if not status:
            logger.info("No changes to commit")
            return True, "No changes to commit"

        # Add all changes
        success, _ = run_git_command("git add .")
        if not success:
            return False, "Failed to stage changes"
        
        # Create commit message if not provided
        if not commit_message:
            commit_message = f"Automated update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Commit changes
        success, output = run_git_command(f'git commit -m "{commit_message}"')
        if not success:
            return False, f"Failed to commit: {output}"
        
        # Push changes
        success, output = run_git_command("git push -u origin main")
        if not success:
            return False, f"Failed to push: {output}"
        
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
    
    # Initialize repository if needed
    if not initialize_repository():
        return False, "Failed to initialize repository"
    
    # Pull changes
    pull_success, pull_message = git_pull()
    if not pull_success and "No remote branch yet" not in pull_message:
        return False, f"Pull failed: {pull_message}"
    
    # Push changes
    push_success, push_message = git_push()
    if not push_success:
        return False, f"Push failed: {push_message}"
    
    return True, "Repository synchronized successfully"

if __name__ == "__main__":
    success, message = sync_repository()
    if success:
        logger.info(message)
        print(f"Success: {message}")
    else:
        logger.error(message)
        print(f"Failed: {message}")
