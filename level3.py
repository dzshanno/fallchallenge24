import sys
import math


class position:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y


# Given three collinear points p, q, r, the function checks if
# point q lies on line segment 'pr'
def onSegment(p, q, r):
    if (
        (q.x <= max(p.x, r.x))
        and (q.x >= min(p.x, r.x))
        and (q.y <= max(p.y, r.y))
        and (q.y >= min(p.y, r.y))
    ):
        return True
    return False


def orientation(p, q, r):
    # to find the orientation of an ordered triplet (p,q,r)
    # function returns the following values:
    # 0 : Collinear points
    # 1 : Clockwise points
    # 2 : Counterclockwise

    # See https://www.geeksforgeeks.org/orientation-3-ordered-points/amp/
    # for details of below formula.

    val = (float(q.y - p.y) * (r.x - q.x)) - (float(q.x - p.x) * (r.y - q.y))
    if val > 0:

        # Clockwise orientation
        return 1
    elif val < 0:

        # Counterclockwise orientation
        return 2
    else:

        # Collinear orientation
        return 0


# The main function that returns true if
# the line segment 'p1q1' and 'p2q2' intersect.
def lineIntersect(p1: position, q1: position, p2: position, q2: position) -> bool:

    # Find the 4 orientations required for
    # the general and special cases
    o1 = orientation(p1, q1, p2)
    o2 = orientation(p1, q1, q2)
    o3 = orientation(p2, q2, p1)
    o4 = orientation(p2, q2, q1)
    # special case of joined at ends

    if p1 == p2 or p1 == q2 or q1 == p2 or q1 == q2:
        return False

    # General case
    if (o1 != o2) and (o3 != o4):
        return True

    # Special Cases

    # p1 , q1 and p2 are collinear and p2 lies on segment p1q1
    if (o1 == 0) and onSegment(p1, p2, q1):
        return True

    # p1 , q1 and q2 are collinear and q2 lies on segment p1q1
    if (o2 == 0) and onSegment(p1, q2, q1):
        return True

    # p2 , q2 and p1 are collinear and p1 lies on segment p2q2
    if (o3 == 0) and onSegment(p2, p1, q2):
        return True

    # p2 , q2 and q1 are collinear and q1 lies on segment p2q2
    if (o4 == 0) and onSegment(p2, q1, q2):
        return True

    # If none of the cases
    return False


# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.


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
    def __init__(self, id: int, type: int, pos: position, astros: list = []) -> None:
        self.id = id
        self.type = type
        self.pos = pos
        self.conns = 0
        self.astros = astros
        self.homed = []

    def __str__(self) -> str:
        return str(self.id)

    def __repr__(self) -> str:
        return str(self.id)

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

            return True

    for t in tubes:
        if lineIntersect(t.b1.pos, t.b2.pos, b1.pos, b2.pos):

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


def pathexists(b1, b2):
    for t in tubes:
        if (t.b1 == b1 and t.b2 == b2) or (t.b1 == b2 and t.b2 == b1):
            return True
    return False


def nearest_buildings(pad: building):
    blist = []
    for b in buildings:
        distance = dist(pad.pos, b.pos)
        blist.append((distance, b))
    blist = sorted(blist)
    output2 = []
    for b in blist:
        output2.append(b[1])
    # print("buildings in order " + str(output2), file=sys.stderr, flush=True)
    return output2


def addactions():
    global resources, nextpod

    if resources > 0:
        for p in pads:
            # print("checking pad " + str(p.id), file=sys.stderr, flush=True)
            for b in nearest_buildings(p):
                if b.conns >= 5 or p.conns >= 5:
                    # print("5 connections already ", file=sys.stderr, flush=True)
                    continue
                # print("checking "+str(len(p.astros))+" astros from pad " + str(p.id), file=sys.stderr, flush=True)
                for a in p.astros:

                    if len(actions) > 500:
                        print("too many actions ", file=sys.stderr, flush=True)
                        return

                    if int(b.type) == int(a):
                        tube_exists = False
                        for t in tubes:
                            if (str(t.b1) == str(p.id) and str(t.b2) == str(b.id)) or (
                                (str(t.b2) == str(p.id) and str(t.b1) == str(b.id))
                            ):
                                # print("tube "+str(t.b1)+":"+str(t.b2)+" exists ", file=sys.stderr, flush=True)
                                tube_exists = True
                        if tube_exists == False and not blocked_tube(p, b):
                            actions.append("TUBE " + str(p.id) + " " + str(b.id))
                            tubes.append(tube(p, b, 1))
                            resources -= tubecost(p, b)

                            # TODO reset conns when connection doesnt go through
                            p.conns += 1
                            b.conns += 1

                        if resources >= 1000:
                            pod_exists = False
                            for pp in pods:
                                if p.id in pp.path and b.id in pp.path:
                                    print(
                                        "path between "
                                        + str(p.id)
                                        + " and "
                                        + str(b.id)
                                        + " exists with pod "
                                        + str(pp.id)
                                        + " path:"
                                        + str(pp.path),
                                        file=sys.stderr,
                                        flush=True,
                                    )
                                    pod_exists = True
                            if pod_exists == False and pathexists(p, b):

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
                                pods.append(pod(nextpod, [p.id, b.id, p.id]))
                                print(
                                    "create pod: "
                                    + str(nextpod)
                                    + " - "
                                    + str(p.id)
                                    + ":"
                                    + str(b.id),
                                    file=sys.stderr,
                                    flush=True,
                                )
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


def find_building_from_id(id: int) -> building:
    for b in buildings:
        if b.id == id:
            return b
    return False


# game loop
buildings = []
resources = 0
nextpod = 1
while True:

    pods = []
    pads = []
    ports = []
    tubes = []
    actions = []

    resources = int(input())
    num_travel_routes = int(input())

    # reset conns numbers
    for b in buildings:
        b.conns = 0

    for i in range(num_travel_routes):
        building_id_1, building_id_2, capacity = [int(j) for j in input().split()]
        b1 = find_building_from_id(building_id_1)
        b2 = find_building_from_id(building_id_2)

        if capacity == 0:
            ports.append(port(b1, b2))
        else:
            tubes.append(tube(b1, b2, capacity))
            b1.conns += 1
            b2.conns += 1

    num_pods = int(input())
    for i in range(num_pods):
        p_props = input().split()
        pathlist = [int(p) for p in p_props[2:]]
        pods.append(pod(int(p_props[0]), pathlist))

    num_new_buildings = int(input())
    for i in range(num_new_buildings):
        bp = input().split()
        if bp[0] == "0":
            buildings.append(
                building(
                    int(bp[1]), int(bp[0]), position(int(bp[2]), int(bp[3])), bp[5:]
                )
            )
        else:
            buildings.append(
                building(int(bp[1]), int(bp[0]), position(int(bp[2]), int(bp[3])))
            )

    # link pads and buildings
    for b in buildings:
        if b.type == 0:
            pads.append(b)
            # print("created " + str(len(pads))+" pods ", file=sys.stderr, flush=True)

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
