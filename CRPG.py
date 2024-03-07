import sys
import os
import time
import random

##### Player Setup ######
class Player:
    def __init__(self):
        self.name = ''
        self.job = ''
        self.hp = 0
        self.mp = 0
        self.status_effects = []
        self.location = 'a1'
        self.game_over = False
        self.coins = 100  # Adding a coins attribute for the player
        self.inventory = []  # Adding an inventory list for the player

myPlayer = Player()

##### Title Screen #####
def title_screen_selections():
    option = input("> ")
    if option.lower() == "play":
        start_game()  # Placeholder until written
    elif option.lower() == "help":
        help_menu()
    elif option.lower() == "quit":
        sys.exit()
    while option.lower() not in ['play', 'help', 'quit']:
        print("Enter a valid command please")
        option = input("> ")
        if option.lower() == "play":
            start_game()  # Placeholder until written
        elif option.lower() == "help":
            help_menu()
        elif option.lower() == "quit":
            sys.exit()

def title_screen():
    os.system('cls' if os.name == 'nt' else 'clear')
    print('\033[93m' + '#--------------------------#' + '\033[0m')
    print('\033[93m' + '############################' + '\033[0m')
    print('\033[93m' + '# Welcome to the Text RPG! #' + '\033[0m')
    print('\033[93m' + '############################' + '\033[0m')
    print('\033[93m' + '#--------------------------#' + '\033[0m')
    print('          - \033[97mPlay\033[0m -          ')
    print('          - \033[97mHelp\033[0m -          ')
    print('          - \033[97mQuit\033[0m -          ')
    title_screen_selections()



def help_menu():
    print('\033[93m' + '############################' + '\033[0m')
    print('\033[93m' + '# Welcome to the Text RPG! #' + '\033[0m')
    print('\033[93m' + '############################' + '\033[0m')
    print('- Use up, down, left, right to move')
    print('- Type your commands to do them')
    print('- Use "look" to inspect something')
    print('- Type "inventory" to head to your inventory')
    print('- Use "quit" to quit anytime')
    print('- While in the shop, type "shop" to enter the shop')
    print('- You start out on the location "a1" and this game\'s locations go "a1-d4". I will not spoil the map layout so enjoy finding it out yourself')
    print('- The shop is down 1 location from your starting location')
    print('- Though not necessary, using the "look" command in all locations will make things more interesting and is encouraged')
    print('- On the map in the location "c4" if you use the "look" command you will be able to fight the first and only enemy in this game, Gobble the goblin')
    print('- Good luck and have fun!')
    title_screen_selections()



##### Game Functionality #####
def start_game():
    setup_game()
    main_game_loop()

##### Map #####
ZONENAME = 'ZONENAME'
DESCRIPTION = 'DESCRIPTION'
EXAMINATION = 'EXAMINATION'
SOLVED = 'SOLVED'
UP = 'UP'
DOWN = 'DOWN'
LEFT = 'LEFT'
RIGHT = 'RIGHT'

solved_places = {'a1': False, 'a2': False, 'a3': False, 'a4': False,
                 'b1': False, 'b2': False, 'b3': False, 'b4': False,
                 'c1': False, 'c2': False, 'c3': False, 'c4': False,
                 'd1': False, 'd2': False, 'd3': False, 'd4': False,
                }

