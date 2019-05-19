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

        last_average = 0
        first_average = 0
        self.min_total = 0
        self.num_mutations = 0
        # print titles
        dash = '-'*65
        print(dash)
        print('|{:<10s}|{:<10s}|{:<10s}|{:<10s}|{:<10s}|{:<10s}|{:<10s}|'.format(
            'Iteracion','Promedio','Diferencia','Prob Mut','Minimo','Min Tot','Num muts'))
        print(dash)
        # calculates
        self.mutation_probability = 1
        for idx in range(0,100000):
            self.num_mutations=0
            if idx == 0:
                mutation_probability = .8
            elif idx < 10000:
                self.mutation_probability -= .0005
            elif 10000 < idx < 50000:
                self.mutation_probability -= .001
            elif 50000 < idx < 75000:
                self.mutation_probability -= .002
            # ALGORITHM
            population = self.simple_selection_and_population(population)
            # population = self.mutation(population)
            population = self.uniform_mutation(population)
            #END ALGORITHM

            # first average
            if idx == 0:
                self.min_total = self.fitness_calculate(population[0])
                for element in population:
                    first_average += self.fitness_calculate(element)                    
                first_average = int(first_average / num_population_members)

            # if idx % 100 == 0:
            #     import pdb                
            #     pdb.set_trace()
            # Prints every x iterations
            if idx % 10 == 0:
                # average
                arrayFitness = []
                for element in population:
                    arrayFitness.append(self.fitness_calculate(element))
                average= int(sum(arrayFitness)/num_population_members)     
                # Data to print 
                data = [
                    idx,
                    average,
                    average-last_average,
                    "{0:.7f}".format(self.mutation_probability),
                    min(arrayFitness),
                    self.min_total,
                    self.num_mutations
                ]
                last_average=average
                
                print('|{:<10s}|{:<10s}|{:<10s}|{:<10s}|{:<10s}|{:<10s}|{:<10s}|'.format(
                    str(data[0]),
                    str(data[1]),
                    str(data[2]),
                    str(data[3]),
                    str(data[4]),
                    str(data[5]),
                    str(data[6]),
                    ))
                    # print(element)
                # for element in population:
                    # print(self.fitness_calculate(element))
        # population
    
    def create_class(self):
        asigned_class = []
        # 0 subject matters
        asigned_class.append(
            random.randint(self.min_value,self.num_subject_matters)
        )
        # 1 classrooms
        asigned_class.append(
            random.randint(self.min_value,self.num_classrooms)
        )
        # 2 teachers
        asigned_class.append(
            random.randint(self.min_value,self.num_teachers)
        )
        # 3 horaries
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
        count = 0
        for idx_element,element in enumerate(individual):
            individual_compare = list(individual)
            individual_compare.pop(idx_element)
            for compare_element in individual_compare:
                count += 1
                if(element[2]==compare_element[2] and element[3] ==compare_element[3]):
                # if(element[2]!=compare_element[2] and element[3]!=compare_element[3]):
                    fitness += 1
                if(element[1]==compare_element[1] and element[3]==compare_element[3]):
                    fitness += 1
        # print(count)
        # print(individual[3])
        if self.min_total > fitness:
            self.min_total = fitness
        if fitness <= 0:
            print('Maximo valor encontrado:')
            for element in individual:
                print(element)
            exit()
        return fitness

    def reproduction(self,best_individuals,population):        
        # MIX
        for idx in range(len(population)):
            # Select one point to cut the individual
            cut_point = random.randint(1, self.num_classes)
            # Select two parents
            parent_1 = numpy.random.choice(range(self.pressure))
            parent_2 = numpy.random.choice(range(self.pressure))
            while (parent_1==parent_2):
                parent_2 = numpy.random.choice(range(self.pressure))
            # Mix genetic material
            child = best_individuals[parent_1][:cut_point] + best_individuals[parent_2][cut_point:] 
            population[idx] = child
        return population

    def simple_selection_and_population(self,population):     
        population_punctuated = [
            (self.fitness_calculate(element), element)for element in population]
        population = [
            element[1] for element in sorted(population_punctuated)]
        # MIX
        best_individuals = population[:self.pressure]
        
        for idx in range(len(population)):
            import pdb
            pdb.set_trace()
            # Select one point to cut the individual
            cut_point = random.randint(1, self.num_classes)
            # Select two parents
            parents = random.sample(range(self.pressure),2)             
            # Mix genetic material
            child = best_individuals[parents[0]][:cut_point] + best_individuals[parents[1]][cut_point:] 
            population[idx] = child

        return population

    def rulete_selection_and_population(self,population):
        punctuations = [
            self.fitness_calculate(element) for element in population
        ]   
        sum_punctuations = sum(numpy.absolute(punctuations))
        # print(sum_punctuations)
        selection_probability = [
            1/numpy.absolute(punctuation) for punctuation in punctuations
        ]
        # print(selection_probability)
        sum_punctuations = sum(punctuations)
        selection_probability = [
            punctuation / sum_punctuations for punctuation in punctuations
        ]
        # print(selection_probability)
        # MIX
        
        choices = numpy.random.choice(
            numpy.arange(0,self.num_population_members),
            self.pressure,
            p=selection_probability)
        print(choices)
        parents = [
            population[choice] for choice in choices
        ]
        population=self.reproduction(
            best_individuals = parents,
            population = population,
        )
        return population

    def mutation(self,population):
        # for x in range(0,5+int(self.num_classes/10)):
        for idx in range(len(population)):
            if random.random() <= self.mutation_probability:
                cut_point = random.randint(0, self.num_classes-1)
                new_class = self.create_class()
                while(new_class == population[idx][cut_point]):
                    new_class = self.create_class()
                population[idx][cut_point]=new_class
        return population        

    def uniform_mutation(self,population):
        # if random.random() <= self.mutation_probability:  
        # print(population[0])   
        population_punctuated = [
            (self.fitness_calculate(element), element)for element in population]
        population = [
            element[1] for element in sorted(population_punctuated,reverse=True)]
        for idx in range(self.num_population_members):
            if random.random() < self.mutation_probability:
                individual_1 = random.sample(range(self.num_classes),2)
                individual_2 = random.sample(range(self.num_classes),2)
                population[idx][individual_1] = self.create_class()
                population[idx][individual_2] = self.create_class()
                self.num_mutations+=1
        return population


algorithm= AG(
    num_parameters = 4,
    num_population_members = 30,
    num_classes = 100,
    num_subject_matters = 75,
    num_classrooms = 50,
    num_horaries = 5,
    num_teachers = 50,
    min_value = 0,
    pressure = 30,  # individuos que se seleccionan para reporduccion
    mutation_probability = .2, #Por ahora no importa    
)