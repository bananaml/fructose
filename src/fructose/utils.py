import os 

# Get the relative path to whatever directory the user specified
def get_target_dir(dir):
    # route to cwd if no path specified
    if len(dir) == 0:
        target_dir = "."
    else:
        target_dir = dir[0]
    # clean to relative path from here
    target_dir = os.path.relpath(target_dir)
    if not os.path.exists(target_dir):
        os.makedirs(target_dir)
    return target_dir