zonemap = {
    'a1': {
        ZONENAME: "Town Market",
        DESCRIPTION: 'You enter a bustling market place in the town you just entered.',
        EXAMINATION: 'You look around and notice how crowded it is.',
        SOLVED: False,
        UP: '',
        DOWN: 'b1',
        LEFT: '',
        RIGHT: 'a2'
     },
     'a2': {
        ZONENAME: "Town Entrance",
        DESCRIPTION: 'You get to the new town\'s entrance, how welcoming!',
        EXAMINATION: 'You see how welcoming the entrance of the town makes you feel.',
        SOLVED: False,
        UP: '',
        DOWN: 'b2',
        LEFT: 'a1',
        RIGHT: 'a3'
     },
     'a3': {
        ZONENAME: "Town Square",
        DESCRIPTION: 'You enter town square, a very popular place in the town.',
        EXAMINATION: 'You decide to look around and you see a guy dancing in the middle of town square.',
        SOLVED: False,
        UP: '',
        DOWN: 'b3',
        LEFT: 'a2',
        RIGHT: 'a4'
     },
     'a4': {
        ZONENAME: "Town Hall",
        DESCRIPTION: 'You make it to the town hall and there is a giant speech happening.',
        EXAMINATION: 'You thought that the town hall was just a big hallway in this town, but boy were you wrong.',
        SOLVED: False,
        UP: '',
        DOWN: 'b4',
        LEFT: 'a3',
        RIGHT: ''
     },
     'b1': {
        ZONENAME: "Town Shop",
        DESCRIPTION: 'You enter the town shop, to look around and maybe buy something.',
        EXAMINATION: 'You look around and see many rare treasures around to buy.',
        SOLVED: False,
        UP: 'a1',
        DOWN: 'c1',
        LEFT: '',
        RIGHT: 'b2'
     },
     'b2': {
        ZONENAME: "Home",
        DESCRIPTION: 'This is your home!',
        EXAMINATION: 'Your home looks the same - nothing has changed.',
        SOLVED: False,
        UP: 'a2',
        DOWN: 'c2',
        LEFT: 'b1',
        RIGHT: 'b3'
     },
     'b3': {
        ZONENAME: "East Town Exit",
        DESCRIPTION: 'It\'s the main exit to the east of town.',
        EXAMINATION: 'This exit is definitely less welcoming than the town entrance. This exit is pretty similar to the South Exit.',
        SOLVED: False,
        UP: 'a3',
        DOWN: 'c3',
        LEFT: 'b2',
        RIGHT: 'b4'
     },
     'b4': {
        ZONENAME: "Forest Entrance",
        DESCRIPTION: 'You get close to entering the forest as you get to the entrance.',
        EXAMINATION: 'You look around, but you can only see forest and green as far as you can see.',
        SOLVED: False,
        UP: '',
        DOWN: 'c4',
        LEFT: 'b3',
        RIGHT: ''
     },
     'c1': {
        ZONENAME: "South Town Exit",
        DESCRIPTION: 'This is one of the two exits in this town.',
        EXAMINATION: 'This exit is definitely less welcoming than the town entrance. This exit is pretty similar to the East Exit. ',
        SOLVED: False,
        UP: 'b1',
        DOWN: 'd1',
        LEFT: '',
        RIGHT: 'c2'
     },
     'c2': {
        ZONENAME: "Your Backyard",
        DESCRIPTION: 'This is the backyard of your house.',
        EXAMINATION: 'In the very back of your backyard, you notice a small exit in the back of it.',
        SOLVED: False,
        UP: 'b2',
        DOWN: 'd2',
        LEFT: 'c1',
        RIGHT: 'c3'
     },
     'c3': {
        ZONENAME: "The Town Museum",
        DESCRIPTION: 'You enter the Town Museum, Known to hold the vast History of this town.',
        EXAMINATION: 'You notice how much history this town has as you look at all of the museum exhibits.',
        SOLVED: False,
        UP: 'b3',
        DOWN: '',
        LEFT: 'c2',
        RIGHT: 'c4'
     },
     'c4': {
        ZONENAME: "The Deep Forest",
        DESCRIPTION: 'You have traveled deeper into the deep part of the forest.',
        EXAMINATION: 'You notice how dark and quiet things are deep into this forest, it\'s pretty eerie. Suddenly a goblin attacks you out of nowhere!',
        SOLVED: False,
        UP: 'b4',
        DOWN: 'd4',
        LEFT: '',
        RIGHT: ''
     },
     'd1': {
        ZONENAME: "The Traveling Road",
        DESCRIPTION: 'You exit town only to find yourself traveling a very long traveling road.',
        EXAMINATION: 'You notice how long the road is, it will probably take you a day to travel it. ',
        SOLVED: False,
        UP: 'c1',
        DOWN: '',
        LEFT: '',
        RIGHT: 'd2'
     },
     'd2': {
        ZONENAME: "Secret Hideaway",
        DESCRIPTION: 'You enter a secret hideaway from your backyard or from the traveling road.',
        EXAMINATION: 'You notice that this secret hideaway leads to three different places, one in every direction besides down.',
        SOLVED: False,
        UP: 'c2',
        DOWN: '',
        LEFT: 'd1',
        RIGHT: 'd3'
     },
     'd3': {
        ZONENAME: "The Secret Alter",
        DESCRIPTION: 'You enter a room that has nothing but a secret alter.',
        EXAMINATION: 'You notice you can\'t go anywhere here besides from where you came.',
        SOLVED: False,
        UP: '',
        DOWN: '',
        LEFT: 'd2',
        RIGHT: ''
     },
     'd4': {
        ZONENAME: "Forest Treasure Hoard",
        DESCRIPTION: 'You find the forest\'s treasure hoard, congrats! ',
        EXAMINATION: 'You notice piles upon piles of treasure.',
        SOLVED: False,
        UP: 'c4',
        DOWN: '',
        LEFT: '',
        RIGHT: ''
     },
}

