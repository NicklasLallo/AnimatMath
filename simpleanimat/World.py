

class World:
    graph = {}

    --init--(self, nodes=[], edges=[]):
        for node in nodes:
            e = []
            for (start, end) in edges:

                if start == node:
                    e.append(end)

