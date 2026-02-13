# Escape Response Replication Project

A computational neuroscience project with the goal of replicating the following linked paper with Brian2: https://www.eneuro.org/content/eneuro/6/2/ENEURO.0423-18.2019.full.pdf, and publishing it in [ReScience C](https://rescience.github.io/write/)

Repository to the original paper's code can be found here: https://github.com/ModelDBRepository/245415

Example of a previously published computational neuroscience ReScience C paper can be found here: https://rescience.github.io/bibliography/Reynes_2025.html 

## Table of Contents

- [Contributing with Pull/Merge Requests](#contributing-with-pullmerge-requests)

## Contributing with Pull/Merge Requests

Follow these steps to create and submit pull/merge requests:

1. **Create a new branch** from the main branch for your work:
   ```bash
   git checkout main
   git pull origin main
   git checkout -b your-feature-branch
   ```

2. **Make your changes** in the new branch, committing regularly with clear, descriptive commit messages:
   ```bash
   git add <modified-files>
   git commit -m "Brief description of changes"
   ```

3. **Keep your branch up to date** with the main branch to avoid merge conflicts:
   ```bash
   git checkout main
   git pull origin main
   git checkout your-feature-branch
   git merge main
   ```

4. **Push your branch** to the remote repository:
   ```bash
   git push origin your-feature-branch
   ```

5. **Create a Pull/Merge Request** on GitHub/GitLab:
   - Navigate to the repository on the web interface
   - Click "New Pull Request" or "New Merge Request"
   - Select your feature branch as the source and main as the target
   - Provide a clear title and description of your changes
   - Reference any related issues using `#issue-number`

6. **Request reviews** from team members and address any feedback:
   - Make additional commits to your branch to address comments
   - Push updates to automatically update the PR/MR

7. **Merge your request** once approved:
   - Ensure all CI/CD checks pass
   - Use "Squash and merge" or "Merge commit" as per team conventions
   - Delete the feature branch after merging

8. **Update your local repository** after merging:
   ```bash
   git checkout main
   git pull origin main
   git branch -d your-feature-branch
   ```
