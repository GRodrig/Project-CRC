# CRC Project
Project - Schelling's Model of Segregation

**Use our app and try to create a multiracial community fully happy!** 🌎

<ins> Website: https://share.streamlit.io/grodrig/schelling_model_segregation </ins>

---

## Group 11
- 102181, Guilherme Rodrigues
- 98797, Tiago Silva

---

## Overview

* `schelling_model.py` - Python file that contains a simple Schelling model
* `streamlit_app.py` - Python file to load/generate a "user-friendly" interface where its possible to define every variable and see live the model changing as well as the "Mean Similarity Ratio" graph
---

## Installation and execution

1. Clone this repository

```bash
    git clone https://github.com/GRodrig/schelling_model_segregation.git
```

2. Open a terminal and install the requirements

```bash
    pip install -r requirements.txt
```

3. Run the Schelling Segregation Model Simulation (Visual Interface)

```bash
    streamlit run .\streamlit_app.py
```

3. Run the Schelling Segregation Model Simulation (Terminal)

```bash
    python3 .\schelling_model.py
```

---


## Code Overview

This method runs the Schelling simulation for one iteration. For each agent in the community, we check if the agent is happy. If the agent isnot happy, it will be moved to an empty slot.

```python
    def road_to_happiness(self):
        number_unhappy = 0
        for (width, height), race in np.ndenumerate(self.community):
            if not self.is_empty(race=race):
                if not self.is_happy(width, height):
                    number_unhappy += 1
                    self.move_to_empty_space(width, height)   

        if number_unhappy == 0:
            self.no_one_is_sad=True
```

This method returns the agent neighbourhood based on the neighbour_depth, including himself.

```python
    def get_neighbourhood(self, w ,h ):
        x_min = w - self.neighbour_depth if w - self.neighbour_depth > 0 else 0
        x_max = w + self.neighbour_depth + 1 if w + self.neighbour_depth < self.width else self.width
        y_min = h - self.neighbour_depth if h - self.neighbour_depth > 0 else 0
        y_max = h + self.neighbour_depth + 1 if h + self.neighbour_depth < self.height else self.height
        neighbourhood = self.community[x_min:x_max  , y_min:y_max]
        return neighbourhood
```

The is_happy method checks the ratio of neighbors of similar race, and returns True if the ratio is above the similarity threshold, otherwise it returns False

```python
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
```

This method moves the agent at (width, height) to an empty slot.

```python
    def move_to_empty_space(self, width, height):
        current_race = self.get_race(width, height)
        empty_pos_list = []
        for (w, h), race in np.ndenumerate(self.community):
            if self.is_empty(race=race):
                empty_pos_list.append((w,h))
        random_empty = random.choice(empty_pos_list)
        self.community[random_empty] = current_race
        self.community[width,height] = 0
```

This method computes the average similarity ratio of the entire community. Its used to draw the graph.

```python
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

```

---

### Images

Visual Interface

![Visual Example](https://github.com/GRodrig/schelling_model_segregation/blob/master/imgs/interface.png "Visual Interface")

Example of a Run

![Run example](https://github.com/GRodrig/schelling_model_segregation/blob/master/imgs/example_run.png "Example of a Run")

**Parameters:**

- **Number of Race**: number of races ranged from 1 to 4;
- **Population Size**: number of rows or columns. it will be a square grid (rows * columns) in the board;
- **Similarity Threshold**: number between 0.0 and 1.0; this number defines how easily is to make the community the happy 
- **Neighbourhood Depth**: neighbourhood radius of each individual ranged from 1 to 5;
- **Number of Iterations**: number of iterations ranged from 10 to 500;
- **Empty Slots Ratio**: number between 0.1 and 0.9 that defines the empty spaces' ratio;
- **Races Ratios (X-Z)**: number between 0.0 and 1.0 that defines the races' ratios;

The **Run Simulation** button starts the simulation, and runs for the number of iterations or until the community is fully happy;

---

## Dependencies
Main Dependencies:
- Streamlit
- Numpy
- Matplotlib

---


### References

- McCown, F. Schelling’s Model of Segregation. 2014 [Link] (https://nifty.stanford.edu/2014/mccown-schelling-model-segregation/)
- Yamashita A., Gomez C., Dombroski K Segregation, exclusion and LGBT people in disaster
impacted areas: experiences from the Higashinihon Dai-Shinsai (Great East-Japan Disaster)
2017 A Journal of Feminist Geography Volume 24, 2017 - Issue 1: Sexual and Gender Minorities and Disasters DOI: 10.1080/0966369X.2016.1276887 [Link](https://www.tandfonline.com/doi/abs/10.1080/0966369X.2016.1276887)
- Liu T. Y. The Schelling Model of Segregation: Static and Dynamic Equilibrium 23-28 Marc¸o
2021 [Link] (https://ytliu0.github.io/schelling/)
- Moujahid A. An Introduction to Agent-based Models: Simulating Segregation with Python. 2014 [Link] (https://adilmoujahid.com/posts/2014/09/schelling-model/)
- Moujahid A. An Introduction to Agent-based Models: Simulating Segregation with Python. 2020 [Link] (https://adilmoujahid.com/posts/2020/05/streamlit-python-schelling/)
- McCown, F. Schelling’s Model of Segregation. 2014 [Link] (https://nifty.stanford.edu/2014/mccown-schelling-model-segregation/)
- Hart, V. and N. Case. [Parable of the polygons](https://ncase.me/polygons/)
