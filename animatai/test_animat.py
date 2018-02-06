from gzutils.gzutils import DotDict
from agents import Agent, Thing, Direction, NonSpatial, XYEnvironment

MOVES = [(1, 0), (-1, 0)]

OPTIONS = DotDict({
    'terrain': 'DDDDD',
    'wss_cfg': {
        'numTilesPerSquare': (1, 1),
        'drawGrid': True,
        'randomTerrain': 0,
        'agents': {
            'Test': {
                'name': 'T',
                'pos': (0,0),
                'hidden': False
            } 
        }
    }
})

# Classes
# =======

class World(XYEnvironment):
    def __init__(self, options):
        super().__init__(options)

    def calc_performance(self, _, _2):
        pass

    def execute_action(self, agent, action, time):
        super().execute_action(agent, action, time)

    def is_done(self):
        return False

class TestAnimat(Agent):
    def __repr__(self):
        return '{} ({})'.format(self.__name__, self.__class__.__name__)

def program (percept):
    return 'Right'

def run(wss=None, steps=None, seed=None):
    steps = int(steps) if steps else 50

    options = OPTIONS
    options.wss = wss

    world = World(options)
    test1 = TestAnimat(program, 'Test')
    
    test1.direction = Direction(Direction.D)
    
    world.add_thing(test1, (0,0))

    world.run(steps)

if __name__ == "__main__":
    run()
