import random
import time
import numpy
# import numpy


class AG:
    def __init__(
            self,
            num_parameters,
            num_population_members,
            num_classes,
            num_subject_matters,
            num_classrooms,
            num_horaries,
            num_teachers,
            min_value,
            pressure,
            mutation_probability):
        self.num_parameters = num_parameters
        self.num_population_members = num_population_members
        self.num_classes = num_classes
        self.num_subject_matters = num_subject_matters
        self.num_classrooms = num_classrooms
        self.num_horaries = num_horaries
        self.num_teachers = num_teachers
        self.min_value = min_value
        self.pressure = pressure
        self.mutation_probability = mutation_probability
        population = self.create_population()
        for idx in range(0,1000000):
            # population = self.simple_selection_and_population(population)
            self.rulete_selection_and_population(population)
            population = self.mutation(population)
            if idx % 1000 == 0:
                print('-----BEST-----')
                print(num_classes*num_classes)
                print('-----{}-----'.format(idx))
                for element in population:
                  print(self.fitness_calculate(element))
                    # print(element)
                # for element in population:
                    # print(self.fitness_calculate(element))
        # population

    
    def create_class(self):
        asigned_class = []
        asigned_class.append(
            random.randint(self.min_value,self.num_subject_matters)
        )
        asigned_class.append(
            random.randint(self.min_value,self.num_classrooms)
        )
        asigned_class.append(
            random.randint(self.min_value,self.num_teachers)
        )
        asigned_class.append(
            random.randint(self.min_value,self.num_horaries)
        )
        return asigned_class
    
    def create_individual(self):
        individual = []
        for idx in range(0,self.num_classes):
            individual.append(self.create_class())
        return individual

    def create_population(self):
        population = []
        for i in range(0,self.num_population_members):
            population.append(self.create_individual())
        return population

    def fitness_calculate(self,individual):
        fitness = 0
        # count =0
        for idx_element,element in enumerate(individual):
            individual_compare = list(individual)
            individual_compare.pop(idx_element)
            for compare_element in individual_compare:
                # count += 1
                if(element[2]!=compare_element[2]):
                # if(element[2]!=compare_element[2] and element[3]!=compare_element[3]):
                    fitness += 1
                # if(element[1]!=compare_element[1] and element[3]!=compare_element[3]):
                    # fitness += 1
        # print(count)
        return fitness

    def reproduction(self,parents,population):        
        # MIX
        for idx in range(self.num_population_members-self.pressure-1):
            # Select one point to cut the individual
            cut_point = random.randint(1, self.num_classes)
            # Select two parents
            parents = random.sample(parents, 2)
            # Mix genetic material
            population[idx][:cut_point] = parents[0][:cut_point]
            population[idx][cut_point:] = parents[1][cut_point:]
        return population

    def simple_selection_and_population(self,population):
        population_punctuated = [
            (self.fitness_calculate(element), element)for element in population]
        population_punctuated = [
            element[1] for element in sorted(population_punctuated)]
        population = list(population_punctuated)

        population_punctuated = population_punctuated

        # MIX
        for idx in range(len(population)-self.pressure):
            # Select one point to cut the individual
            cut_point = random.randint(1, self.num_classes)
            # Select two parents
            parents = random.sample(population_punctuated, 2)
            # Mix genetic material
            population[idx][:cut_point] = parents[0][:cut_point]
            population[idx][cut_point:] = parents[1][cut_point:]
        return population

    def rulete_selection_and_population(self,population):
        punctuations = [
            self.fitness_calculate(element) for element in population
        ]   
        sum_punctuations = sum(punctuations)
        selection_probability = [
            punctuation  / sum_punctuations for punctuation in punctuations
        ]
        # MIX
        
        choices = numpy.random.choice(
            numpy.arange(0,self.num_population_members),
            self.pressure,
            p=selection_probability)
        parents = [
            population[choice] for choice in choices
        ]
        population=self.reproduction(
            parents = parents,
            population = population,
        )
        return population

    def mutation(self,population):
        for x in range(0,5+int(self.num_classes/10)):
            for idx in range(len(population)):
                if random.random() <= self.mutation_probability:
                    cut_point = random.randint(0, self.num_classes-1)
                    new_class = self.create_class()
                    while(new_class == population[idx][cut_point]):
                        new_class = self.create_class()
                    population[idx][cut_point]=new_class
        return population        


algorithm= AG(
    num_parameters = 4,
    num_population_members = 30,
    num_classes = 100,
    num_subject_matters = 50,
    num_classrooms = 30,
    num_horaries = 5,
    num_teachers = 60,
    min_value = 0,
    pressure = 10,  # individuos que se seleccionan para reporduccion
    mutation_probability = .2,    
)