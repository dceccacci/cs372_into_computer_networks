import sys
import json
import math  # If you want to use math.inf for infinity

def dijkstras_shortest_path(routers, src_ip, dest_ip):
    """
    This function takes a dictionary representing the network, a source
    IP, and a destination IP, and returns a list with all the routers
    along the shortest path.

    The source and destination IPs are **not** included in this path.

    Note that the source IP and destination IP will probably not be
    routers! They will be on the same subnet as the router. You'll have
    to search the routers to find the one on the same subnet as the
    source IP. Same for the destination IP. [Hint: make use of your
    find_router_for_ip() function from the last project!]

    The dictionary keys are router IPs, and the values are dictionaries
    with a bunch of information, including the routers that are directly
    connected to the key.

    This partial example shows that router `10.31.98.1` is connected to
    three other routers: `10.34.166.1`, `10.34.194.1`, and `10.34.46.1`:

    {
        "10.34.98.1": {
            "connections": {
                "10.34.166.1": {
                    "netmask": "/24",
                    "interface": "en0",
                    "ad": 70
                },
                "10.34.194.1": {
                    "netmask": "/24",
                    "interface": "en1",
                    "ad": 93
                },
                "10.34.46.1": {
                    "netmask": "/24",
                    "interface": "en2",
                    "ad": 64
                }
            },
            "netmask": "/24",
            "if_count": 3,
            "if_prefix": "en"
        },
        ...

    The "ad" (Administrative Distance) field is the edge weight for that
    connection.

    **Strong recommendation**: make functions to do subtasks within this
    function. Having it all built as a single wall of code is a recipe
    for madness.
    """
    
    # Set up
    sourceRouter = find_router_for_ip(routers, src_ip)
    destinationRouter = find_router_for_ip(routers, dest_ip)
    to_visit, distance, parent = initialize_arrays(routers, sourceRouter)

    # Find path
    map_paths(to_visit, distance, routers, parent)
    path = find_path(sourceRouter, destinationRouter, parent)
    
    return path


def initialize_arrays(routers, sourceRouter):
    """Takes a dictionary of routers and returns "Set-Up" values

    Args:
        routers (Dictionary): A dictionary of router IPs and which IPs they are connected to

    Returns:
        Tuple:
            1: Set with all of the "children" IPs found in the router dictionary.
            2: Dictionary representing the distance between IPs, with the distance (value) set to infinite
            3: Dictionary representing child to parent nodes, with parent node (value) set to None
    """
    # list of nodes we still need to visit
    to_visit = set()
    # Holds the distance from any node to the start node
    distance = {}
    # for any given node (key) lists the key for parent leading back to the starting node.
    parent = {}

    # For each parent node
    for ip in routers:
        # For each of its children
        for connectedIP in routers[ip]["connections"]:
            to_visit.add(connectedIP)
            distance[connectedIP] = math.inf
            parent[connectedIP] = None

    # Make sure that the starting distance is set to 0
    distance[sourceRouter] = 0

    return to_visit, distance, parent

def get_smallest_distance(to_visit, distance):
    """From the dictionary distance, return the smallest distance and its IP

    Args:
        to_visit (Set): Nodes that are still needed to be visited
        distance (Dictionary): distance from start to each router

    Returns:
        String: The IP address of the router with the smallest distance
    """
    # Set up
    smallest_value = math.inf
    smallest_values_IP = None

    # for each node still need visiting, get the one with the smallest distance
    for keyIP in to_visit:
        if distance[keyIP] < smallest_value:
            smallest_value = distance[keyIP]
            smallest_values_IP = keyIP

    return smallest_values_IP

def find_neighbors(currentNode, to_visit, routers):
    """
    Find the neighbors of the currentNode that are still in to_visit and 
    return a list of those nodes.

    Args:
        currentNode (Str): The current Nodes Router IP
        to_visit (Set): A set of all router nodes still need visiting
        routers (Dictionary): A dictionary of router IPs and which IPs they are connected to

    Returns:
        List: A list of the unvisited neighbors of the current node
    """
    unvisitedNeighbors = []
    for neighbor in routers[currentNode]["connections"]:
        if neighbor in to_visit:
            unvisitedNeighbors.append(neighbor)

    return unvisitedNeighbors

def map_paths(to_visit, distance, routers, parent):
    """Maps the paths from the start node to all other nodes

    Args:
        to_visit (Set): Nodes that are still needed to be visited
        distance (Dictionary): distance from start to each router
        routers (Dictionary): A dictionary of router IPs and which IPs they are connected to
        parent (Dictionary): A dictionary that contains children nodes(key) to their parents(value)
    """
    while len(to_visit) > 0:
        currentNode = get_smallest_distance(to_visit, distance)
        to_visit.remove(currentNode)
        currentNodeNeighbors = find_neighbors(currentNode, to_visit, routers)

        # For each neighbor of the current node
        for neighbor in currentNodeNeighbors:
            totalDistanceToNeighbor = get_distance_from_start_to_neighbor(currentNode, neighbor, distance, routers)
            if totalDistanceToNeighbor < distance[neighbor]:
                distance[neighbor] = totalDistanceToNeighbor
                parent[neighbor] = currentNode

