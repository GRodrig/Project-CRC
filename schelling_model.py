import numpy as np
import random

class Schelling:

    def __init__(self, width , height, empty_ratio, similarity_threshold, neighbour_depth, races_ratio: list = [0.30,0.30]):

        self.model_config(width , height, empty_ratio, similarity_threshold, neighbour_depth, races_ratio)



    def model_config(self, width , height, empty_ratio, similarity_threshold, neighbour_depth, races_ratio):
        self.height = height
        self.width = width
        self.empty_ratio = empty_ratio
        self.similarity_threshold = similarity_threshold
        self.neighbour_depth = neighbour_depth
        self.no_one_is_sad = False
        self.nr_races = len(races_ratio)

        ratios = races_ratio.copy()

        self.final_ratios = ratios
        
        self.final_ratios= [empty_ratio] + self.final_ratios

        self.model_size = self.width * self.height

        array_races = [i for i in range(len(self.final_ratios))]

        # Populate the model
        self.community = np.random.choice(array_races, size=self.model_size, p=self.final_ratios)
        # Reshape 1D array to 2D
        self.community = np.reshape(self.community, (int(self.width), int(self.height)))

    


    def road_to_happiness(self):
        number_unhappy = 0
        for (width, height), race in np.ndenumerate(self.community):
            if not self.is_empty(race=race):
                if not self.is_happy(width, height):
                    number_unhappy += 1
                    self.move_to_empty_space(width, height)   

        if number_unhappy == 0:
            self.no_one_is_sad=True   


    def get_mean_similarity_ratio(self):
        total_elem_race = 0
        similarity_ratio = 0
        for (w, h), race in np.ndenumerate(self.community):
            if not self.is_empty(race=race):
                neighborhood = self.get_neighbourhood(w, h)
                neighborhood_size = np.size(neighborhood) -1
                nr_empty_neighbors = np.count_nonzero(neighborhood == 0)
                if neighborhood_size != nr_empty_neighbors: # If there is neighbours
                    n_similar = np.count_nonzero(neighborhood == self.get_race(w ,h)) - 1
                    similarity_ratio += n_similar / (neighborhood_size - nr_empty_neighbors)
                    total_elem_race += 1
        return similarity_ratio / total_elem_race if total_elem_race > 0 else 0


    def get_neighbourhood(self, w ,h ):
        x_min = w - self.neighbour_depth if w - self.neighbour_depth > 0 else 0
        x_max = w + self.neighbour_depth + 1 if w + self.neighbour_depth < self.width else self.width
        y_min = h - self.neighbour_depth if h - self.neighbour_depth > 0 else 0
        y_max = h + self.neighbour_depth + 1 if h + self.neighbour_depth < self.height else self.height
        neighbourhood = self.community[x_min:x_max  , y_min:y_max]
        return neighbourhood


    def is_happy(self, w , h ):
        neighbourhood = self.get_neighbourhood(w ,h)
        nr_elemts_race = np.count_nonzero(neighbourhood == self.get_race(w ,h)) - 1
        nr_elemts_race = nr_elemts_race if nr_elemts_race > 0 else 0
        nr_no_neighbour = np.count_nonzero(neighbourhood == 0) 
        nr_neighbours = np.size(neighbourhood) - nr_no_neighbour  - 1

        if nr_neighbours == 0:
            return True
            
        happiness = nr_elemts_race/nr_neighbours
        if happiness < self.similarity_threshold:
            return False
        return True

    def move_to_empty_space(self, width, height):
        current_race = self.get_race(width, height)
        empty_pos_list = []
        for (w, h), race in np.ndenumerate(self.community):
            if self.is_empty(race=race):
                empty_pos_list.append((w,h))
        random_empty = random.choice(empty_pos_list)
        self.community[random_empty] = current_race
        self.community[width,height] = 0

    def get_race(self, width, height):
        return self.community[width, height]

    def is_empty(self, width: int = -1, height: int = -1, race: int = -1):
        return self.community[width, height] == 0 if race == -1 else race ==0


if __name__ == "__main__":
    schelling = Schelling(5, 5, 0.40, 0.60, 1, [0.3, 0.3])
    for i in range(50):
        schelling.road_to_happiness()
        if schelling.no_one_is_sad:
            print(f"Everyone is happy at iteration {i}")
            break
    print("Community")
    print(schelling.community)
    
