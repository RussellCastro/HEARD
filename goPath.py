import goPID

#adjacency list
route_graph = {
    'hallway_home': ['hallway_turn'],
    'hallway_turn': ['hallway_home', 'door_tags'],
    'door_tags': ['hallway_turn', 'door_enter'],
    'door_enter': ['door_tags', 'startstop_scan'],
    'startstop_scan': ['door_enter', 'scan2'],
    'scan2': ['startstop_scan', 'scan3'],
    'scan3': ['scan2', 'scan4'],
    'scan4': ['scan3', 'scan4'],


}

point_poses = {

}

def navi_to_scan(start_node, target_node):
    path = get_shortest_path(start_node, target_node)
    current_point = path[0]
    for waypoint in path:
        relative_target = point_poses[waypoint] - current_point
        goPID.goPID(relative_target[0], relative_target[1], relative_target[2], 5, 5, 5)
        current_point = waypoint

#def scan():

def try_to_relax(a, v, d, parent):
    if d[v] > d[a] + 1:
        d[v] = d[a] + 1
        parent[v] = a

def pop_min(pq):
  min_dist = float('inf')
  min_node = None
  for node in pq:
    if pq[node] < min_dist:
      min_dist = pq[node]
      min_node = node

  del pq[min_node]
  return min_node

def dijkstra(G, end):
    d, parent = {}, {}
    for node in G:
        d[node] = float('inf')
        parent[node] = None

    d[end] = 0
    visited = {end}

    pq = {}
    pq[end] = d[end]

    while pq != {}:
        v1 = pop_min(pq)
        visited.add(v1)

        for v2 in G[v1]:
            try_to_relax(v1, v2, d, parent)

            if v2 not in visited:
              pq[v2] = d[v2]

    return d, parent

def get_shortest_path(start, target):
  target_node = target
  output_list = [start]
  parents = dijkstra(route_graph, target)[1]
  go = True

  while go == True:
    current_node = parents[target_node]
    output_list.insert(0, current_node)
    target_node = current_node

    if current_node == start:
      go = False

  return output_list