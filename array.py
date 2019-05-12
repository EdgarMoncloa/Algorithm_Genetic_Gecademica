import random
import time

num_parameters = 4
num_populations = 5
num_classes = 100
num_subject_matters = 80
num_classrooms = 28
num_horaries = 5
num_teachers = 60
min_value = 1
pressure = 3  # individuos que se seleccionan para reporduccion
mutation_probability = .50


def create_class(
        num_teachers,
        num_classrooms,
        num_subject_matters,
        num_horaries):
    asigned_class = []
    asigned_class.append(random.randint(min_value, num_subject_matters))
    asigned_class.append(random.randint(min_value, num_classrooms))
    asigned_class.append(random.randint(min_value, num_horaries))
    asigned_class.append(random.randint(min_value, num_teachers))
    return asigned_class


def create_individual(
        num_teachers,
        num_classrooms,
        num_subject_matters,
        num_horaries):
    individual = []
    for idx in range(0, num_classes):
        individual.append(create_class(
            num_teachers,
            num_classrooms,
            num_subject_matters,
            num_horaries
        ))
    return individual


def create_population():
    return [create_individual(
        num_teachers,
        num_classrooms,
        num_subject_matters,
        num_horaries
    ) for i in range(0, num_populations)]


def fitness_calculate(individual):
    fitness = 0
    for idx_element, element in enumerate(individual):
        individual_compare = individual.copy()
        individual_compare.pop(idx_element)
        for compare_element in individual_compare:
            for idx in range(0, num_parameters):
                if element[idx] == compare_element[idx]:
                    fitness -= 1
    if fitness == 0 :
        print("-----------------------------------------------------FITNES 0")
        print(individual)
        quit()
    return fitness


def selection_and_reproduction(population):
    population_punctuated = [
        (fitness_calculate(element), element)for element in population]
    population_punctuated = [
        element[1] for element in sorted(population_punctuated)]
    population = population_punctuated.copy()

    population_punctuated = population_punctuated[(len(population)-pressure):]    

    # Mix
    for idx in range(len(population)-pressure):
        # Select one point to cut the individual
        cut_point = random.randint(1, num_classes)
        # Select two parents
        parents = random.sample(population_punctuated, 2)
        # Mix genetic material
        population[idx][:cut_point] = parents[0][:cut_point]
        population[idx][cut_point:] = parents[1][cut_point:]

    return population


def mutation(population):
    for idx in range(len(population)-pressure):
        if random.random() <= mutation_probability:
            cut_point = random.randint(0, num_classes-1)
            new_class = create_class(
                num_teachers,
                num_classrooms,
                num_subject_matters,
                num_horaries
            )
            while(new_class == population[idx][cut_point]):
                new_class = create_class(
                    num_teachers,
                    num_classrooms,
                    num_subject_matters,
                    num_horaries
                )
            population[idx][cut_point]=new_class
    return population

def print_data(population):
    print("VALORES")
    for element in population:
        print(element)
    print("FITNESS")
    for idx,element in enumerate(population):
        print("{} : {}".format(idx,fitness_calculate(element)))
    return



start_time = time.time()
# Create First population
population = create_population()
# Print
# print('-----> PRIMERA POBLACION <-----')
# print_data(population)

# Algorithm
for i in range(100000):
    # Selection and rerpoduction
    if i % 1000 == 0:
        print('----------{}-----------------'.format(i))   
    population = selection_and_reproduction(population)
    population = mutation(population)

# Last population
print('-----> ULTIMA POBLACION <-----')
# print_data(population)
# print('(---------{}--------------)'.format(time.time-start_time))