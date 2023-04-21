import pandas as pd
import nltk
import string
import numpy
import ast
import re
import unidecode
import os
import numpy as np
import csv

from sklearn.metrics.pairwise import cosine_similarity
from words_parser import ingredient_parser, category_parser
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from gensim.models import Word2Vec

def get_recommendations(N, scores):
    """
    Top-N recomendations order by score
    """
    df_recipes = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\parseddocuments.csv')

    # order the scores with and filter to get the highest N scores
    S = len(scores)
    top = sorted(range(S), key=lambda x: scores[x], reverse=True)[:N]
    # create dataframe to load in recommendations
    recommendation = pd.DataFrame(columns=["recipe_name", "ingredients", "category", "recipe_instructions","score"])
    count = 0
    for i in top:
        recommendation.at[count, "recipe_name"] = df_recipes["Name"][i]
        recommendation.at[count, "ingredients"] = df_recipes["RecipeIngredientParts"][i]
        recommendation.at[count, "category"] = df_recipes["Keywords_parsed"][i]
        recommendation.at[count, "recipe_instructions"] = df_recipes["RecipeInstructions"][i]
        recommendation.at[count, "score"] = f"{scores[i]}"
        count += 1

    return recommendation
 
class TfidfEmbeddingVectorizer(object):
    def __init__(self, word_model):

        self.word_model = word_model
        self.word_idf_weight = None
        self.vector_size = word_model.wv.vector_size

    def fit(self, docs):  # comply with scikit-learn transformer requirement
        """
		Fit in a list of docs, which had been preprocessed and tokenized,
		such as word bi-grammed, stop-words removed, lemmatized, part of speech filtered.
		Then build up a tfidf model to compute each word's idf as its weight.
		Noted that tf weight is already involved when constructing average word vectors, and thus omitted.
		:param
			pre_processed_docs: list of docs, which are tokenized
		:return:
			self
		"""

        text_docs = []
        for doc in docs:
            text_docs.append(" ".join(doc))

        tfidf = TfidfVectorizer()
        tfidf.fit(text_docs)  # must be list of text string

        # if a word was never seen - it must be at least as infrequent
        # as any of the known words - so the default idf is the max of
        # known idf's
        max_idf = max(tfidf.idf_)  # used as default value for defaultdict
        self.word_idf_weight = defaultdict(
            lambda: max_idf,
            [(word, tfidf.idf_[i]) for word, i in tfidf.vocabulary_.items()],
        )
        return self

    def transform(self, docs):  # comply with scikit-learn transformer requirement
        doc_word_vector = self.word_average_list(docs)
        return doc_word_vector

    def word_average(self, sent):
        """
		Compute average word vector for a single doc/sentence.
		:param sent: list of sentence tokens
		:return:
			mean: float of averaging word vectors
		"""

        mean = []
        for word in sent:
            if word in self.word_model.wv.index_to_key:
                mean.append(self.word_model.wv.get_vector(word) * self.word_idf_weight[word])  # idf weighted

        if not mean:  # empty words
            # If a text is empty, return a vector of zeros.
            # logging.warning(
            #     "cannot compute average owing to no vector for {}".format(sent)
            # )
            return np.zeros(self.vector_size)
        else:
            mean = np.array(mean).mean(axis=0)
            return mean

    def word_average_list(self, docs):
        """
		Compute average word vector for multiple docs, where docs had been tokenized.
		:param docs: list of sentence in list of separated tokens
		:return:
			array of average word vector in shape (len(docs),)
		"""
        return np.vstack([self.word_average(sent) for sent in docs])
    
def get_and_sort_corpus(data):
    """
    Get corpus with the documents sorted in alphabetical order
    """
    sorted = []
    for doc in data.parsed_categorylist_keywords.values:
        doc = ast.literal_eval(doc)
        doc.sort()
        sorted.append(doc)
    return sorted

def addsorteddoctocsv(rec, input):
    
    with open(r'app\csvfiles\recipesbycategory.csv', 'w',encoding='UTF8', newline='') as file:
        
        writer = csv.writer(file)

        writer.writerow(['RecipeId','Name','CookTime','RecipeCategory','Keywords_parsed','RecipeIngredientParts','RecipeInstructions','parsed_categorylist_keywords','ingredients_parsed'])
        
        df_recipes = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\parseddocuments.csv')
        
        
        count = 0
        rows = []
        print("started adding the docs to the file")
        print(len(rec))
        for i in rec:
            
            rows.clear()
            t= ""
            recipeid = df_recipes["RecipeId"][i]
            name = df_recipes["Name"][i]
            cooktime = df_recipes["CookTime"][i]
            categories = df_recipes["RecipeCategory"][i]
            Keywords_parsed = df_recipes["Keywords_parsed"][i]
            ingredients = df_recipes["RecipeIngredientParts"][i]
            ingredientsparsed = df_recipes["ingredients_parsed"][i]
            instructions = df_recipes["RecipeInstructions"][i]
            parsedcatergorylist = df_recipes["parsed_categorylist_keywords"][i]
            count += 1

            check = all(u in parsedcatergorylist for u in input)

            if check: 
                rows.append([recipeid, name, cooktime, categories, Keywords_parsed, ingredients, instructions, parsedcatergorylist, ingredientsparsed])

                #t = ', '.join(map(lambda x: '"'+ str(x) + '"', rows[0]))

                writer.writerow(rows[0])
            else:
                continue
            

    file.close()
    print("added to csv successfully")    
    return 0


