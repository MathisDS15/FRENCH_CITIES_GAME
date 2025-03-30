# DA SILVA Mathis

# Cities Game

import tkinter as tk
import random as rd


class City:
    def __init__(self, name, lat, lon):
        self.name, self.lat, self.lon = name, lat, lon

    def __str__(self):
        return f"{self.name}, {self.lon:.3f}, {self.lat:.3f}"


def import_cities(file):
    """Reads the file and returns a list of cities."""
    cities = []
    with open(file, encoding='utf_8') as f:
        for line in f:
            name = line[:30].strip()
            lat = float(line[30:38])
            lon = float(line[54:65])
            cities.append(City(name, lat, lon))
    return cities


class Application:
    def __init__(self, file_name):
        # Create the application window with a canvas
        self.wnd = tk.Tk()
        self.wnd.title("Cities Game")
        self.wnd.geometry("-5+5")
        self.cnv = tk.Canvas(self.wnd, bg='light green')
        self.cnv.pack()
        self.v_game = tk.Label(self.wnd, text="", padx=10, pady=10)
        self.v_game.pack(side="top", fill="both")
        self.button_quit = tk.Button(self.wnd, text='Quit', padx=5,
                                     pady=5, command=self.wnd.destroy)
        self.button_quit.pack(side='bottom')
        self.button_start = tk.Button(self.wnd, text='Start Game',
                                      padx=5, pady=5, command=self.start_game)
        self.button_start.pack(side='bottom')

        # Click handler
        self.cnv.bind('<Button-1>', self.city_zone)

        # Display parameters
        self.ppdh = 55   # Pixels per degree of longitude (horizontal)
        self.ppdv = 70   # Pixels per degree of latitude (vertical)
        self.margin = 20  # Margin around the map in the canvas
        self.size = 7     # Size of the square representing a city

        # Load and display cities
        self.cities = import_cities(file_name)
        self.adjust_display()
        self.display_cities()

        # Game variables
        self.target_city = None
        self.correct_answers = 0
        self.wrong_answers = 0
        self.score = 0
        self.button_start.config(state=tk.NORMAL)

        # Display the window
        self.wnd.mainloop()

    def adjust_display(self):
        """Adjust the canvas size based on the cities' coordinates."""
        self.north = max(c.lat for c in self.cities)
        self.east = max(c.lon for c in self.cities)
        self.south = min(c.lat for c in self.cities)
        self.west = min(c.lon for c in self.cities)
        width = (self.east - self.west) * self.ppdh + 2 * self.margin
        height = (self.north - self.south) * self.ppdv + 2 * self.margin
        self.cnv.config(width=width, height=height)

    def display_cities(self):
        """Display all cities as red squares on the canvas."""
        d = self.size / 2
        for c in self.cities:
            c.x = int((c.lon - self.west) * self.ppdh + self.margin)
            c.y = int((self.north - c.lat) * self.ppdv + self.margin)
            c.id = self.cnv.create_rectangle(c.x - d, c.y - d, c.x + d, c.y + d,
                                             fill='red', outline='black')

    def start_game(self):
        """Start a new game by selecting a random city."""
        city_index = rd.randint(0, len(self.cities) - 1)
        self.target_city = self.cities[city_index]
        self.display_message(f"Find the city: {self.target_city.name}")
        self.button_start.config(state=tk.DISABLED)

    def city_zone(self, event):
        """Handle a click on the canvas and check if the correct city was clicked."""
        x, y = event.x, event.y
        clicked_city = self.find_city(x, y)

        if clicked_city == self.target_city:
            self.correct_answers += 1
            self.score = self.correct_answers - self.wrong_answers
            message = (f"Correct! You earn 1 point. " +
                       f"Your score is: {self.score}.")
            self.reset_game()
        else:
            self.wrong_answers += 1
            self.score = self.correct_answers - self.wrong_answers
            message = (f"Wrong! The correct city was " +
                       f"{self.target_city.name}. " +
                       f"You lose 1 point. Your score is: {self.score}.")
            self.reset_game()

        self.display_message(message)

    def display_message(self, message):
        """Display a message in the label."""
        self.v_game.config(text=message)

    def reset_game(self):
        """Reset the game state to allow starting a new game."""
        self.button_start.config(state=tk.NORMAL)
        self.target_city = None

    def find_city(self, x, y):
        """Find the city corresponding to the clicked coordinates."""
        for c in self.cities:
            if (c.x - self.size / 2 < x < c.x + self.size / 2 and
                c.y - self.size / 2 < y < c.y + self.size / 2):
                return c
        return None


# Run the application with the provided file
app = Application("french_cities.txt")
