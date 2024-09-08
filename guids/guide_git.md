# Pushing and Commiting

When you are happy with a feature add it, commit it with a name and push it to GitHub:

    git add .
    git commit -m "message"
    git push


# Error solutions

If you get errors such as 'fetch first' or 'rebase' these might help:

    git fetch
    git rebase


# Branches

The main app is located on the main branch, when you are working on a new feature you can add a new branch in case something goes wrong that might affect the whole project (you can also make branches from branches):

    git status          #your current branch
    git branch name     #new branch create
    git branch -a       #all branches
    git checkout name   #go to this branch
    git branch -D name  #delete branch

You can commit and push this branch to save it, when you want to add it (merge) to the main branch:
    
    git merge name

If there are conflicts (which happen when someone alters the main branch after creating a new branch), there will be comments about what is different, change it to your liking and do:

    git commit