import random
import time
import numpy
import pdb
from collections import Counter
import datetime

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
        self.date_start = datetime.datetime.now()
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
        idx = 0
        while True:
            self.num_mutations=0
            if idx == 0:
                mutation_probability = 1
            elif idx < 50000:
                self.mutation_probability -= .00001 
            elif 50000 < idx < 70000:
                self.mutation_probability -= .00002
                
            # ALGORITHM
            population = self.rulete_selection_and_population(population)
            population = self.uniform_mutation(population)
            #END ALGORITHM

            # first average
            if idx == 0:
                array_first_min = []
                for element in population:
                    fitness_value = self.fitness_calculate(element)   
                    array_first_min.append(fitness_value)
                    first_average += fitness_value
                first_average = int(first_average / num_population_members)
                self.min_total = min(array_first_min)
            
            if idx % 500 == 0:
                # average
                arrayFitness = []                
                for element in population:
                    arrayFitness.append(self.fitness_calculate(element))
                average= int(sum(arrayFitness)/num_population_members)  
                # Local Minium
                local_min = min(arrayFitness)
                # Global Minium
                arrayFitness.append(self.min_total)
                global_min = min(arrayFitness)
                # Data to print 
                data = [
                    idx,
                    average,
                    average-last_average,
                    "{0:.7f}".format(self.mutation_probability),
                    local_min,
                    global_min,
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
            #END WHILE 
            idx +=1
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
        # subject_matters = []  
        classrooms_horaries = []
        teachers_horaries = []
        horaries = []
        for element in individual:
            # subject_matters.append(element[0])
            classrooms_horaries.append((element[1],element[3]))
            teachers_horaries.append((element[2],element[3]))
        repeat_classrooms =Counter(classrooms_horaries)
        repeat_teachers = Counter(teachers_horaries)
        fitness += sum([k[1] for k in repeat_classrooms if repeat_classrooms[k] > 1])
        fitness += sum([k[1] for k in repeat_teachers if repeat_teachers[k] > 1])
        # print(count)
        # print(individual[3])
        if self.min_total > fitness:
            self.min_total = fitness
        if fitness <= 0:
            print('Maximo valor encontrado:')
            for element in individual:
                print(element)
            print('Hora de inicio: ' + str(self.date_start))
            print('Hora de finalizacion: ' + str(datetime.datetime.now()))
            print('Tiempo que se tardo: ' + str(datetime.datetime.now().minute-self.date_start.minute)  )
            exit()
        return fitness

    def reproduction(self,best_individuals,population):        
        # MIX
        num_reproductions = [0] * len(best_individuals)
        idx = 0
        new_population = []
        while len(new_population) <= len(population):
            # Select one point to cut the individual
            cut_point = random.randint(1, self.num_classes)
            # Select two parents
            parent_1 = numpy.random.choice(range(len(best_individuals)))
            parent_2 = numpy.random.choice(range(len(best_individuals)))
            # Mix genetic material
            child_1 = best_individuals[parent_1][:cut_point] + best_individuals[parent_2][cut_point:] 
            new_population.append(child_1)
            # Regulate number of children
            num_reproductions[parent_1] +=1
            num_reproductions[parent_2] +=1
            if num_reproductions[parent_1] > 100:
                best_individuals.pop(parent_1)
                num_reproductions.pop(parent_1)
                parent_2 -= 1
            if num_reproductions[parent_2] > 100:
                best_individuals.pop(parent_2)  
                num_reproductions.pop(parent_2)  
            idx += 1 
        return population

    def simple_selection_and_population(self,population):     
        population_punctuated = [
            (self.fitness_calculate(element), element)for element in population]
        population = [
            element[1] for element in sorted(population_punctuated)]
        # MIX
        best_individuals = population[:self.pressure]
        
        for idx in range(len(population)):
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
        selection_probability = [
            1/numpy.absolute(punctuation) for punctuation in punctuations
        ]
        sum_punctuations = sum(punctuations)
        selection_probability = [
            punctuation / sum_punctuations for punctuation in punctuations
        ]
        # MIX
        
        choices = numpy.random.choice(
            numpy.arange(0,self.num_population_members),
            int(len(population)/2), #self.pressure,
            p=selection_probability)
        best_individuals = [
            population[choice] for choice in choices
        ]
        new_population=self.reproduction(
            best_individuals = best_individuals,
            population = population,
        )
        return new_population

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
        for idx,individual in enumerate(population):
            if random.random() < self.mutation_probability:  
                random_position = random.choice(
                    range(self.num_classes))
                individual[random_position] = self.create_class()
                self.num_mutations+=1
        return population


algorithm= AG(
    num_parameters = 4,
    num_population_members = 20,
    num_classes = 62,
    num_subject_matters = 50,
    num_classrooms = 30,
    num_horaries = 5,
    num_teachers = 52,
    min_value = 1,
    pressure = 10,  # individuos que se seleccionan para reporduccion
    mutation_probability = .2, #Por ahora no importa    
)