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

    def __lt__(self, other):
        if self.id < other.id:
            return True
        else:
            return False


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
    d = math.sqrt(((b1.x - b2.x) ** 2) + ((b1.y - b2.y) ** 2))
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


def blocked_tube(b1, b2):
    for b in buildings:
        if point_intersect(b.pos, b1.pos, b2.pos) and b != b1 and b != b2:
            print(
                "tube: "
                + str(b1.id)
                + ":"
                + str(b2.id)
                + " blocked by building "
                + str(b.id),
                file=sys.stderr,
                flush=True,
            )
            print(
                "dist: "
                + str(b1.id)
                + ":"
                + str(b2.id)
                + " is "
                + str(dist(b1.pos, b2.pos)),
                file=sys.stderr,
                flush=True,
            )

            return True
    for p in pads:
        if point_intersect(p.pos, b1.pos, b2.pos) and p != b1 and p != b2:
            print(
                "tube: "
                + str(b1.id)
                + ":"
                + str(b2.id)
                + " blocked by pad"
                + str(b.id),
                file=sys.stderr,
                flush=True,
            )
            return True
    return False


def point_intersect(A, B, C):
    # is position A on the line between position B and position C
    epsilon = 0.0000001
    onpath = -epsilon < dist(B, A) + dist(A, C) - dist(B, C) < epsilon
    return onpath


def tubecost(b1, b2):
    cost = math.floor(dist(b1.pos, b2.pos) * 0.1)
    return cost


def nearest_buildings(pad):
    blist = []
    for b in buildings:
        distance = dist(pad.pos, b.pos)
        blist.append((distance, b))
    blist = sorted(blist)
    output2 = []
    for b in blist:
        output2.append(b[1])
    return output2


def addactions():
    global resources, nextpod
    if resources > 0:
        for p in pads:
            if p.conns < 5:
                print("checking pad " + str(p.id), file=sys.stderr, flush=True)
                for b in nearest_buildings(p):
                    for a in p.astros:
                        if b.conns < 5 and p.conns < 5:
                            if len(actions) > 500:
                                print("toomany actions ", file=sys.stderr, flush=True)
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
                                if tube_exists == False and not blocked_tube(p, b):
                                    actions.append(
                                        "TUBE " + str(p.id) + " " + str(b.id)
                                    )
                                    tubes.append(tube(p.id, b.id, 1))
                                    resources -= tubecost(p, b)
                                    print(
                                        "resources now: " + str(resources),
                                        file=sys.stderr,
                                        flush=True,
                                    )

                                    # TODO reset conns when connection doesnt go through
                                    p.conns += 1
                                    b.conns += 1

                                if resources >= 1000:
                                    pod_exists = False
                                    for pp in pods:
                                        if str(p.id) in str(pp.path) and str(
                                            b.id
                                        ) in str(pp.path):
                                            # print("path between "+str(p.id)+" and "+str(b.id)+ " exists with pod "+str(pp.id)+" path:"+str(pp.path), file=sys.stderr, flush=True)
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
                                        pods.append(
                                            pod(
                                                nextpod,
                                                str(p.id)
                                                + " "
                                                + str(b.id)
                                                + " "
                                                + str(p.id),
                                            )
                                        )
                                        # print("create pod: "+str(nextpod)+" - "+str(p.id)+":"+str(b.id), file=sys.stderr, flush=True)
                                        resources -= 1000
                                        nextpod += 1


def add_teleport():
    global resources
    # build teleport if enough resources exist

    for p in pads:
        for b in reversed(nearest_buildings(p)):
            if resources < 20000:
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

    # reset conns numbers
    for b in buildings:
        b.conns = 0
    for p in pads:
        p.conns = 0

    for i in range(num_travel_routes):
        building_id_1, building_id_2, capacity = [int(j) for j in input().split()]
        if capacity == 0:
            ports.append(port(building_id_1, building_id_2))
        else:
            tubes.append(tube(building_id_1, building_id_2, capacity))
            for p in pads:
                if p.id == building_id_1 or p.id == building_id_2:
                    p.conns += 1
            for b in buildings:
                if b.id == building_id_1 or b.id == building_id_2:
                    b.conns += 1

    num_pods = int(input())
    for i in range(num_pods):
        p_props = input().split()
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
    # add_teleport()

    # work to closest buildings first
    # calculate cost of action
    # predict value of action

    # add upgrade

    output = ";".join(actions)
    if output == "":
        output = "WAIT"

    # Write an action using print
    # To debug: print("Debug messages...", file=sys.stderr, flush=True)

    # TUBE | UPGRADE | TELEPORT | POD | DESTROY | WAIT
    print(output)
