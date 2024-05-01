# -------------------------------------------------------------------------------------
# Welcome to the Ant Roleplay Game!
#
# In this game, players control anthills as if they were nations and can take
# numerous actions and choices to boost their nation and conquer (or be conquered by)
# other player's or NPC's anthills.
#
# Here, we store the player's anthill data with databases and modify it with 
# data structure and oriented objects.
# -------------------------------------------------------------------------------------

import mysql.connector
from prettytable import PrettyTable

queens = []

def merge_sort(arr):
    if len(arr) > 1:
        half = len(arr)//2
        left = arr[:half]
        right = arr[half:]

        merge_sort(left)
        merge_sort(right)

        i = j = k = 0

        while i < len(left) and j < len(right):
            if left[i] < right[j]:
                arr[k] = left[i]
                i += 1
            
            else:
                arr[k] = right[j]
                j += 1
                
            k += 1

        while i < len(left):
            arr[k] = left[i]
            i += 1
            k += 1

        while j < len(right):
            arr[k] = right[j]
            j += 1
            k += 1

    return arr

def pass_turn():
    for queen in queens:
        queen.food -= queen.pop * 0.1
        for anthill in queen.anthills:
            queen.pop += anthill.pop_growth
            queen.food -= anthill.food_cost

            if anthill.level > 0:
                queen.feces += 1

            elif anthill.level > 1:
                queen.feces += 2

class antqueen:
    def __init__(self, dynasty, anthills, pop, oper_pop, mil_pop, food, feces):
        self.__dynasty = dynasty
        self.anthills = anthills
        self.pop = pop
        self.oper_pop = oper_pop
        self.mil_pop = mil_pop
        self.food = food
        self.feces = feces
    
    def add_anthill(self, name):
        hill = anthill(self.__dynasty, name)
        self.anthills.append(hill)
        return
    
    def set_pop(self, pop, qtty):
        if pop == 0:
            if qtty > 0:
                self.pop += qtty
                self.oper_pop += qtty
            
            else:
                print("Quantity given less than 1.")
        
        elif pop == 1:
            if qtty > 0:
                self.pop += qtty
                self.mil_pop += qtty
            
            else:
                print("Quantity given less than 1.")
        
        else:
            print("Type of pop non-existent")
        
        return
    
    def set_food(self, food):
        self.food += food
        return
    
    def set_feces(self, feces):
        self.feces += feces
        return

class anthill:
    def __init__(self, queen, name, level, pop_growth, pop_cap, storage, food_cost):
        self.__queen = queen
        self.__name = name
        self.level = level,
        self.buildings = []
        self.pop_growth = pop_growth
        self.pop_cap = pop_cap
        self.storage = storage
        self.food_cost = food_cost

    def level_up(self, level):
        if self.level >= 0 and self.level < 4:
            self.level = level
        
        else:
            print("Level non-existent.")

    def add_build(self, type):
        if self.level < 2:
            print("Can't construct building - not colony or anthill.")
        
        elif self.level > 2:
            if type > 0 and type < 6:
                self.buildings.append(type)
            
            else:
                print("Type of building non-existent.")

        else:
            if type == 1 and type == 2:
                self.buildings.append(type)
            else:
                print("Can only construct nests and shelters in colony.")
    
    def update(self):
        if self.level == 0:
            self.food_cost = -1
        
        elif self.level > 0:
            self.food_cost = self.level ** 2
        
        for i in range(1, 6):
            builds = self.buildings.count(i)

            if i == 1:
                self.pop_growth = builds * 1
                self.food_cost -= builds * 1
            
            elif i == 2:
                self.pop_cap = builds * 10
                self.food_cost -= builds * 1
            
            elif i == 3:
                self.storage = builds * 10
                self.food_cost -= builds * 1
            
            elif i == 4:
                self.food_cost -= builds * 1

            elif i == 5:
                self.food_cost -= builds * 4

db = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'root',
    database = 'antrpg'
)

cursor = db.cursor()

