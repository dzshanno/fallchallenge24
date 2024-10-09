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


def dist_from_line(b: building, t: tube) -> int:
    x1 = t.b1.pos.x
    y1 = t.b1.pos.y

    x2 = t.b2.pos.x
    y2 = t.b2.pos.y

    x0 = b.pos.x
    y0 = b.pos.y

    d = abs(((y2 - y1) * x0) - ((x2 - x1) * y0) + (x2 * y1) - (y2 * x1)) / (
        math.sqrt((y2 - y1) ** 2 + (x2 - x1) ** 2)
    )

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


def blocked_tube(t):
    bintercept = None
    tintercept = []
    tube_length = dist(t.b1.pos, t.b2.pos)
    for b in buildings_within(tube_length, t.b1):
        if point_intersect(b.pos, t.b1.pos, t.b2.pos) and b != t.b1 and b != t.b2:
            bintercept = b

    for nt in nearest_tubes(t.b1):
        if lineIntersect(nt.b1.pos, nt.b2.pos, t.b1.pos, t.b2.pos):
            tintercept.append(nt)

    if bintercept is not None:
        # print("bintercept " + str(bintercept), file=sys.stderr, flush=True)
        min_intercept = dist(t.b1.pos, bintercept.pos)
    else:
        min_intercept = 10000
    intercepter = bintercept
    for ti in tintercept:
        dfl = dist_from_line(t.b1, ti)
        if dfl < min_intercept:
            min_intercept = dfl
            intercepter = ti

    return intercepter


def point_intersect(A, B, C):
    # is position A on the line between position B and position C
    epsilon = 0.0000001
    onpath = -epsilon < dist(B, A) + dist(A, C) - dist(B, C) < epsilon
    return onpath


def tubecost(t):
    cost = math.floor(dist(t.b1.pos, t.b2.pos) / 0.1)
    return cost


def suppliers():
    s = []
    for b in buildings:
        if sum(b.supply) != 0:
            s.append(b)
    # print("suppliers " + str(s), file=sys.stderr, flush=True)
    return s


def top_suppliers():
    # find the one or many buildings with the most astros still to house

    # loop through all the buildings with astros still looking for homes
    maxsupply = 0
    maxtype = -1
    ts = []
    for s in suppliers():
        # print("supply " + str(s.supply), file=sys.stderr, flush=True)
        for typ, num in enumerate(s.supply):
            if num > maxsupply:
                maxsupply = num
                maxtype = typ
                ts = [(s, typ, num)]
            elif num == maxsupply:
                ts.append((s, typ, num))
    # print("top suppliers " + str(ts), file=sys.stderr, flush=True)
    return ts


def addactions():
    global resources, nextpod
    if resources > 0:
        for p in pads:
            if p.conns < 5:
                print("checking pad " + str(p.id), file=sys.stderr, flush=True)
                for b in nearest_buildings(p):
                    for a, num in enumerate(p.supply):
                        if num != 0:
                            if b.conns < 5 and p.conns < 5:
                                if len(actions) > 500:
                                    print(
                                        "toomany actions ", file=sys.stderr, flush=True
                                    )
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
                                    if tube_exists == False and not blocked_tube(
                                        tube(p, b, 1)
                                    ):
                                        actions.append(
                                            "TUBE " + str(p.id) + " " + str(b.id)
                                        )
                                        tubes.append(tube(p, b, 1))
                                        resources -= tubecost(tube(p, b, 1))
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


def next_action():
    global resources, nextpod, new_action
    if suppliers():
        t = next_tube()
        if t:
            actions.append("TUBE " + str(t.b1.id) + " " + str(t.b2.id))
            # print("create tube " + str(t.b1)+":"+str(t.b2), file=sys.stderr, flush=True)
            tubes.append(t)
            new_action = True
            resources -= tubecost(t)
            t.b1.conns += 1
            t.b2.conns += 1
    else:
        new_action = False

    nps = next_pods()
    if nps:
        for np in nps:
            # print("next pod: " + str(np.path), file=sys.stderr, flush=True)
            actions.append(
                "POD " + str(np.id) + " " + " ".join(str(i) for i in np.path)
            )
            pods.append(np)
            new_action = True

            resources -= 1000

            startb = np.path[0]
            endb = np.path[1]
            for typ, num in enumerate(startb.supply):
                if typ not in endb.demand:
                    endb.supply[typ] += startb.supply[typ]
            for d in endb.demand:
                startb.supply[int(d)] = 0
                startb.demand.append(d)

            for p in pods:
                for b in p.path:
                    for d in b.demand:
                        for bb in p.path:
                            bb.supply[d] = 0
    else:
        new_action = False


def tube_exists(t) -> bool:
    for t2 in tubes:
        if (t2.b1 == t.b1 and t2.b2 == t.b2) or (t2.b1 == t.b2 and t2.b2 == t.b1):
            return True
    return False


def next_tube() -> tube:
    # from the top suppliers find the closest home
    global resources
    best_tube = None
    blockedtube = None
    tubeblocker = None
    for s, type, num in top_suppliers():
        mindist = 10000
        bests = None
        bestb = None
        for b in buildings:
            if b == s:
                continue
            next_tube = tube(s, b, 1)
            if tube_exists(next_tube):
                # print("tube exists " + str(s.id)+":"+str(b.id), file=sys.stderr, flush=True)
                continue
            if b.conns == 5 or s.conns == 5:
                continue
            if type in b.demand:
                newdist = dist(b.pos, s.pos)
                if (
                    newdist < mindist
                    and tubecost(next_tube) < resources
                    and not blocked_tube(next_tube)
                ):
                    mindist = newdist
                    best_tube = next_tube
                    bests = s
                    bestb = b
                if blocked_tube(next_tube):
                    blockeds = s
                    blockedtube = next_tube
                    tubeblocker = blocked_tube(next_tube)
    if not best_tube and blockedtube:
        print(
            "only blocked tubes available" + str(blockedtube),
            file=sys.stderr,
            flush=True,
        )
        if isinstance(tubeblocker, building):
            best_tube = tube(blockeds, tubeblocker, 1)
        if isinstance(tubeblocker, tube):
            best_tube = tube(blockeds, tubeblocker.b1, 1)
    return best_tube


def next_pods() -> pod:
    global resources, nextpod
    new_pods = []
    if resources >= 1000:
        for t in tubes:
            pod_exists = False
            # print("checking tube " + str(t.b1.id)+":"+str(t.b2.id), file=sys.stderr, flush=True)
            for p in pods:
                # print("in pod " + str(p.id)+" with path"+str(p.path), file=sys.stderr, flush=True)
                if t.b1 in p.path and t.b2 in p.path:
                    pod_exists = True
            if not pod_exists:
                new_pods.append(pod(nextpod, [t.b1, t.b2, t.b1]))
                nextpod += 1
    return new_pods


def buildings_within(x: int, b1: building):
    blist = []
    for b in nearest_buildings(b1):
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
        pathlist = [find_building_from_id(int(p)) for p in p_props[2:]]
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

    if len(buildings) > 21:
        addactions()

    else:

        new_action = True
        while new_action and resources > 0:
            # print(str(b.id)+" supply:"+str(b.supply), file=sys.stderr, flush=True)
            pass
            next_action()

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
