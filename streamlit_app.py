from schelling_model import *
import streamlit as st

import matplotlib.pyplot as plt
from matplotlib.colors import ListedColormap


st.title("Schelling's Model of Segregation")

ratio_x, ratio_y, ratio_w, ratio_z = -1, -1, -1, -1
load=True

nr_races = st.sidebar.number_input("Number of Races", 2, 4, 2)

population = st.sidebar.slider("Population size", 3, 50, 10)

similarity_threshold = st.sidebar.slider("Similarity Threshold", 0.0, 1.0, 0.65)

neighbour_depth = st.sidebar.number_input("Neighbour Depth", 1, 5, 1)

n_iterations = st.sidebar.number_input("Number of Iterations", 10, 500, 20)

empty_ratio = st.sidebar.slider("Empty Slots Ratio", 0.1, 0.9, 0.5)

equi_ratios = (1.0-empty_ratio) / nr_races

ratio_x = st.sidebar.slider("Race X ratio", 0.0, 1.0, equi_ratios)

ratio_y = st.sidebar.slider("Race Y ratio", 0.0, 1.0, equi_ratios)

races_ratio= [ratio_x, ratio_y]

if nr_races >= 3:
    ratio_w = st.sidebar.slider("Race W ratio", 0.0, 1.0, equi_ratios)
    races_ratio.append(ratio_w)

if nr_races == 4:
    ratio_z = st.sidebar.slider("Race Z ratio", 0.0, 1.0, equi_ratios)
    races_ratio.append(ratio_z)

races_ratio = races_ratio[:nr_races]

if sum(races_ratio) + empty_ratio != 1.0:
    st.sidebar.error('Ratios do not sum up to 1')
    load=False


@st.cache(allow_output_mutation=True, max_entries=1, suppress_st_warning=True,)
def getSchelling(population_w, population_h, empty_ratio, similarity_threshold, neighbour_depth, races_ratio):
    return Schelling(population_w, population_h, empty_ratio, similarity_threshold, neighbour_depth, races_ratio)

if load:
    schelling = getSchelling(population, population, empty_ratio, similarity_threshold, neighbour_depth, races_ratio)

    mean_similarity_ratio = []
    mean_similarity_ratio.append(schelling.get_mean_similarity_ratio())

    #Plot the graphs at initial stage
    plt.style.use("ggplot")
    plt.figure(figsize=(8, 4))

    # Left hand side graph with Schelling simulation plot
    cmap = ListedColormap(['white', 'gold', 'limegreen','purple', 'red'])
    plt.subplot(121)
    plt.axis('off')
    plt.pcolor(np.flipud(schelling.community), cmap=cmap, edgecolors='w', linewidths=1)

    # Right hand side graph with Mean Similarity Ratio graph
    plt.subplot(122)
    plt.xlabel("Iterations")
    plt.xlim([0, n_iterations])
    plt.ylim([0, 1.1])
    plt.title("Mean Similarity Ratio", fontsize=15)
    plt.text(0.90, 1.06, "Similarity Ratio: %.4f" % schelling.get_mean_similarity_ratio(), fontsize=8)
    plt.text(0.90, 1.02, "Iteration Index: %.0f" % 0, fontsize=8)


    community_plot = st.pyplot(plt)
    progress_bar = st.progress(0)

    if st.sidebar.button('Run Simulation', key="run"):

        for i in range(n_iterations):
            schelling.road_to_happiness()
            mean_similarity_ratio.append(schelling.get_mean_similarity_ratio())
            plt.figure(figsize=(8, 4))

            plt.subplot(121)
            plt.axis('off')
            plt.pcolor(np.flipud(schelling.community), cmap=cmap, edgecolors='w', linewidths=1)

            plt.subplot(122)
            plt.xlabel("Iterations")
            plt.xlim([0, n_iterations])
            plt.ylim([0.0, 1.1])
            plt.title("Mean Similarity Ratio", fontsize=15)
            plt.plot(range(0, len(mean_similarity_ratio)), mean_similarity_ratio)
            plt.text(0.90, 1.06, "Similarity Ratio: %.4f" % schelling.get_mean_similarity_ratio(), fontsize=8)
            plt.text(0.90, 1.02, "Iteration Index: %.0f" % (i + 1), fontsize=8)
            
            community_plot.pyplot(plt)
            plt.close("all")
            progress_bar.progress((i+1.)/n_iterations)
            if schelling.no_one_is_sad:
                progress_bar.progress(100)
                break
        st.legacy_caching.clear_cache()

