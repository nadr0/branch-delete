# branch-delete

Delete local git branches using curses GUI written in python `3.5.2`

# Purpose

I tend to accumulate a lot of local branches and I want a simple and quick method to delete large amounts of branches.

# How to

###### Controls

| Key | Description |
| --- | --- |
| j | Move selection down |
| k | Move selection up |
| enter | Activate selection event |
| q | Quit application (while in branch list screen) |

Start screen

![Start Screen](https://github.com/nadr0/branch-delete/blob/master/images/branch-delete-start.png)

After pressing enter to select a branch to delete

![Selection Screen](https://github.com/nadr0/branch-delete/blob/master/images/branch-delete-select.png)

# FYI

- your current branch is not included in the branch list
- master is not include in the branch list
- branches that need force delete i.g `git branch -D ...` will fail

# Improvements

- config to filter your own custom branches for you cannot accidently delete an important branch
- handle `git branch -D` error
- allow for force branch delete
