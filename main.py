from git import Repo
from pathlib import Path
import shutil
import csv
import json

packageNameDir = Path("./PackageNames")

managerRepo = "https://github.com/vortech11/Scratch-Package-Manager.git"

repoAlias = {}
installedPackages = {}

def replaceRepo(dirPath: Path, repo, branch="Main"):
    if dirPath.is_dir(): 
        shutil.rmtree(dirPath)

    Repo.clone_from(repo, dirPath, branch=branch)

def pullRepo(repo: Path):
    if repo.is_dir():
        repo = Repo(repo)
        origin = repo.remote()

        origin.fetch()

        localBranch = repo.active_branch
        remoteBranch = origin.refs[localBranch.name]

        if localBranch.commit == remoteBranch.commit:
            return
        
        repo.remotes.origin.pull()

def getNewest(dirPath: Path, repo, branch):
    if not dirPath.is_dir():
        replaceRepo(dirPath, repo, branch)
    else:
        pullRepo(dirPath)


getNewest(packageNameDir, managerRepo, "Verified-Packages")

with open("./PackageNames/packages.csv") as csv_file:
    csv_read = csv.reader(csv_file, delimiter=",")
    for row in csv_read:
        repoAlias[row[0]] = row[1]

with open("./packageWeb.json") as json_file:
    installedPackages = json.load(json_file)

print(repoAlias)
print(installedPackages)

