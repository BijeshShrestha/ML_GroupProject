import pickle

pickle_file_path = 'diseaseLabels_256.pickle'

with open(pickle_file_path, 'rb') as file:
    data = pickle.load(file)
# print(data)
    
unique_names = set(data)  
print(unique_names)