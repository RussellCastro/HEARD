import goPID

#adjacency list
route_graph = {
    'hallway_home': ['null', 'hallway_turn'],
    'hallway_turn': ['hallway_home', 'door_tags'],
    'door_tags': ['hallway_turn', 'door_enter'],
    'door_enter': ['door_tags', 'startstop_scan'],
    'startstop_scan': ['door_enter', 'scan2'],
    'scan2': ['startstop_scan', 'scan3'],
    'scan3': ['scan2', 'scan4'],
    'scan4': ['scan3', 'scan4'],


}

#position list
point_poses = {

}

#go to door
def navi_to_scan(start_node, target_node, direction):
  path = simple_path(start_node, target_node, direction)
  current_point = path[0]
  for waypoint in path:
      relative_target = point_poses[waypoint] - current_point
      goPID.goPID(relative_target[0], relative_target[1], relative_target[2], 5, 5, 5)
      current_point = waypoint
    
#go sweep/scan
def scan(start_node, target_node, direction):
  path = simple_path(start_node, target_node, direction)
  current_point = path[0]
  for waypoint in path:
      relative_target = point_poses[waypoint] - current_point
      goPID.goPID(relative_target[0], relative_target[1], relative_target[2], 5, 5, 5)
      current_point = waypoint

#find path
def simple_path(start_node, target_node, direction):
  output_path = []
  if direction == True:
    index_dir = 1
  else:
    index_dir = 0
  current_node = start_node
  while current_node != target_node:
    output_path.append(current_node)
    current_node = route_graph[current_node][index_dir]

  return output_path