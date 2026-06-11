# Prior art — published TSP heuristic families (novelty boundary for `idea`)

A cell = (search paradigm, move/operator family). No emitted cell may share
BOTH axes with an entry here. Single-axis overlap is allowed.

| search paradigm | move/operator family | canonical reference |
|---|---|---|
| greedy construction | nearest neighbor / cheapest insertion | Rosenkrantz et al. (1977) |
| local search | 2-opt | Croes (1958) |
| local search | 3-opt / Or-opt | Lin (1965), Or (1976) |
| local search | Lin–Kernighan variable-depth | Lin & Kernighan (1973) |
| chained/iterated local search | LK + double-bridge kicks | Martin, Otto & Felten (1991); LKH, Helsgaun (2000) |
| simulated annealing | 2-opt neighborhood | Kirkpatrick et al. (1983) |
| tabu search | 2-opt/city-swap with tabu list | Glover (1989) |
| genetic algorithm | EAX edge-assembly crossover | Nagata & Kobayashi (1997, 2013) |
| ant colony optimization | pheromone-guided construction | Dorigo & Gambardella (1997) |
| guided local search | penalty-augmented 2-opt | Voudouris & Tsang (1999) |
| greedy construction | Christofides (MST + matching) | Christofides (1976) |
| neural construction (out of scope: needs GPU training) | pointer/attention decoders | Vinyals et al. (2015), Kool et al. (2019) |
