import random
import matplotlib.pyplot as plt


class TourActivity:
    def __init__(self, name, type, cost):
        self.name = name
        self.type = type
        self.cost = cost

ACTIVITIES = [
    TourActivity('Boulevard City', 'Exciting', 450),
    TourActivity('Boulevard World', 'Exciting', 550),
    TourActivity('Winter Wonder land', 'Exciting', 300),
    TourActivity('Middle Beast', 'Exciting', 350),
    TourActivity('Riyadh Front', 'Shopping & Resturants', 500),
    TourActivity('U Walk', 'Shopping & Resturants', 400),
    TourActivity('The Zone', 'Shopping & Resturants', 350),
    TourActivity('The Park Avenue', 'Shopping & Resturants', 600),
    TourActivity('Albujairi', 'Shopping & Resturants', 700),
    TourActivity('River Walk', 'Shopping & Resturants', 400),
    TourActivity('Granada Mall', 'Shopping & Resturants', 350),
    TourActivity('Centria Mall', 'Shopping & Resturants', 900),
    TourActivity('Al Maigliah', 'Shopping & Resturants', 200),
    TourActivity('Riyadh Park', 'Shopping & Resturants', 550),
    TourActivity('Al Nakheel Mall', 'Shopping & Resturants', 450),
    TourActivity('The Kingdom mall', 'Shopping & Resturants', 500),
    TourActivity('Sky Bridge', 'Exciting', 70),
    TourActivity('Rawdat Tinhat', 'Nature', 50),
    TourActivity('Camp Daliah', 'Nature', 750),
    TourActivity('Horseback Safari', 'Nature', 200),
    TourActivity('Hiking', 'Nature', 300),
    TourActivity('Red Sands Trip', 'Nature', 200),
    TourActivity('King Khaled Royal Reserve', 'Nature', 350),
    TourActivity('Edge of the World', 'Nature', 300),
    TourActivity('Nofa Wild Life Park', 'Nature', 100),
    TourActivity('Al Thumamah', 'Nature', 300),
    TourActivity('Rawdat Kharaim', 'Nature', 400),
    TourActivity('Camping', 'Nature', 1000),
    TourActivity('Resorts', 'Nature', 1700),
    TourActivity('Perfume Expo', 'Exciting', 700),
    TourActivity('Theatre Shows', 'Exciting', 800),
    TourActivity('Swimming with Dolphine', 'Exciting', 550),
    TourActivity('Concert', 'Exciting', 700),
    TourActivity('Ramez Experience', 'Exciting', 200),
    TourActivity('Crystal Maze', 'Exciting', 300),
    TourActivity('Escape Room', 'Exciting', 100),
]

class Chromosome:
    def __init__(self, genes):
        self.genes = genes
        self.fitness = self.calculate_fitness()
    
    def calculate_fitness(self):
        # Calculate the fitness based on the budget
        budget_weight = 0.5
        experience_weight = 2
        num_activities_weight = 0.5
        total_weight = budget_weight + experience_weight + num_activities_weight

        budget_score = budget_weight / total_weight
        experience_score = experience_weight / total_weight
        num_activities_score = num_activities_weight / total_weight
        budget = 0
        for activity in self.genes:
            budget += activity.cost
        if budget > BUDGET:
            return 0
        budget_fitness = (BUDGET - budget) / BUDGET
        
        # Calculate the fitness based on the experience type
        activity_types = [activity.type for activity in self.genes]
        experience_fitness = 0
        if EXPERIENCE_TYPE == 'Exciting':
            experience_fitness += activity_types.count('Exciting') / len(self.genes)
        elif EXPERIENCE_TYPE == 'Shopping & Resturants':
            experience_fitness += activity_types.count('Shopping & Resturants') / len(self.genes)
        elif EXPERIENCE_TYPE == 'Nature':
            experience_fitness += activity_types.count('Nature') / len(self.genes)
        
        # Calculate the fitness based on the number of activities
        num_activities_fitness = 0
        if len(self.genes) == NUM_ACTIVITIES:
            num_activities_fitness = 1
        elif len(self.genes) < NUM_ACTIVITIES:
            num_activities_fitness = len(self.genes) / NUM_ACTIVITIES
        
        # Calculate the overall fitness using the weighted sum
        fitness = budget_score * budget_fitness + experience_score * experience_fitness + num_activities_score * num_activities_fitness
        
        return fitness
    

def initialize_population(population_size):
    # Initialize a population of chromosomes with random genes
    population = []
    for i in range(population_size):
        genes = random.sample(ACTIVITIES, NUM_ACTIVITIES)
        chromosome = Chromosome(genes)
        population.append(chromosome)
    return population

