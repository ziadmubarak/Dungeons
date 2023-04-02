#Version 1.14 - 28/10/22
from random import randint

class Player:

    def __init__(self, health):
        self.__Health = health
        self.__Location = None
        self.__Inventory = []
        self.__SpellBook = {"frostbolt": 50, "lightning": 80}

    def AddItem(self, item):
        self.__Inventory.append(item)

    def GetHealth(self):
        return self.__Health

    def SetHealth(self, health):
        self.__Health = health

    def GetLocation(self):
        return self.__Location

    def SetLocation(self, location):
        self.__Location = location
        print(self.__Location.GetDescription())

    def AdjustHealth(self, health):
        self.__Health += health
        return self.__Health

    def DoCommand(self, command):
        if command == "QUIT":
            return True
        
        instructions = command.split(' ')

        if instructions[0] == "look":
            print(self.__Location.GetDescription())
        elif instructions[0] == "health":
            print(f"you have {self.__Health} health")
        elif instructions[0] == "move" or instructions[0] == "go":
            if len(instructions) <= 1:
                print("Move where?")
            else:
                self.__Move(instructions[1])
        elif instructions[0] == "get" or instructions[0] == "take":
            self.__Inventory.append(self.__Location.RemoveItem(instructions[1]))
        elif instructions[0] == "attack":
            for creature in self.__Location.GetCreatures():
                if creature.GetName() == instructions[1]:
                    damage = randint(1,100)
                    dead = creature.TakeDamage(damage)
                    if dead:
                        print(f"Your attack killed the {creature.GetName()}")
                        self.__Location.RemoveCreature(creature)
                    else:
                        print(f"Your attack caused the {creature.GetName()} to lose {damage} health.")
                        damageTaken = creature.GetAttackDamage()
                        print(f"{creature.GetName()} attacks you and causes {damageTaken} damage.")
                        self.__Health -= damageTaken
                        if self.__Health <= 0:
                            print("You die")
                            return True
                        else:
                            return False
        elif instructions[0] == "cast":
            if len(instructions) != 3:
                print("Cast which spell at which target?")
            else:
                spell = instructions[1]
                target = instructions[2]
                if spell in self.__SpellBook.keys():
                    for creature in self.__Location.GetCreatures():
                        if creature.GetName() == target:
                            dead = creature.TakeSpellDamage(spell, self.__SpellBook[spell])
                            if dead:
                                print(f"Your {spell} killed the {creature.GetName()}")
                                self.__Location.RemoveCreature(creature)
                            else:
                                self.__Health -= creature.GetAttackDamage()
                                if self.__Health <= 0:
                                    print("You die")
                                    return True
                                else:
                                    return False
                else:
                    print("You don't know that spell!")
        elif instructions[0] == "examine":
            if len(instructions) <= 1:
                print("Examine What?")
            else:
                for i in range(len(self.__Inventory)):
                    if instructions[1] == self.__Inventory[i].GetName():
                        print(self.__Inventory[i].GetDescription())
        elif instructions[0] == "eat":
            if len(instructions) <= 1:
                print("Eat What?")
            else:
                self.__Eat(instructions[1])
        elif instructions[0] == "inventory" or instructions[0] == "i":
            items = "\n"
            if len(self.__Inventory) > 0:
                if len(self.__Inventory) == 1:
                    items += f"You have the following item: {self.__Inventory[0].GetName()}"
                else:
                    items += f"You have the following items: {self.__Inventory[0].GetName()}"
                    for i in range(1,len(self.__Inventory)-1):
                        items += ", " + self.__Inventory[i].GetName()
                    items += f" and {self.__Inventory[len(self.__Inventory)-1].GetName()}"
            else:
                items += "You aren't carrying anything"
            print(items)
        else:
            print("You can't do that")
            return False

    def __Move(self, direction):
        exits = self.__Location.GetDirections()
        directionFound = False

        for i in range(len(exits)):
            if direction == exits[i]:
                directionFound = True
                if not self.__Location.GetConnections()[i].GoThrough(self,direction):
                    print(f"You can't go {direction}")

        if not directionFound:
            print(f"There is no exit to the {direction}")

    def __Eat(self,food):
        for foodPosition in range(len(self.__Inventory)):
            if self.__Inventory[foodPosition].GetName() == food:
                self.__Health += self.__Inventory[foodPosition].GetHeals()
                self.__Inventory.pop(foodPosition)
                break
        
class Creature:
    def __init__(self, name, health):
        self.__Name = name
        self.__Health = health

    def GetAttackDamage(self):
        return randint(1,10)

    def GetHealth(self):
        return self.__Health

    def GetName(self):
        return self.__Name

    def SetHealth(self, amount):
        self.__Health = amount

    def TakeDamage(self, damage):
        self.__Health -= damage
        if self.__Health <= 0:
            return True
        else: 
            return False

    def TakeSpellDamage(self, spell, damage):
        # returns True if the creature dies, else False if it's still alive
        print(f"{self.__Name} takes {damage} from {spell}")
        return self.TakeDamage(damage)