# Shop items and their prices
shop_items = {
    'sword': 50,
    'potion': 30,
    'scroll': 20
}

##### Game Interactivity #####
def print_location():
    print('\n' + ('#' * (4 + len(myPlayer.location))))
    print('# ' + zonemap[myPlayer.location][ZONENAME].upper() + ' #')  # Show ZONENAME
    print('# ' + zonemap[myPlayer.location][DESCRIPTION] + ' #')
    print('\n' + ('#' * (4 + len(myPlayer.location))))

def prompt():
    print("\n" + "===============================")
    print("What would you like to do?")
    action = input("> ")
    acceptable_actions = ['move', 'go', 'travel', 'walk', 'quit', 'examine', 'inspect', 'interact', 'look', 'inventory']  # Added 'inventory'
    if myPlayer.location == 'b1':
        acceptable_actions.append('shop')  # Add 'shop' action if player is in location 'b1'
    while action.lower() not in acceptable_actions:
        print("Unknown action, try again.\n")
        action = input("> ")

    if action.lower() == 'quit':
        sys.exit()
    elif action.lower() in ['move', 'go', 'travel', 'walk']:
        player_move(action.lower())
    elif action.lower() in ['examine', 'inspect', 'interact', 'look']:
        player_examine(action.lower())
    elif action.lower() == 'inventory':  # Added inventory prompt
        show_inventory()
    elif action.lower() == 'shop' and myPlayer.location == 'b1':
        shop()
    elif myPlayer.location == 'c4':
        combat()  # Start combat if the player is in location 'c4'


def player_move(action):
    ask = "Where would you like to move to?\n"
    dest = input(ask)
    dest = dest.lower()  # Convert the destination to lowercase for consistent handling
   
    valid_directions = ['up', 'down', 'left', 'right']
   
    if dest in valid_directions:
        destination = zonemap[myPlayer.location].get(dest.upper())  # Use dictionary get method to handle missing keys
        if destination:
            movement_handler(destination)
        else:
            print("Hey, you can't go that way!")
    else:
        print("Unknown direction!")

def movement_handler(destination):
    print("\n" + "You have moved to the " + destination + ".")
    myPlayer.location = destination
    print_location()

def player_examine(action):
    if zonemap[myPlayer.location][SOLVED]:
        print("You have already exhausted this zone.")
    else:
        print(zonemap[myPlayer.location][EXAMINATION])  # Show EXAMINATION text
        if not zonemap[myPlayer.location][SOLVED]:
            zonemap[myPlayer.location][SOLVED] = True
            if myPlayer.location == 'c4':
                combat()  # Start combat if the player is in location 'c4'
            elif myPlayer.location == 'd4':
                print("\nAs you look around, you notice something shimmering in the distance.")
                time.sleep(1)
                print("You walk towards it and find a hidden treasure hoard!")
                time.sleep(1)
                print("Congratulations, " + myPlayer.name + "! You have completed your adventure in this RPG world.")
                print("The creepy narrator from the beginning of your journey returns,")
                print("moving text appearing before your eyes:")
                print()
                print_moving_text("Well done, " + myPlayer.name + ", the " + myPlayer.job + "!")
                print_moving_text("You have navigated the twists and turns of this strange world, defeated fearsome foes,")
                print_moving_text("and uncovered hidden treasures. Your journey here is complete.")
                print_moving_text("Farewell, adventurer. May your next adventure be as thrilling as this one!")
                myPlayer.game_over = True

def print_moving_text(text):
    for char in text:
        sys.stdout.write('\033[93m' + char + '\033[0m')  # ANSI escape code for godlike light color
        sys.stdout.flush()
        time.sleep(0.05)  # Adjust the delay between characters as needed
    print()




def show_inventory():
    print("\nInventory:")
    print("Coins: ", myPlayer.coins)  # Display player's coins
    print("Items: ", myPlayer.inventory)  # Display player's inventory