def evaluate_fitness(population):
    # Evaluate the fitness of each chromosome in the population
    for chromosome in population:
        chromosome.fitness = chromosome.calculate_fitness()
    return population

def select_fittest(population, num_fittest):
    # Select the fittest individuals from the population
    population.sort(key=lambda x: x.fitness)
    fittest = population[num_fittest:]
    return fittest

def crossover(parent1, parent2):
    # Perform crossover to create a new offspring
    offspring = parent1.genes[:int(NUM_ACTIVITIES/2)] + parent2.genes[int(NUM_ACTIVITIES/2):]
    return Chromosome(offspring)

def mutate(chromosome):
    # Mutate a chromosome by randomly swapping two genes
    genes = chromosome.genes[:]
    i, j = random.sample(range(NUM_ACTIVITIES), 2)
    genes[i], genes[j] = genes[j], genes[i]
    return Chromosome(genes)

def evolve(population, num_fittest, num_offspring, mutation_rate):
    # Select the fittest individuals and create offspring through crossover and mutation
    fittest = select_fittest(population, num_fittest)
    offspring = []
    for i in range(num_offspring):
        parent1, parent2 = random.sample(fittest, 2) #Roulette wheel
        offspring.append(crossover(parent1, parent2))
    for chromosome in offspring: 
        if random.uniform(0, 1) < mutation_rate:
            chromosome = mutate(chromosome) 
    fittest.extend(offspring)
    return fittest

def plot(gen, fitness_scores):
    # print(list(range(num_generations)), fitness_scores)
    # Plotting the fitness score vs generation graph
    plt.plot(gen, fitness_scores, "o")
    plt.xlabel('Generation')
    plt.ylabel('Fitness')
    plt.title('Generation vs Fitness')
    plt.show()


def avgFit(population):
    # Calculate average to use it in the plot
    avg = 0
    count = 0
    for chromosome in population:
        avg+= chromosome.fitness
        count+=1
    avg=avg/count
    return avg     

def main():
    
    # Get the name of the tourist
    name = input("Welcome to Riyadh Season Trip Planner! What is your name?\n")
    print(f"Hi {name}!\n")
    
    # Get the number of activities for each day
    NUM_ACTIVITIES_PER_DAY = []
    for i in range(3):
        num_activities = int(input(f"Please enter number of activities you prefer to do in Day{i+1}(1 or 2):\n"))
        NUM_ACTIVITIES_PER_DAY.append(num_activities)
    
    # Get the activity preference of the tourist
    activity_preference = input("Please enter your activity preference (E for Exciting, S for Shopping & Restaurants and N for Nature).\n")
    global EXPERIENCE_TYPE
    EXPERIENCE_TYPE = activity_preference
    if activity_preference == 'E':
        EXPERIENCE_TYPE = 'Exciting'
    elif activity_preference == 'S':
        EXPERIENCE_TYPE = 'Shopping & Resturants'
    elif activity_preference == 'N':
        EXPERIENCE_TYPE = 'Nature'
    
    # Get the budget of the tourist
    budget = int(input("Please enter your budget:\n"))
    global BUDGET
    BUDGET = budget
    
    global NUM_ACTIVITIES
    NUM_ACTIVITIES = sum(NUM_ACTIVITIES_PER_DAY)
    print("We are working on preparing your optimal trip. . .")
    
    # Set the parameters for the genetic algorithm
    POPULATION_SIZE = 400
    NUM_FITTEST = 200
    NUM_OFFSPRING = 200
    MUTATION_RATE = 0.3
    num_generations = 50
    
    # Initialize the population
    population = initialize_population(POPULATION_SIZE)
    
    # Run the genetic algorithm
    generation = 1
    fitness_scores = []
    ge = []
    while generation <= num_generations:
        population = evaluate_fitness(population)
        population = evolve(population, NUM_FITTEST, NUM_OFFSPRING, MUTATION_RATE)
        ge.append(generation)
        fitness_scores.append(avgFit(population))
        generation += 1


    # Show plot between generations vs average fitness score
    plot(ge, fitness_scores)


    # Getting the fittest chromosome from the population
    fittest = select_fittest(population, NUM_FITTEST)[-1] # returns last element which has highest fitness
    print(f"Here is your optimal trip for {name}:\n")
    counter = 0
    for i in range(3):
        print(f"Day {i+1}:")
        for j in range(NUM_ACTIVITIES_PER_DAY[i]):
            if counter < len(fittest.genes):
                activity = fittest.genes[counter]
                print(f"\t- {activity.name} ({activity.cost} SAR)")
                counter += 1
    print(fittest.fitness)            
if __name__ == '__main__':
    main()