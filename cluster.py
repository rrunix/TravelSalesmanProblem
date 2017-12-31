def point_avg(points):
    x = 0
    y = 0

    for px, py in points:
        x += px
        y += py

    if len(points) > 0:
        x /= len(points)
        y /= len(points)

    return [x, y]


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return "Point(%d, %d)" % (self.x, self.y)

    def __repr__(self):
        return self.__str__()

    def is_group(self):
        return False


class PointGroup(Point):
    def __init__(self, pgroups):
        super().__init__(*point_avg(pgroups))
        self.pgroups = set(pgroups)

    def join(self, pgroup):
        return PointGroup(self.pgroups | pgroup.pgroups)

    def intersects_with(self, pgroup):
        return len(self.pgroups & pgroup.pgroups) > 0

    def is_group(self):
        return True

    def __str__(self):
        return "PointGroup(%d, %d)" % (self.x, self.y)

def two_group(kdtree, points):
    new_points = list()
    points_group = list()
    seen = set()

    for i, p0 in enumerate(points):
        if p0 not in seen:
            seen.add(p0)
            p1_dist, p1_index = T.query(p0, k=2)[1]
            p1_point = points[p1_index]

            near_p1_dist, near_p1_index = T.query(p1_point, k=2)[1]

            if i == near_p1_index or near_p1_dist > p1_dist:
                seen.add(p1_point)
                points_group.append(PointGroup([p0, p1_point]))
            else:
                new_points.append(Point(*p0))

    i = 0
    new_points_group = list()
    while i < len(points_group):
        group = points_group[i]

        i += 1
        j = i
        while j < len(points_group):
            group_j = points_group[j]

            if group.intersects_with(group_j):
                group = group.join(group_j)
                points_group.remove(group_j)
            else:
                j += 1

        new_points_group.append(group)

    return new_points + new_points_group