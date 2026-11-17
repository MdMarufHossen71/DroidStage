# Start here: create your public GitHub repository

This scaffold is prepared for the GitHub account `MdMarufHossen71` and repository name `DroidStage`.

## 1. Install the required command-line tools

- Git for Windows: https://git-scm.com/download/win
- GitHub CLI: https://cli.github.com/

Open a new PowerShell 7 window after installation and verify:

```powershell
git --version
gh --version
```

## 2. Sign in to GitHub CLI

```powershell
gh auth login
```

Choose GitHub.com, HTTPS, and authenticate in the browser as `MdMarufHossen71`. Verify:

```powershell
gh auth status
gh api user --jq .login
```

The second command must print `MdMarufHossen71`.

## 3. Create the public repository and push this scaffold

Extract the ZIP. In PowerShell, change into the extracted `DroidStage-Starter` folder, then run:

```powershell
Set-ExecutionPolicy -Scope Process Bypass
.\Create-GitHubRepo.ps1
```

The script initializes Git (if needed), creates the first commit, creates `MdMarufHossen71/DroidStage` as a **public** GitHub repository, and pushes the files. It deliberately stops if the remote repository already exists or an `origin` remote is already configured; it will not overwrite an existing repository.

## 4. Start building with OpenCode

Open the extracted folder in OpenCode. Then open:

`docs/OPENCODE_BOOTSTRAP_PROMPT.md`

Copy the full prompt under the heading **OpenCode implementation prompt** and paste it into OpenCode. The prompt directs the coding agent to validate the browser streaming architecture, implement a real Physical Device Bridge vertical slice first, run tests, and document limitations honestly.

## Notes

- The public GitHub repository is open to everyone to view, clone, fork, and contribute under the MIT license.
- Publishing the repository does not make the Android app functional yet; the scaffold is a project specification and bootstrap prompt.
- If GitHub CLI reports that the repository already exists, stop and inspect it manually. Do not use a force push to replace its history.
