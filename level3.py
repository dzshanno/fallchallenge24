import sys
import math
from operator import add


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
    def __init__(self, id: int, type: int, pos: position) -> None:
        self.id = id
        self.type = type
        self.pos = pos
        self.conns = 0
        self.homed = []
        self.demand = []
        self.supply = []
        for i in range(21):
            self.supply.append(0)

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

    def __lt__(self, other):
        if self.b1.id < other.b1.id:
            return True
        else:
            return False


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


def suppliers():
    output = []
    for b in buildings:
        if sum(b.supply) != 0:
            output.append(b)
    return output


def blocked_tube(b1, b2):
    tube_length = dist(b1.pos, b2.pos)
    for b in buildings_within(tube_length, b1):
        if point_intersect(b.pos, b1.pos, b2.pos) and b != b1 and b != b2:

            return True

    for t in nearest_tubes(b1):
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


def top_suppliers():
    # find the one or many buildings with the most astros still to house

    # loop through all the buildings with astros still looking for homes
    maxsupply = 0
    maxtype = -1
    topsuppliers = []
    for s in suppliers():
        for num, type in enumerate(s.supply):
            if num > maxsupply:
                maxsupply = num
                maxtype = type
                topsuppliers = [(s, type, num)]
            if num == maxsupply:
                topsuppliers.append((s, type, num))


def next_tube() -> tube:
    # from the top suppliers find the closest home

    for s, type, num in top_suppliers():
        mindist = 10000
        bests, bestb = None
        for b in buildings:
            if b == s:
                continue
            if type in b.demand:
                newdist = dist(b.pos, s.pos)
                if newdist < mindist:
                    mindist = newdist
                    bests = s
                    bestb = b
    best_tube = tube(bestb, bests, 1)
    return best_tube


def nearest_building_for_max_supply2(b1: building):
    output = []
    for type, num in enumerate(b1.supply):
        if num == 0:
            continue
        mindist = 10000
        maxnum = 0
        for b2 in buildings:
            if b1 != b2:
                if type in b2.demand:
                    # if not blocked_tube(b1,b2):
                    newdist = dist(b1.pos, b2.pos)
                    if newdist < mindist:
                        mindist = newdist
                        bestb = b2
        output.append((num, mindist, bestb, type))
    output.sort(key=lambda d: (-d[0], d[1]))
    print("buildings " + str(output), file=sys.stderr, flush=True)
    return output


def buildings_within(x: int, b1: building):
    blist = []
    for b in buildings:
        distance = dist(b1.pos, b.pos)
        if distance < x:
            blist.append(b)
    return blist


def tubes_within(x: int, b1: building):
    blist = []
    for b in buildings:
        distance = dist(b1.pos, b.pos)
        if distance < x:
            blist.append(b)
    return blist


def nearest_buildings(b1: building):
    blist = []
    for b in buildings:
        distance = dist(b1.pos, b.pos)
        blist.append((distance, b))
    blist = sorted(blist)
    output2 = []
    for b in blist:
        output2.append(b[1])
    return output2


def nearest_tubes(b1: building):
    tlist = []
    for t in tubes:
        distance = dist(b1.pos, t.b1.pos)
        tlist.append((distance, t))
    tlist = sorted(tlist)
    output2 = []
    for t in tlist:
        output2.append(t[1])
    return output2


def addactions():
    global resources, nextpod

    if resources > 0:
        for p in buildings:
            for n, d, b, a in nearest_building_for_max_supply2(p):
                if b.conns >= 5 or p.conns >= 5:
                    continue
                tube_exists = False
                for t in tubes:
                    if (str(t.b1) == str(p.id) and str(t.b2) == str(b.id)) or (
                        (str(t.b2) == str(p.id) and str(t.b1) == str(b.id))
                    ):
                        tube_exists = True
                if tube_exists == False:
                    if not blocked_tube(p, b):
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

                        p.demand.append(a)
                        b.supply = list(map(add, p.supply, b.supply))
                        resources -= 1000
                        nextpod += 1


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
        new_building = building(
            int(bp[1]), int(bp[0]), position(int(bp[2]), int(bp[3]))
        )

        if bp[0] == "0":
            astros = bp[5:]
            for a in astros:
                new_building.supply[int(a)] += 1
        else:
            new_building.demand.append(new_building.type)

        # print("created building " + str(new_building), file=sys.stderr, flush=True)
        buildings.append(new_building)

    # link pads and buildings
    for b in buildings:
        if sum(b.supply) != 0:
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
