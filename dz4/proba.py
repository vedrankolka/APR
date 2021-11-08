import numpy as np

population = [np.array([1, 2]), np.array([2, 1]), np.array([1, 1]), np.array([2, 2])]

one_array = np.array(population)
print(one_array.shape)

np.save('proba.npy', one_array)

my_arr = np.load('proba.npy')
print(my_arr)

"""
if interactive_mode:
    if input('Save hyperparameters configuration and population (yes / no) ? >> ').lower() == 'yes':
        hyperparams_path = input('Path to hyperparameters file >> ')
        shutil.copy(sys.argv[1], hyperparams_path)

        population_path = input('Path to population file >> ')
        population_array = np.array([solution.decode() for solution in double_population])
        np.save(population_path, population_array)

        print('Done.')
"""