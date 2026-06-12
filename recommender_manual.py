import math
import numpy as np 
import string
from nltk.corpus import stopwords

stop_words = set(stopwords.words('english'))
text = open('plot_summaries.txt', 'r+', encoding='utf-8')
text.seek(0)
lines = text.readlines()
text.truncate(0)
text.seek(0)
text.writelines(lines[:250])
input_summery = input('please input the summery:').split(' ') # input summary
input_summery = [str(pt).translate(str.maketrans('', '', string.punctuation)) for pt in str(input_summery).split(' ')] # remove the punctuation for input summary
input_summary = [word for word in input_summery if word.lower() not in stop_words] # remove the stop words for input summary
input_summary = [''.join(fw) for fw in input_summary]
text.write(f"movie;{' '.join(input_summary)};") # write the input summary to text file
text.close()
text_r = open('plot_summaries.txt', 'r+')
text_1 = open('p_s_1.txt', 'r+')
text_2 = open('tf_idf_number.txt', 'w+') 

#step 3

def TF(word, words_in_summary):  # TF 
    return words_in_summary.count(word) / len(words_in_summary)

def I_DF(word, movie_summaries): # IDF 
    n = sum(1 for summary in movie_summaries if word in summary.lower())
    return math.log(250 / (n+1))

result_dict = {}
lines = text_r.read().split(';')

for i in range(251):
    result_dict[lines[2 * i]] = lines[2 * i + 1]  #dict => Movie Name:Movie Summary
    text_1.write(lines[2 * i + 1] + '\n')  # just summary text without summary name

text_1.seek(0)  
text_1_contents = text_1.read()  
res_list = []
tf_idf_dict = {}
idf_dict = {}
for movie_name, movie_summary in result_dict.items():
    tf_idf_vector = []
    for word in list(set(text_1_contents.split(' '))): # for all words in all summary
        word = word.lower()
        tf = TF(word, movie_summary.lower())  # TF Calculate
        if word not in idf_dict.keys():
            idf_dict[word] = I_DF(word, result_dict.values()) #IDF Calculate
        tf_idf = tf * idf_dict[word] #TF(word) * IDF(word)
        tf_idf_vector.append(tf_idf) # append to TF_IDF list for all movie
    tf_idf_dict[movie_name] = tf_idf_vector # dict => movie name:TF_IDF vector
    res_list.append(f'{movie_name};{tf_idf_vector}') # append movie name;tf_idf_number to tf_idf_number.txt

text.close()
text_1.close()

with open("tf_idf_number.txt", "w", encoding= "utf-8") as fp:
    fp.write(",".join(res_list))


def cosine_simularity(input_array, doc_arrays, k):
    name_cosine_list = []
    for name in doc_arrays:
        name_cosine_list.append((name, (np.dot(input_array, doc_arrays[name])) / (np.linalg.norm(input_array) * np.linalg.norm(doc_arrays[name])))) # Calculate the cosine of the input array and the other movie array and append to cosine_list
    return sorted(name_cosine_list, key= lambda x : x[1], reverse = True)[:k if k <= len(name_cosine_list) else len(name_cosine_list)] # sort list[(movie name , cosine)]

def get_input_array(): #  کد ما در قسمت چهارم به این صورت بود که اسم فیلم میدادی و فیلم های شبیه رو بهت میداد الان من سامری جدید رو ریختم توی همون تکست با اسم فیلم پس باید تابع رو برای فیلم فرا بخونم
    while True:
        input_array = None
        chosen_film = 'movie' 
        for name_array in name_array_list:
            if chosen_film == name_array[0]: 
                input_array = name_array[1]
                return input_array  # get input vector
        
with open ('tf_idf_number.txt', 'r') as fd:
    name_array_list = []
    for name_array in fd.read().split(",\n"):
        try:
            array_text = name_array.split(";")[1]
        except:continue
        array = []
        for elem in array_text[1:-1].split(", "): # Extract all numbers in text file
            array.append(float(elem)) #append all number to list
        name_array_list.append((name_array.split(";")[0], array)) # we have list(name,vector)

def main():
    input_array = get_input_array() # Calling the function to say that we want the recommendation of "movie"
    doc_arrays = {}
    for name, array in name_array_list:
        doc_arrays[name] = array
    recommendations = cosine_simularity(input_array=input_array, doc_arrays=doc_arrays, k=6) # get 6 recommendation with movie
    for recommendation in recommendations:
        print(recommendation) #print 6 recommendation

if __name__ == "__main__":
    main()