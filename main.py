import os
from pathlib import Path

import gitlab
import getpass


TOKEN = getpass.getpass("Enter gitlab token: ")
GITLAB_BASE_URL = input("Enter gitlab url: ")
BASE_DIR_NAME = input("Enter gitlab url: ")
PB_PATH = input("Enter protobuf path: ")
PROJECT_ID = input("Enter project id: ")
BASE_DIR = Path(BASE_DIR_NAME)

if TOKEN is None:
    raise RuntimeError("GITLAB_TOKEN is missing")


def importer():
    try:
        BASE_DIR.mkdir()
    except FileExistsError:
        print("The directory already exists")
    gl = gitlab.Gitlab(GITLAB_BASE_URL, private_token=TOKEN)
    gl.auth()
    project = gl.projects.get(PROJECT_ID)
    files = project.repository_tree(path=PB_PATH)
    file_names = []
    for file in files:
        name = file.get('name')
        file_names.append(name)

    for file_name in file_names:
        raw_content = project.files.raw(
            file_path="".join(PB_PATH + file_name), ref="master"
        )
        file = raw_content.decode("utf-8")
        with (BASE_DIR / file_name).open("w") as fp:
            fp.write(file)

def converter():
    os.system(f"protoc -I=. --python_out=. {BASE_DIR_NAME}/*.proto")


if __name__ == "__main__":
    importer()
    converter()