def get_recs(ingredients, N=10):
    # loading in the ingredients word2vec model 
    model = Word2Vec.load("app\models\model_cbow_categorykeywords.bin")
    model.init_sims(replace=True)
    #check if modle is there
    if model:
        print("Successfully loaded model :)")
    # load in data
    data  = pd.read_csv(r"app\csvfiles\parsed_Categories.csv")
    
    # create corpus
    corpus = get_and_sort_corpus(data)

    # use TF-IDF as weights for each word embedding
    tfidf_vec_tr = TfidfEmbeddingVectorizer(model)
    tfidf_vec_tr.fit(corpus)
    doc_vec = tfidf_vec_tr.transform(corpus)
    doc_vec = [doc.reshape(1, -1) for doc in doc_vec]
    assert len(doc_vec) == len(corpus)

    # create embessing for input text
    input = ingredients
    # create tokens with elements
    input = input.split(",")
    # parse ingredient list
    input = category_parser(input)
    print("This is is the input : ", input)
    
    # get embeddings for ingredient doc
    input_embedding = tfidf_vec_tr.transform([input])[0].reshape(1, -1)
    # get cosine similarity between input embedding and all the document embeddings
    cos_sim = map(lambda x: cosine_similarity(input_embedding, x)[0][0], doc_vec)
    scores = list(cos_sim)
    
    # Filter top N recommendations
    recommendations = get_recommendations(N, scores)
    #addsorteddoctocsv(recommendations, input)

    return recommendations   
 

#input = "meat,savory"
#rec = get_recs(input)

def changetolist(values):
    if isinstance(values, list):
        keysw = values
        
    else:
        keysw = ast.literal_eval(values)
    return keysw


# category sorter 

def getsortedcategorycsv(rec, input):
    #opens the csv file for over writting to add the new list of recipes by a certain category/categories
    with open('app\csvfiles\specific_category.csv', 'w', encoding='UTF8', newline='') as file:
        
        #file pointer for csv file
        writer = csv.writer(file)

        #adds the headings of the csv file
        writer.writerow(['RecipeId','Name','CookTime','RecipeCategory','Keywords_parsed','RecipeIngredientParts','RecipeInstructions','parsed_categorylist_keywords','ingredients_parsed'])
        
        #opens the parsed document csv file for reading.
        df_recipes = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\parseddocuments.csv', encoding= 'unicode_escape')
        
        rows = []
        print("started adding the docs to the file")
        #loops through the parsed documents to sort by categories given 
        for i in len(rec):
            
            rows.clear()
            #getting the needed infromation from the parsed documents file for adding to the new file specific_category 
            recipeid = df_recipes["RecipeId"][i]
            name = df_recipes["Name"][i]
            cooktime = df_recipes["CookTime"][i]
            categories = df_recipes["RecipeCategory"][i]
            Keyword_parsed = df_recipes["Keywords_parsed"][i]
            ingredients = df_recipes["RecipeIngredientParts"][i]
            ingredientsparsed = df_recipes["ingredients_parsed"][i]
            instructions = df_recipes["RecipeInstructions"][i]
            parsedcatergorylist = df_recipes["parsed_categorylist_keywords"][i]

            #checks the categoty list with the current recipe categroy list to see if it has the all the categories beeing sorted by
            check = all(u in parsedcatergorylist for u in input)

            #checks if the check list is empty or not and adds the data to the file 
            if check: 
                rows.append([recipeid, name, cooktime, categories, Keyword_parsed, ingredients, instructions, parsedcatergorylist, ingredientsparsed])

                #t = ', '.join(map(lambda x: '"'+ str(x) + '"', rows[0]))
                #print(type(t))
                writer.writerow(rows[0])
            else:
                continue
            

    file.close()
    print("added to csv successfully")    
    return 0

#input= ['meat', 'savory']
#data = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\updated_Categories.csv')
#tester = getsortedcategorycsv(data["Keywords_parsed"], input)