# Shop function
def shop():
    print("\nWelcome to the shop!")
    print("Here are the items available for purchase:")
    for item, price in shop_items.items():
        print(f"{item.capitalize()}: {price} coins")

    purchase = input("What would you like to buy? (Type 'exit' to leave): ").lower()
    if purchase == 'exit':
        print("Thanks for visiting the shop!")
        return
    elif purchase in shop_items:
        if myPlayer.coins >= shop_items[purchase]:
            myPlayer.coins -= shop_items[purchase]
            myPlayer.inventory.append(purchase)
            print(f"You bought a {purchase}!")
        else:
            print("You don't have enough coins to buy that.")
    else:
        print("That item is not available in the shop.")

# Combat function
def combat():
    goblin_hp = 50
    player_defending = False

    while goblin_hp > 0 and myPlayer.hp > 0:
        print("\n")
        print("\033[91m" + "Goblin's turn" + "\033[0m")
        goblin_attack = random.randint(5, 10)
        if player_defending:
            goblin_attack //= 2  # Halve goblin's attack if player is defending
            print("\033[91m" + "The goblin sees you defending and lowers its attack!" + "\033[0m")
        myPlayer.hp -= goblin_attack
        print("\033[91m" + f"The goblin attacks you and deals {goblin_attack} damage!" + "\033[0m")
        print(f"You have \033[91m{myPlayer.hp} HP\033[0m left.")

        if myPlayer.hp <= 0:
            print("\033[91m" + "You died, you noob!" + "\033[0m")
            myPlayer.game_over = True
            break

        print("\n")
        print("\033[91m" + "Your turn" + "\033[0m")
        print("Choose your action:")
        print("1. Attack")
        print("2. Defend")
        action = input("> ")

        if action == '1':  # Attack
            player_damage = random.randint(10, 20)
            if 'sword' in myPlayer.inventory or 'scroll' in myPlayer.inventory:
                player_damage *= 2  # Double damage if player has sword or scroll
            goblin_hp -= player_damage
            print(f"\033[91m" + f"You attack the goblin and deal {player_damage} damage!" + "\033[0m")
            if goblin_hp <= 0:
                print("\033[91m" + "You defeated the goblin!" + "\033[0m")
                gold_reward = random.randint(1, 35)
                myPlayer.coins += gold_reward
                print(f"The goblin dropped \033[93m{gold_reward} gold coins\033[0m!")
                break
            else:
                print(f"The goblin has \033[91m{goblin_hp} HP\033[0m left.")

        elif action == '2':  # Defend
            print("You defend against the goblin's next attack.")
            player_defending = True

        else:
            print("Invalid action. You wasted your turn!")

    if myPlayer.hp <= 0:
        print("\033[91m" + "You died, you noob!" + "\033[0m")
        myPlayer.game_over = True


##### Game Functionality#####
def setup_game():
    os.system('cls' if os.name == 'nt' else 'clear')

    ### NAME COLLECTING
    question1 = "Hello there, what's your name?\n"
    for character in question1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    player_name = input("> ")
    myPlayer.name = player_name

    ### JOB HANDLING
    question2 = "Hello there, what role do you want to play?\n"
    question2added = "(You can play as a warrior, mage, or priest.)\n"
    for character in question2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in question2added:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.01)
    player_job = input("> ")
    valid_jobs = ['warrior', 'mage', 'priest']
    if player_job.lower() in valid_jobs:
        myPlayer.job = player_job
        print("You are now a " + player_job + "!\n")
    while player_job.lower() not in valid_jobs:
        player_job = input("> ")
        if player_job.lower() in valid_jobs:
            myPlayer.job = player_job
            print("You are now a " + player_job + "!\n")

    ### PLAYER STATS
    if myPlayer.job == 'warrior':
        myPlayer.hp = 120
        myPlayer.mp = 20
    elif myPlayer.job == 'mage':
        myPlayer.hp = 40
        myPlayer.mp = 120
    elif myPlayer.job == 'priest':
        myPlayer.hp = 60
        myPlayer.mp = 60

    # Introduction message with varying text speed
    intro_msg1 = "Welcome, " + myPlayer.name + " the " + myPlayer.job + ", to this weirdly bizzare text adventure!\n"
    intro_msg2 = "You find yourself in a strange town, with many mysteries to uncover.\n"
    intro_msg3 = "But beware, danger lurks around every corner...\n"
    for character in intro_msg1:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.05)
    for character in intro_msg2:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.04)
    for character in intro_msg3:
        sys.stdout.write(character)
        sys.stdout.flush()
        time.sleep(0.04)

    print_location()

def main_game_loop():
    while myPlayer.game_over is False:
        prompt()
    else:
        print("Thanks for playing!")
        sys.exit()

title_screen()
