from time import sleep
from random import randint, uniform

#  #  TODO
# Implement seagulls, then clouds(up down+bidirectional, a flapping \/) 
# Think of some new boat designs
# Add a start animation
# Cooler looking finish line

class Boat:
    """
    A boat.

    Constants
    ---------
    DEFAULT_IMG: list<list<str>>
        Default boat image.

    ROW_MULT_GENERATOR: func
        Function to generate row multiplier.
        
    ROW_MULT_RANGE: pair
        Range for random row multiplier.

    Parameters
    ----------
    name: str
        Name of boat.

    num_rowers: int
        Number of rowers on boat.

    img: list<list<str>>, default=DEFAULT_IMG
        The boat image.

    distance: int, default=0
        Distance the boat starts out.
    """
    
    total_boats = 0

    DEFAULT_IMG = [[' ', '<', ' '],
                   [' ', '|', ' '],
                   ['<', '_', '>']]

    ROW_MULT_GENERATOR = uniform
    
    ROW_MULT_RANGE = (.4, 1)

    def __init__(self, name, num_rowers, img=None, distance=0):
        self.name = name
        
        self.num_rowers = num_rowers

        self._img = img if img else Boat.DEFAULT_IMG

        self.distance = distance
        
        self.add_boat_count()

    @classmethod
    def add_boat_count(cls):
        cls.total_boats += 1

    @property
    def img(self):
        """
        Returns an inverted copy of img
        """
        return self._img[::-1]
    
    def row(self):
        """
        Moves the boat by the number of rowers * a multiplier
        """
        self.distance += self.num_rowers * Boat.ROW_MULT_GENERATOR(*Boat.ROW_MULT_RANGE)


class Race:
    """
    A boat race.

    Constants
    ---------
    BUFFER_LINES: int
        Number of blank lines in each display.

    DISPLAY_LEN: int
        Length in characters of the display.

    FILLERS: list<char>
        Characters to go at bottom of display, rightmost item goes to bottom.

    FINISH_LINE: list<char>
        Image of finish line.
        
    REFRESH_DELAY: number
        Delay between display updates.

    Parameters
    ----------
    name: str
        Name of race.

    boats: list<Boat>
        Boats to race.

    race_distance: int
        Distance boat needs to achieve to win race.
    """
    
    BUFFER_LINES = 20
    
    DISPLAY_LEN = 80

    FILLERS = ['.'] 
    
    FINISH_LINE = ['', '!', '.']

    REFRESH_DELAY = .2

    # SEAGULL_ROWS = 6
    
    # SEAGULL_SPAWN_RATE = .2

    # SEAGULL_SPRITE = '~'
    
    def __init__(self, name, boats, race_distance):
        self.name = name
        
        self.boats = boats
        
        self.race_distance = race_distance

        fillers = [' ' for _ in range(Race.BUFFER_LINES)] + Race.FILLERS[::-1]
        self._display_base = [list(filler * Race.DISPLAY_LEN + "\n") for filler in fillers]

        # self._display_base[0] = list(' ' * Race.DISPLAY_LEN + "\n")[:-1] + ['~']   # For testing seagulls

        self.race()
        
    def race(self):
        """
        Executes race.
        """
        
        print(f"Total boats entered: {Boat.total_boats}")
        print("Beggining race!")
        
        while not self.winner:
            for boat in self.boats:
                boat.row()

            self.show_boats()
            sleep(Race.REFRESH_DELAY)

        print(f"The {' and the '.join(self.winner)} win{'s' if len(self.winner) == 1 else ''} {self.name.title()}!")
        
    @property
    def display_base(self):
        """
        Returns a kind of deep copy of display base.
        """
        return [l.copy() for l in self._display_base]
    
    @property
    def winner(self):
        """
        Returns a list of boats with distance greater than win distance.
        """
        return [boat.name for boat in self.boats if boat.distance > self.race_distance]

    def move_seagull(self):
        """
        May get used one day
        """
        
        for i, row in enumerate(self._display_base):
            # Might be more efficient to just search each w/out if
            if Race.SEAGULL_SPRITE in row:
                for j, value in enumerate(row):
                    if row[j] == Race.SEAGULL_SPRITE:
                        row[j] = ' '

                        d_h = j - 1
                        if d_h > 0:
                            row[d_h] = Race.SEAGULL_SPRITE
                
    def show_boats(self):
        """
        Creates and renders a display frame.
        """
        display = self.display_base
      
        for boat in self.boats:
            pos = max(len(boat.img[-1]), int(boat.distance * Race.DISPLAY_LEN // self.race_distance))

            for i, row in enumerate(boat.img):
                
                for j, piece in enumerate(row):
                    offset = j - len(boat.img)

                    height = pos + offset
                    
                    if height < Race.DISPLAY_LEN:
                        display[-i - 1][height] = piece

        for i, item in enumerate(Race.FINISH_LINE[::-1]):
            display[-i - 1].insert(-1, item)
            
        print(''.join([''.join(row) for row in display]))


def get_rand(values, exclusive=True):
    """
    Returns a random value from list

    Parameters
    ----------
    values: list
        List to pick a value from.

    exclusive: bool, default=True
        To purge or not to purge item picked from list.
    """ 
    if not values:
        return None

    output = values[randint(1, len(values)) - 1]

    if exclusive:
        values.remove(output)
                    
    return output


def get_boat_list(count, names, rowers, imgs):
    """
    Generates a random group of boats.

    Parameters
    ----------
    count: int
        Number of boats to create.

    names: list<str>
        Possible boat names.

    rowers: lost<int>
        Possible numbers of rowers.

    imgs: list<boat images>
        Possible boat images.

    Returns
    -------
    List of boats.
    """
    return [Boat(get_rand(names), get_rand(rowers, exclusive=False), get_rand(imgs)) for _ in range(boat_count)]

    
if __name__ == '__main__':
    boat_count = 3

    race_distance = 160
    
    race_names = ["The Annual Game", "The Generic Race"]
    
    names = ['Mayflower', 'Codfather', 'Hooker']
    rowers = [i for i in range(6, 9)]
    imgs = [
            [[' ', '<', ' '],
             [' ', '|', ' '],
             ['<', '_', '>']]
            ]
    
    boats_to_race = get_boat_list(boat_count, names, rowers, imgs)

    generic_race = Race(get_rand(race_names), boats_to_race, race_distance)

    
