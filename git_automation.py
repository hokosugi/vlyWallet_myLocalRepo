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
            logger.info("Git configuration set up successfully")
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

        return True
    except Exception as e:
        logger.error(f"Error initializing repository: {str(e)}")
        return False

def git_push(force=False):
    """Push changes to the remote repository"""
    try:
        logger.info("Starting git push operation")
        
        # Add all changes except workflow files
        run_git_command("git add --all")
        run_git_command("git reset -- .github/workflows/")
        
        # Create commit message
        commit_message = f"Automated update: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        # Commit changes
        _, output = run_git_command(f'git commit -m "{commit_message}"', check=False)
        if "nothing to commit" not in output:
            logger.info("Changes committed successfully")
        
        # Force push to remote
        push_command = "git push -u origin main --force" if force else "git push -u origin main"
        success, output = run_git_command(push_command)
        
        if success:
            logger.info("Git push completed successfully")
            return True, "Repository synchronized successfully"
        else:
            logger.error(f"Push failed: {output}")
            return False, f"Push failed: {output}"
            
    except Exception as e:
        logger.error(f"Error during git push: {str(e)}")
        return False, str(e)

def sync_repository(force_push=True):
    """Synchronize repository by pushing changes with force"""
    # Setup git configuration first
    if not setup_git_config():
        return False, "Failed to setup git configuration"
    
    # Initialize repository if needed
    if not initialize_repository():
        return False, "Failed to initialize repository"
    
    # Push changes with force
    success, message = git_push(force=force_push)
    if not success:
        return False, f"Push failed: {message}"
    
    return True, "Repository synchronized successfully"

if __name__ == "__main__":
    # Execute force push
    success, message = sync_repository(force_push=True)
    if success:
        logger.info(message)
        print(f"Success: {message}")
    else:
        logger.error(message)
        print(f"Failed: {message}")