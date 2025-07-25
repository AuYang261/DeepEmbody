import sys
sys.path.append(".")
sys.path.append("./simulator/genesis")

from manager.graph.entity import *
from driver.sim_genesis_ranger.driver import move_to_point

root = None


def sim_gen_graph():
    global root
    root = create_root_room()
    print(f"ID = {root.entity_id}, path = {root.get_absolute_path()}")

    room: Room = create_room_entity("room")
    root.add_child(room)
    print(f"ID = {room.entity_id}, path = {room.get_absolute_path()}")

    ranger: Entity = create_controllable_entity("ranger")
    room.add_child(ranger)
    print(f"ID = {ranger.entity_id}, path = {ranger.get_absolute_path()}")

    book1: Entity = create_generic_entity("book1")
    room.add_child(book1)
    print(f"ID = {book1.entity_id}, path = {book1.get_absolute_path()}")

    # Bind getpos primitive to book1, always returns fixed position
    book1.bind_primitive("getpos", lambda: {"x": -2.2, "y": 1.8, "z": 0.1})

    # Bind move primitive to ranger, calls move_to_point from driver
    def move_impl(x, y, z):
        # Only x, y are used for movement, z is ignored
        move_to_point(x, y)
        return {"success": True}
    ranger.bind_primitive("move", move_impl)


def sim_run_flow():
    book1 = root.get_entity_by_path("room/book1")
    ranger = root.get_entity_by_path("room/ranger")
    print(
        f"book1 = {book1.get_absolute_path()}, ranger = {ranger.get_absolute_path()}")

    book1_pos = book1.getpos()
    print(f"book1_pos = {book1_pos}")
    print(f"ranger = {ranger}")
    ranger.move(x=book1_pos["x"], y=book1_pos["y"], z=book1_pos["z"])
    
    # create a virtual entity at the origin point
    virtual_waypoint1 = create_generic_entity("virtual_waypoint1")
    virtual_waypoint1.bind_primitive("getpos", lambda: {"x": 0.0, "y": 0.0, "z": 0.0})
    root.get_entity_by_path("room").add_child(virtual_waypoint1)
    print(f"virtual_waypoint1 = {virtual_waypoint1.get_absolute_path()}")
    
    ranger.move(x=virtual_waypoint1.getpos()["x"], y=virtual_waypoint1.getpos()["y"], z=virtual_waypoint1.getpos()["z"])

def main():
    sim_gen_graph()
    sim_run_flow()
    print("flow1 done")

if __name__ == "__main__":
    main()