def get_distance_from_start_to_neighbor(currentNode, neighbor, distance, routers):
    """Calculate the total distance from start to the neighbor node

    Args:
        currentNode (Str): The current node
        neighbor (Str): The neighbor of the current Node
        distance (Dictionary): The distances from each node from the start node
        routers (Dictionary): A dictionary of router IPs and which IPs they are connected to

    Returns:
        Int: the Total Distance from start to the neighbor node
    """
    currentNodeDistance = distance[currentNode]
    neighborDistance = routers[currentNode]["connections"][neighbor].get("ad")

    return currentNodeDistance + neighborDistance

def find_path(sourceRouter, destinationRouter, parent):
    """Finds the best path from the source router to the destination router

    Args:
        sourceRouter (Str): The IP of the source router
        destinationRouter (Str): The IP of the destination router
        parent (Dictionary): A dictionary that contains children nodes(key) to their parents(value)

    Returns:
        List: The path source router to destination router
    """
    currentNode = destinationRouter
    path = []
    while currentNode != sourceRouter:
        path.insert(0, currentNode)
        currentNode = parent[currentNode]
    if len(path) > 0:
        path.insert(0, sourceRouter)

    return path

# ------------ Functions from netfuncs.py below -----------------------

def ipv4_to_value(ipv4_addr):
        """
        Convert a dots-and-numbers IP address to a single 32-bit numeric
        value of integer type. Returns an integer type.
        """
        # Seperate on the period to get each byte chunk.
        splitByDot = ipv4_addr.split(".")

        # Add up the shifted bits to get the final value
        numericValue = 0
        numericValue += int(splitByDot[0]) << 24
        numericValue += int(splitByDot[1]) << 16
        numericValue += int(splitByDot[2]) << 8
        numericValue += int(splitByDot[3])

        return numericValue

def value_to_ipv4(addr):
        """
        Convert a single 32-bit numeric value of integer type to a
        dots-and-numbers IP address. Returns a string type.
        """

        # Empty List to hold each 8 bit chunk
        ipAddressParts = []

        # Grab each 8 bit chunk from the passed value, putting them into a list
        ipAddressParts.append(str((addr >> 24) & 0xff))
        ipAddressParts.append(str((addr >> 16) & 0xff))
        ipAddressParts.append(str((addr >> 8) & 0xff))
        ipAddressParts.append(str((addr >> 0) & 0xff))

        # Join the list on a period.
        finalIPAddress = ".".join(ipAddressParts)

        return finalIPAddress

def get_subnet_mask_value(slash):
        """
        Given a subnet mask in slash notation, return the value of the mask
        as a single number of integer type. The input can contain an IP
        address optionally, but that part should be discarded.

        Returns an integer type.
        """

        # Obtain how many bits the mask covers.
        splitBySlash = slash.split("/")
        slashValue = splitBySlash[-1]

        # Figure out how many 1's will cover the mask portion
        runOfOnes = ((1 << int(slashValue)) - 1)
        # Figure out how many 0's will cover the rest of the 32 bit IP
        zeroesToAdd = 32 - int(slashValue)

        # Shift the chunk of 1's over, creating 0's in their place.
        subnetMask = runOfOnes << zeroesToAdd

        return subnetMask

def ips_same_subnet(ip1, ip2, slash):
        """
        Given two dots-and-numbers IP addresses and a subnet mask in slash
        notataion, return true if the two IP addresses are on the same
        subnet.

        Returns a boolean.
        """

        # Grab subnet mask, and ip values.
        subnetMask = get_subnet_mask_value(slash)
        ip1Value = ipv4_to_value(ip1)
        ip2Value = ipv4_to_value(ip2)

        # Get the network number from each IP.
        ip1NetworkNum = ip1Value & subnetMask
        ip2NetworkNum = ip2Value & subnetMask

        # Return whether they are the same or not.
        return  ip1NetworkNum == ip2NetworkNum

def get_network(ip_value, netmask):
        """
        Return the network portion of an address value as integer type.
        """
        return ip_value & netmask

def find_router_for_ip(routers, ip):
    """
    Search a dictionary of routers (keyed by router IP) to find which
    router belongs to the same subnet as the given IP.

    Return None if no routers is on the same subnet as the given IP.
    """

    # Default return value
    ipInSameSubnet = None

    # For each IP in the router dictionary
    for ipInRouters in routers:
        # Get the network mask for each of those IPs
        netMaskSlash = routers[ipInRouters].get("netmask")
        # If they are on the same network
        if ips_same_subnet(ip, ipInRouters, netMaskSlash):
            # change the default value to this IP
            ipInSameSubnet = ipInRouters

    return ipInSameSubnet


#------------------------------
# DO NOT MODIFY BELOW THIS LINE
#------------------------------
def read_routers(file_name):
    with open(file_name) as fp:
        data = fp.read()

    return json.loads(data)

def find_routes(routers, src_dest_pairs):
    for src_ip, dest_ip in src_dest_pairs:
        path = dijkstras_shortest_path(routers, src_ip, dest_ip)
        print(f"{src_ip:>15s} -> {dest_ip:<15s}  {repr(path)}")

def usage():
    print("usage: dijkstra.py infile.json", file=sys.stderr)

def main(argv):
    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    routes = json_data["src-dest"]

    find_routes(routers, routes)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
