import pandas as pd
import numpy as np
import ast
import unidecode

from sklearn.metrics.pairwise import cosine_similarity
from app.words_parser import ingredient_parser
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from gensim.models import Word2Vec
from app.getdocsforcategory import getsortedcategorycsv


def get_recommendations(N, scores,categories):
    """
    Top-N recomendations order by score
    """
    # load in recipe dataset
    if categories == []:
        # load in data
        print("came to parsed ingredients")
        df_recipes  = pd.read_csv(r"C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\parseddocuments.csv", encoding= 'unicode_escape')
    else:
        print("came to category list")
        df_recipes = pd.read_csv(r"C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\specific_category.csv", encoding= 'unicode_escape')
        #uses the full document if there are no recipes with the combination of keywords for categories querried
        if len(df_recipes["Keywords_parsed"]) == 0 :
            df_recipes  = pd.read_csv(r"C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\parsed_ingredients.csv", encoding= 'unicode_escape')

    # order the scores with and filter to get the highest N scores
    top = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:N]
    print("thi is top",top)
    # create dataframe to load in recommendations
    recommendation = pd.DataFrame(columns=["recipe_name", "ingredients", "category", "recipe_instructions","score"])
    count = 0
    for i in top:

        recommendation.at[count, "RecipeId"] = df_recipes["RecipeId"][i]
        recommendation.at[count, "recipe_name"] = df_recipes["Name"][i]
        recommendation.at[count, "ingredients"] = df_recipes["RecipeIngredientParts"][i]
        recommendation.at[count, "category"] = df_recipes["Keywords_parsed"][i]
        recommendation.at[count, "recipe_instructions"] = df_recipes["RecipeInstructions"][i]
        recommendation.at[count, "Images"] = df_recipes["Images"][i]
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
        #print("mean vector of a word", self.word_model.wv.get_vector('peri peri') * self.word_idf_weight['peri peri'])
        #print("checking the weight of a word",self.word_idf_weight['peri peri'])
        #print("vector of a word", self.word_model.wv.get_vector('peri peri'))
        #print("vector of a word", self.word_model.wv.get_vector('sugar'))

        if not mean:  # empty words
            # If a text is empty, return a vector of zeros.
            # logging.warning(
            #     "cannot compute average owing to no vector for {}".format(sent)
            # )
            return np.zeros(self.vector_size)
        else:
            #print("before",mean)
            mean = np.array(mean).mean(axis=0)
            #print("mean after",mean)
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
    for doc in data.ingredients_parsed.values:
        doc = ast.literal_eval(doc)
        doc.sort()
        sorted.append(doc)
    return sorted

def get_recs(ingredients, N, categories):
    print(ingredients)
    # loading in the ingredients word2vec model 
    model = Word2Vec.load("app\models\model_cbow_ingredients.bin")
    model.init_sims(replace=True)
    #check if modle is there
    if model:
        print("Successfully loaded model :)")
    
    #check if there are categories that the corpus was sorted for
    if categories == []:
        # load in data
        print("came to parsed ingredients")
        data  = pd.read_csv(r"app\csvfiles\parsed_ingredients.csv", encoding= 'unicode_escape')
    else:
        print("came to category list")
        dataforsort = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\parseddocuments.csv')
        getsortedcategorycsv(dataforsort["Keywords_parsed"], categories)
        data = pd.read_csv(r"app\csvfiles\specific_category.csv", encoding= 'unicode_escape')
        #uses the full document if there are no recipes with the combination of keywords for categories querried
        if len(data["Keywords_parsed"]) == 0 :
            data  = pd.read_csv(r"app\csvfiles\parsed_ingredients.csv", encoding= 'unicode_escape')
    
    # parse ingredients
    #data["parsed"] = data.RecipeIngredientParts.apply(ingredient_parser)

    # create corpus
    corpus = get_and_sort_corpus(data)

    #print("this is after corpus:", corpus)

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
    input = ingredient_parser(input)
    #print("this is input", input)
    # get embeddings for ingredient doc
    input_embedding = tfidf_vec_tr.transform([input])[0].reshape(1, -1)
    
    #print("This is doc_vec", doc_vec)
    #print("this is input embeding", input_embedding)

    # get cosine similarity between input embedding and all the document embeddings
    cos_sim = map(lambda x: cosine_similarity(input_embedding, x)[0][0], doc_vec)
    scores = list(cos_sim)
    
    # Filter top N recommendations
    recommendations = get_recommendations(N, scores,categories)
    
    return recommendations   

#data  = pd.read_csv(r"app\csvfiles\parsed_ingredients.csv")
#dit= data.RecipeIngredientParts.values
#for i in dit:
#    print(type(ast.literal_eval(i)))

#"peas, rice , oat, flour, yam, banana, cucumber, mango , ginger, pork"
#input = "kiwi,banana,grapes,raspberries,black berries,milk,peanutbutter"
#categories = ['sweet','beverage']
#rec = get_recs(input, 10, categories)
#print(rec)