from astronave import Astronave

def game_controller(game_status, elements):
    if game_status == "init":
        player = Astronave()
        elements.add(player)
    return True, elements
