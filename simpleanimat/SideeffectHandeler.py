

class SideeffectHandeler:
    def __init__(self):
        raise NotImplementedError("SideeffectHandeler is an abstract supertype and cannot be instantiated.")

    #Takes an animat, the action it performed, and the world to cause potential sideeffects of the action to the world
    def handleAction(animat, action, world):
        raise NotImplementedError("Any SideeffectHandler needs to implement a the handleAction function.")
