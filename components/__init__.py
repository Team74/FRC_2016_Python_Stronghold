class Component(object):
    def update(self):
        raise NotImplementedError("Component must have an 'update' method")

    def stop(self):
        raise NotImplementedError("Component must have a 'stop' method")
