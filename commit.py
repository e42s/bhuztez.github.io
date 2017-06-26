#!/usr/bin/env python2

import os
import os.path
import sys
from dulwich.repo import Repo
from dulwich.objects import Blob, Tree, Commit


repo = Repo(".")

commit_sha = repo.head()
commit = repo.get_object(commit_sha)


def add_blob(store, path):
    with open(path, "rb") as f:
        blob = Blob.from_string(f.read())
    store.add_object(blob)
    return blob.id

def add_folder(store, folder):
    tree = Tree()

    for name in os.listdir(folder):
        filename = os.path.join(folder, name)
        if os.path.islink(filename):
            continue
        elif os.path.isdir(filename):
            tree.add(name, 040000, add_folder(store, filename))
        elif os.path.isfile(filename):
            tree.add(name, 0100644, add_blob(store, filename))

    store.add_object(tree)
    return tree.id


store = repo.object_store
tree = add_folder(store, 'output')

old_commit = repo.get_refs().get("refs/heads/master", None)

new_commit = Commit()

if old_commit is not None:
    new_commit.parents = [old_commit]

new_commit.author = commit.author
new_commit.committer = commit.committer
new_commit.author_time = commit.author_time
new_commit.commit_time = commit.commit_time
new_commit.author_timezone = commit.author_timezone
new_commit.commit_timezone = commit.commit_timezone
new_commit.encoding = commit.encoding
new_commit.message = commit.message
new_commit.tree = tree

store.add_object(new_commit)

repo['refs/heads/master'] = new_commit.id