while True:
    print("--------------------")
    print("ANTHILL RPG TERMINAL")
    print("--------------------")
    print()
    print("This terminal allows you to modify and visualize the game's database of anthills.")
    print("Create or access an antqueen table? [c/a]")

    option = str(input())
    
    print()
    if option == 'c':
        print("Name of the dynasty:")
        dyn = str(input())

        cursor.execute(f"""
        INSERT INTO antqueens (dynasty, pop, oper_pop, mil_pop, food, feces)
        VALUES ('{dyn}', 0, 0, 0, 0, 0);
        """)

        queen_id = cursor.lastrowid
        db.commit()

        print()
        print("Name of the capital anthill:")
        hill_name = str(input())

        cursor.execute(f"""
        INSERT INTO anthills (queen_id, name, level, pop_growth, pop_cap, storage, food_cost)
        VALUES ({queen_id}, '{hill_name}', 0, 0, 0, 0, 0);
        """)
        
        db.commit()

    elif option == 'a':
        cursor.execute("SELECT dynasty FROM antqueens;")
        queens = cursor.fetchall()

        if queens:
            print("Dynasties in the database:")

            for dynasties in queens:
                print(dynasties[0])

            print()
            print("Which dynasty to access?")
            search = str(input())
            cursor.execute(f"SELECT * FROM antqueens WHERE dynasty = '{search}';")
            result_queen = cursor.fetchone()

            if result_queen:
                columns = cursor.column_names
                table = PrettyTable(columns)
                table.add_row(result_queen)
                print()
                print(table)
                print()
                
                cursor.execute(f"SELECT * FROM anthills WHERE queen_id = {result_queen[0]};")
                result_hill = cursor.fetchall()
                
                if result_hill:
                    print(f"{search} dynasty anthills:")

                    for i in result_hill:
                        hill = i[2]
                        print(hill)
                    
                else:
                    print("This dynasty doesn't have anthills")

                print()
                print("Alter queen or a hill table? [q/h]")
                option = str(input())

                if option == 'q':
                    queen = antqueen(
                            result_queen[1],
                            result_hill,
                            result_queen[2],
                            result_queen[3],
                            result_queen[4],
                            result_queen[5],
                            result_queen[6]
                            )
                    
                    while True:
                        print()
                        print("---------------")
                        print("1- Add anthill")
                        print("2- Set pops")
                        print("3- Set food")
                        print("4- Set feces")
                        print("5- Leave table")
                        print("---------------")
                        print()

                        print("Which option?")
                        option = int(input())

                        if option == 1:
                            print("New anthill name:")
                            hill_name = str(input())
                            queen.add_anthill(hill_name)
                            cursor.execute(f"""
                            INSERT INTO anthills (queen_id, name, level, pop_growth, pop_cap, storage, food_cost)
                            VALUES ({result_queen[0]}, '{hill_name}', 0, 0, 0, 0, 0)
                            """)

                        elif option == 2:
                            print("Operary [0] or soldier [1]?")
                            pop = int(input())
                            print("How many?")
                            qtty = int(input())
                            queen.set_pop(pop, qtty)
                        
                        elif option == 3:
                            print("How many?")
                            qtty = int(input())
                            queen.set_food(qtty)
                        
                        elif option == 4:
                            print("How many?")
                            qtty = int(input())
                            queen.set_feces(qtty)
                        
                        elif option == 5:
                            print(queen.pop)
                            print("Commit alterations? [y/n]")
                            commit = str(input())

                            if commit == 'y':
                                cursor.execute(f"""
                                UPDATE antqueens
                                SET pop = {queen.pop},
                                oper_pop = {queen.oper_pop},
                                mil_pop = {queen.mil_pop},
                                food = {queen.food},
                                feces = {queen.feces}
                                WHERE id = {result_queen[0]};
                                """)
                                db.commit()
                                break

                            else:
                                del queen
                                break

                        else:
                            print("Option doesn't exists")
                
                elif option == 'h':
                    print("Which hill?")
                    search = str(input())
                    cursor.execute(f"SELECT * FROM anthills WHERE name = '{search}'")
                    res_hill = cursor.fetchone()

                    hill = anthill({result_queen[0]},
                                   {search},
                                   res_hill[3],
                                   res_hill[4],
                                   res_hill[5],
                                   res_hill[6],
                                   res_hill[7]
                                   )
                    
            else:
                print("Table not found")

        else:
            print("No dynasties found.")