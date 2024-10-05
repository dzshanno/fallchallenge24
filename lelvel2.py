import sys
import math


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.
class position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


class game:
    pass


class day:
    pass


class month:
    pass


class action:
    def __init__(self, id: int, output: str, cost: int, benefit: int = 0):
        self.id = id
        self.output = output
        self.cost = cost
        self.benefit = benefit


class building:
    def __init__(self, id: int, type: int, pos: position) -> None:
        self.id = id
        self.type = type
        self.pos = pos
        self.conns = 0


class tube:
    def __init__(self, b1: building, b2: building, cap: int) -> None:
        self.b1 = b1
        self.b2 = b2
        self.cap = cap


class pod:
    def __init__(self, id: int, path: list) -> None:
        self.id = id
        self.path = path


class pad:
    def __init__(self, id: int, pos: position, astros: list) -> None:
        self.id = id
        self.pos = pos
        self.astros = astros
        self.conns = 0


class port:
    def __init__(self, b1: building, b2: building) -> None:
        self.b1 = b1
        self.b2 = b2


def dist(b1, b2) -> float:
    d = math.sqrt((b1.x - b2.x) ** 2 + (b1.y - b2.y) ** 2)
    return d


def cmb(pad, astro) -> building:
    # closest matching building

    distance = 1000
    bestb = -1
    for b in buildings:
        if b.type == astro:
            if dist(pad, b) < distance:
                distance = dist(pad, b)
                bestb = b
    return bestb


def point_intersect():
    pass


def tubecost(b1, b2):
    cost = math.floor(dist(b1.pos, b2.pos) * 0.1)
    return cost


def addactions():
    global resources, nextpod
    if resources > 0:
        for p in pads:
            if p.conns < 5:
                for a in p.astros:
                    for b in buildings:
                        if b.conns < 5:
                            if len(actions) > 20:
                                return

                            if int(b.type) == int(a):
                                tube_exists = False
                                for t in tubes:
                                    if (
                                        str(t.b1) == str(p.id)
                                        and str(t.b2) == str(b.id)
                                    ) or (
                                        (
                                            str(t.b2) == str(p.id)
                                            and str(t.b1) == str(b.id)
                                        )
                                    ):
                                        tube_exists = True
                                if tube_exists == False:
                                    actions.append(
                                        "TUBE " + str(p.id) + " " + str(b.id)
                                    )
                                    # tubes.append(tube(p.id, b.id, 1))
                                    resources -= tubecost(p, b)
                                    p.conns += 1
                                    b.conns += 1

                                if resources >= 1000:
                                    pod_exists = False
                                    for pp in pods:
                                        if str(p.id) in str(pp.path) and str(
                                            b.id
                                        ) in str(pp.path):
                                            pod_exists = True
                                    if pod_exists == False:
                                        actions.append(
                                            "POD "
                                            + str(nextpod)
                                            + " "
                                            + str(p.id)
                                            + " "
                                            + str(b.id)
                                            + " "
                                            + str(p.id)
                                        )
                                        resources -= 1000
                                        nextpod += 1

        # build teleport if enough resources exist
        if resources > 5000:
            for t in tubes:
                actions.append("TELEPORT " + str(t.b1) + " " + str(t.b2))
                resources -= 5000


def add_teleport():
    global resources
    # build teleport if enough resources exist

    for p in pads:
        for b in buildings:
            if resources < 5000:
                return
            if str(b.type) in p.astros:
                port_exists = False
                for por in ports:
                    if (
                        por.b1 == p.id
                        or por.b1 == b.id
                        or por.b2 == p.id
                        or por.b2 == b.id
                    ):
                        port_exists = True
                if port_exists == False:
                    actions.append("TELEPORT " + str(p.id) + " " + str(b.id))
                    ports.append(port(p.id, b.id))
                    resources -= 5000


# game loop
buildings = []
pads = []
resources = 0
nextpod = 1
while True:

    pods = []

    ports = []
    tubes = []
    actions = []

    resources = int(input())
    num_travel_routes = int(input())
    for i in range(num_travel_routes):
        building_id_1, building_id_2, capacity = [int(j) for j in input().split()]
        if capacity == 0:
            ports.append(port(building_id_1, building_id_2))
        else:
            tubes.append(tube(building_id_1, building_id_2, capacity))

    num_pods = int(input())

    for i in range(num_pods):
        p_props = input()
        pods.append(pod(int(p_props[0]), p_props[2:]))
    num_new_buildings = int(input())
    for i in range(num_new_buildings):
        bp = input().split()
        if bp[0] == "0":
            pads.append(pad(int(bp[1]), position(int(bp[2]), int(bp[3])), bp[5:]))
            # print("added pad... with " + str(pads[-1].astros), file=sys.stderr, flush=True)
        else:
            buildings.append(
                building(int(bp[1]), int(bp[0]), position(int(bp[2]), int(bp[3])))
            )
            # print("added building...", file=sys.stderr, flush=True)

    # link pads and buildings

    addactions()
    add_teleport()

    # calculate cost of action
    # predict value of action
    # add teleport
    # add upgrade

    output = ";".join(actions)
    if output == "":
        output = "WAIT"

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    print(output)
