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


#input = "meat,savory"
#rec = get_recs(input)


# category sorter 

def getsortedcategorycsv(rec, input):
    print(input, type(input))
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
        for i in range(len(rec)):
            
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

#input= ['sweet']
#data = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\parseddocuments.csv')
#tester = getsortedcategorycsv(data["Keywords_parsed"], input)
