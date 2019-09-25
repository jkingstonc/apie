class VFS:

    def __init__(self):
        self.paths = {}

    # mount a function and a path in the vfs
    def mount(self, path, func):
        current_path = self.paths
        counter = 0
        path_len = len(path.split('/'))
        for path in path.split('/'):
            # first check if we have found a valid path
            if path in current_path:
                # then update the current path to that path
                current_path = current_path[path]
            elif counter < path_len-1:
                current_path[path] = {}
                current_path = current_path[path]
            if counter == path_len-1:
                current_path[path] = func
            counter+=1

    # mount a function and a path in the vfs
    def visit(self, path):
        current_path = self.paths
        counter = 0
        path_len = len(path.split('/'))
        for path in path.split('/'):
            # first check if we have found a valid path
            if path in current_path:
                # then update the current path to that path
                current_path = current_path[path]
            elif counter < path_len-1:
                return False
            if counter == path_len-1:
                if type(current_path) is dict:
                    return False
                return current_path
            counter+=1