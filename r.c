#include <stdio.h>
#include <stdlib.h>
#include <time.h>
#include <math.h>
#define QUEEN 8

void generate_population(int population_size, int population[][QUEEN]);
int fitness_score(int state[]);
void crossover(int population_size, int population[][QUEEN]);
void mutate(int population_size, int population[][QUEEN]);
void evaluate_population(int population_size, int population[][QUEEN], int *best_fitness, int best_solution[]);
int solution_found(int best_fitness);

int main() 
{
    srand(time(NULL));
    int population_size = 150;
    int population[population_size][QUEEN];
    int best_fitness = 0;
    int best_solution[QUEEN];

    //prepare the population
    generate_population(population_size, population);

    //loop till solution is found
    while (!solution_found(best_fitness)) 
    {
        //get fittest population
        evaluate_population(population_size, population, &best_fitness, best_solution);

        //crossover the parent population
        crossover(population_size, population);

        //mutate population
        mutate(population_size, population);
    }

    //print solution
    printf("Solution found!\n");
    printf("Queen State: ");
    for (int i = 0; i < QUEEN; i++) 
    {
        printf("%d ", best_solution[i]);
    }
    printf("\n");
    printf("Fitness Score: %d\n", best_fitness);

    return 0;
}

void generate_population(int population_size, int population[][QUEEN]) 
{
    //initialize population
    for (int i = 0; i < population_size; i++)
    {
        for (int j = 0; j < QUEEN; j++)
        {
            population[i][j] = rand()% QUEEN + 1;
        }
        
    }
}

int fitness_score(int state[]) 
{
    //numebers of queens attacked
    int clashes = 0;

    //calculate the number of clashes
    for (int i = 0; i < QUEEN; i++)
    {
        for(int j = i + 1; j < QUEEN; j++) 
        {
            //if two queens in the same row OR two queens diagonal
            if(state[i] == state[j] || abs(state[i] - state[j]) == abs(i - j))
            {
                clashes = clashes + 1;
            }
        }
    }
    int final_score = (QUEEN * (QUEEN - 1))/2 - clashes;
    return final_score;
}

void crossover(int population_size, int population[][QUEEN]) 
{
    int parents[2][QUEEN];

    for (int i = 0; i < population_size; i += 2) 
    {
        //randomly select two parents
        int parent1_index = rand() % population_size;
        int parent2_index = rand() % population_size;

        //copy the parents
        for (int j = 0; j < QUEEN; j++) 
        {
            parents[0][j] = population[parent1_index][j];
            parents[1][j] = population[parent2_index][j];
        }

        //random crossover point
        int crossover_point = rand() % (QUEEN - 1) + 1;

        //perform crossover
        for (int j = crossover_point; j < QUEEN; j++) 
        {
            population[i][j] = parents[1][j];
            population[i + 1][j] = parents[0][j];
        }
    }
}

void mutate(int population_size, int population[][QUEEN]) 
{
    //chosen mutation rate
    double mutation_rate = 0.1;

    for (int i = 0; i < population_size; i++) 
    {
        for (int j = 0; j < QUEEN; j++) 
        {
            double rand_num = (double)rand() / RAND_MAX;
            if (rand_num <= mutation_rate) 
            {
                //mutate value
                population[i][j] = rand() % QUEEN + 1;
            }
        }
    }
}

void evaluate_population(int population_size, int population[][QUEEN], int *best_fitness, int best_solution[]) 
{
    //find the best fitness score in the population
    for (int i = 0; i < population_size; i++) 
    {
        int fitness = fitness_score(population[i]);
        if (fitness > *best_fitness) 
        {
            //update fitness score
            *best_fitness = fitness;
            for (int j = 0; j < QUEEN; j++) 
            {
                best_solution[j] = population[i][j];
            }
        }
    }
}

int solution_found(int best_fitness) 
{
    //fitness_max is 28 which is the solution
    int fitness_max = (QUEEN * (QUEEN - 1)) / 2;
    return best_fitness == fitness_max;
}