class DragonCreature(Creature):
    def __init__(self):
        super().__init__("dragon", 100)

    def GetAttackDamage(self):
        if randint(1,2) == 1:
            print("The dragon engulfs you with his fiery breath.")
            return 9999999
        else:
            return super().GetAttackDamage()

    def TakeSpellDamage(self, spell, damage):
        if spell == "frostbolt":
            return True
        else:
            return super().TakeSpellDamage(spell, damage)

class Connection:
    def __init__(self, roomFrom, roomTo, direction):
        self.__RoomFrom = roomFrom
        self.__RoomTo = roomTo
        self.__Direction = direction

    def GoThrough(self,player, direction):
        if player.GetLocation() == self.__RoomFrom and direction == self.__Direction:
            player.SetLocation(self.__RoomTo)
            return True
        else:
            return False
    
    def GetDirection(self):
        return(self.__Direction)

class Item:
    def __init__(self, name, description):
        self._Name = name 
        self._Description = description

    def GetHeals(self):
        return 0

    def GetName(self):
        return self._Name

    def SetName(self, name):
        self._Name = name
    
    def GetDescription(self):
        return self._Description

    def SetDescrption(self, description):
        self._Desription = description

class FoodItem(Item):
    def __init__(self, name, description, heals):
        super().__init__(name, description)
        self.__HealAmount = heals

    def GetHeals(self):
        return self.__HealAmount

class Room:
    def __init__(self, description):
        self.__Description = description
        self.__Contents = []
        self.__Creatures = []
        self.__Connections = []
    
    def AddConnection(self, connection):
        self.__Connections.append(connection)

    def AddItem(self,item):
        self.__Contents.append(item)

    def AddCreature(self, creature):
        self.__Creatures.append(creature)

    def GetConnections(self):
        return self.__Connections

    def GetContents(self):
        return self.__Contents

    def GetCreatures(self):
        return self.__Creatures
        
    def GetDescription(self):
        items = "\n"
        if len(self.__Contents) > 0:
            if len(self.__Contents) == 1:
                items += f"You can see the following item: {self.__Contents[0].GetName()}"
            else:
                items += f"You can see the following items: {self.__Contents[0].GetName()}"
                for i in range(1,len(self.__Contents)-1):
                    items += ", " + self.__Contents[i].GetName()
                items += f" and {self.__Contents[len(self.__Contents)-1].GetName()}"
        else:
            items = ""

        creatures = "\n"
        if len(self.__Creatures) > 0:
            if len(self.__Creatures) == 1:
                creatures += f"You can see the following creature: {self.__Creatures[0].GetName()}"
            else:
                creatures += f"You can see the following creatures: {self.__Creatures[0].GetName()}"
                for i in range(1,len(self.__Creatures)-1):
                    creatures += ", " + self.__Creatures[i].GetName()
                creatures += f" and {self.__Creatures[len(self.__Creatures)-1].GetName()}"
        else:
            creatures = ""

        exits = "\n"
        if len(self.__Connections) > 0:
            if len(self.__Connections) == 1:
                exits += f"There is an exit to the {self.__Connections[0].GetDirection()}"
            else:
                exits += f"There are exits to the {self.__Connections[0].GetDirection()}"
                for i in range(1,len(self.__Connections)-1):
                    exits += ", " + self.__Connections[i].GetDirection()
                exits += f" and {self.__Connections[len(self.__Connections)-1].GetDirection()} "
        else:
            exits = "There are no visible exits"

        return self.__Description + creatures + items + exits

    def GetDirections(self):
        directions = []
        for connection in self.__Connections:
            directions.append(connection.GetDirection())
        return(directions)

    def RemoveCreature(self, creature):
        self.__Creatures.remove(creature)

    def RemoveItem(self, name):
        for item in self.__Contents:
            if item.GetName() == name:
                self.__Contents.remove(item)
                return item
        return None

    def SetDescription(self, description):
        self.__Description = description

class Game:
    def PlayGame(self):
        command = ""
        gameOver = False

        # initialising the game
        print("Welcome Message...")
        startRoom = Room("You are in the starting cave.")
        lavaRoom = Room("You are in a dark cave with a glowing river of lava.")
        apple = FoodItem("apple", "a beautiful green apple, it looks delicious.", 10)
        redApple = FoodItem("apple", "a beautiful rosy red apple, it looks delicious.", 10)
        stoneApple = Item("apple", "a beautiful apple made of stone.")
        water = Item("water", "Everian, the best!.")
        glass = Item("glass", "glassy glass.")
        dragon = DragonCreature()

        startRoom.AddConnection(Connection(startRoom, lavaRoom, "north"))
        lavaRoom.AddConnection(Connection(lavaRoom, startRoom, "south"))
        startRoom.AddItem(apple)
        startRoom.AddItem(glass)
        lavaRoom.AddCreature(dragon)

        pc = Player(STARTING_HEALTH)
        pc.SetLocation(startRoom)
        pc.AddItem(redApple)
        pc.AddItem(stoneApple)

        while not gameOver:
            command = input("What would you like to do? ")
            gameOver = pc.DoCommand(command)

        print("Thank you for playing Dungeon! See you again soon, brave dungeoneer.")

########### MAIN PROGRAM ###########

STARTING_HEALTH = 100
dungeon = Game()
dungeon.PlayGame()
