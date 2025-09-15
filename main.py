from git import Repo
from pathlib import Path
import shutil
import csv
import json

packageNameDir = Path("./PackageNames")
packageDir = Path("./Packages")


managerRepo = Repo(Path(".")).remotes.origin.url

repoAlias = {}
installedPackages = {}

packageNum = 0

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

def getNewest(dirPath: Path, repo, branch="main"):
    if not dirPath.is_dir():
        replaceRepo(dirPath, repo, branch)
    else:
        pullRepo(dirPath)

def checkRepoInstallation(repo):
    return any([True for package in installedPackages if installedPackages[package]["repo"] == repo])

def installPackage(repo, required=False):
    if checkRepoInstallation(repo) == True:
        print("HIII")
        return

    packageName = f"p{packageNum}"
    getNewest(packageDir / packageName, repo)
    newName = ""
    version = ""
    dependencies = {}
    with open(packageDir / packageName / "spmMeta.json") as f:
        data = json.load(f)
        version = str(data["version"])
        newName = str(data["name"]) + version
        dependencies = data["dependencies"]

    shutil.move(packageDir / packageName, packageDir / newName)

    packageName = newName

    installedPackages[packageName] = {
        "repo":Repo(packageDir / packageName).remotes.origin.url,
        "version":version,
        "dependencies":dependencies,
        "references":[],
        "required": required
    }

    for package in installedPackages[packageName]["dependencies"]:
        if not package in installedPackages:
            if package in repoAlias:
                packageReference = installPackage(repoAlias[package])
            else:
                packageReference = installPackage(package)
        else:
            packageReference = package    
        installedPackages[packageReference]["references"].append(packageName)

    return packageName

getNewest(packageNameDir, managerRepo, "Verified-Packages")

with open("./PackageNames/packages.csv") as csv_file:
    csv_read = csv.reader(csv_file, delimiter=",")
    for row in csv_read:
        repoAlias[row[0]] = row[1]

with open("./packageWeb.json") as json_file:
    installedPackages = json.load(json_file)

Path("./Packages").mkdir(exist_ok=True)

installPackage(repoAlias["TestPackage"], True)

print(repoAlias)
print(installedPackages)

