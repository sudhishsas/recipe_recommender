import pandas as pd
import nltk
import string
import numpy
import ast
import re
import unidecode
import os
import csv

# nltk.download('wordnet')
from nltk.stem import WordNetLemmatizer
from nltk.corpus import wordnet
from collections import Counter
import config



# lemmatizer = WordNetLemmatizer()
# measures = [lemmatizer.lemmatize(m) for m in measures]
# words_to_remove = [lemmatizer.lemmatize(m) for m in words_to_remove]
data = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\updated_Categories.csv')

def ingredient_parser(ingreds):
    
    #ingreds = ingreds.tolist()
    """

    This function takes in a list (but it is a string as it comes from pandas dataframe) of
       ingredients and performs some preprocessing.
       For example:

       input = '['1 x 1.6kg whole duck', '2 heaped teaspoons Chinese five-spice powder', '1 clementine',
                 '6 fresh bay leaves', 'GRAVY', '', '1 bulb of garlic', '2 carrots', '2 red onions',
                 '3 tablespoons plain flour', '100 ml Marsala', '1 litre organic chicken stock']'

       output = ['duck', 'chinese five spice powder', 'clementine', 'fresh bay leaf', 'gravy', 'garlic',
                 'carrot', 'red onion', 'plain flour', 'marsala', 'organic chicken stock']

    """
    measures = ["teaspoon","t", "tsp.", "tablespoon", "T", "tbl.","tb","tbsp.", "fluid ounce","fl oz","gill","cup",
        "c","pint","p","pt","fl pt","quart","q","qt","fl qt","gallon","g","gal","ml","milliliter","millilitre","cc",
        "mL","l", "liter","litre","L","dl","deciliter","decilitre","dL","bulb","level","heaped","rounded","whole","pinch","medium","slice","pound","lb","#","ounce","oz","mg","milligram","milligramme",
        "g","gram","gramme","kg","kilogram","kilogramme","x","of","mm","millimetre","millimeter","cm",
        "centimeter","centimetre","m","meter","metre","inch","in","milli","centi","deci","hecto","kilo"]
    
    words_to_remove = ["fresh", "minced", "chopped" "oil", "a", "red", "bunch", "and", "or", "leaf","large", "extra", "sprig", "ground", "handful","free", "small", "pepper", "virgin", "range", "from", "dried","sustainable","black","peeled", "higher", "welfare", "seed", "for","finely", "freshly","sea",
        "quality","white", "ripe", "few", "piece", "source", "to", "organic","flat", "smoked", "sliced", "green", "picked", "the", "stick","plain", "plus","mixed", "bay", "your", "cumin", "optional", "fennel", "serve", "mustard", "unsalted", "baby", "paprika", "fat", "ask", "natural","skin", "roughly", "into", "such", "cut", "good","brown",
        "grated","trimmed", "oregano", "powder", "yellow", "dusting", "knob", "frozen", "on", "deseeded", "low", "runny", "balsamic", "cooked", "streaky", "rasher","zest","pin", "groundnut", "breadcrumb", "turmeric", "halved", "grating", "stalk","light","tinned", "reduced", "unbleached",
        "dry", "soft", "rocket", "bone", "colour", "washed", "skinless", "leftover", "splash", "removed", "dijon", "thick", "big", "hot", "drained", "sized", "chestnut", "fishmonger", "english", "dill", "caper", "raw", "worcestershire", "flake", "cider", "cayenne", "tbsp", "leg", "pine", "wild", "if", "fine", "herb", "almond",
        "shoulder",  "cube", "dressing", "with", "chunk", "spice", "thumb", "garam", "new", "little", "punnet", "shelled", "other" "chopped",  "salt", "olive", "taste", "can", "water", "diced", "package", "italian", "shredded", "divided","seedless", "german", "rind", "golden", 
        "all", "purpose", "crushed", "more", "needed", "thinly", "boneless", "half", "thyme", "cubed","cinnamon", "cilantro","jar", "seasoning", "extract", "sweet","baking", "beaten", "heavy", "seeded", "tin", "uncooked", "crumb", "salted", "the", "and", "such as", "miniature",
        "style","thin", "nut", "coarsely", "spring", "strip", "rinsed","root","quartered","head", "softened", "container", "crumbled", "frying", "lean", "cooking", "roasted", "warm", "whipping", "thawed", "corn", "pitted", "sun", "sweetened", "lowfat", "nottingham", "live",
        "kosher", "bite", "toasted", "lasagna","split", "melted", "degree", "lengthwise","romano", "packed", "pod", "anchovy","rom","prepared","juiced","fluid","floret","room", "active", "seasoned", "mix", "deveined", "lightly", "anise", "thai","size", "unsweetened", "torn", "wedge", "sour", "jumbo",
        "basmati", "marinara", "dark","temperature", "garnish", "bouillon", "loaf", "shell", "reggiano", "canola", "parmigiano", "round", "canned", "ghee", "crust", "long", "broken", "ketchup", "bulk", "cleaned", "condensed", "sherry",  "provolone", "cold", "cottage", "spray", "nonfat", "chard", 
        "pecorino", "part", "bottle", "sodium", "french", "roast", "stem", "link", "firm", "asafoetida", "mild", "dash", "boiling", "oil", "chopped", "vegetable oil", "chopped oil", "garlic", "skin off", "bone out" "from sustrainable sources", "halves", "instant"]
    
    
    # The ingredient list is now a string so we need to turn it back into a list. We use ast.literal_eval
    #print("checkign list:",ingreds)
    #print("haksd",type(ingreds))
    
    if isinstance(ingreds, list):
        ingredients = ingreds
        
    else:
        ingredients = ast.literal_eval(ingreds)
    # We first get rid of all the punctuation. We make use of str.maketrans. It takes three input
    # arguments 'x', 'y', 'z'. 'x' and 'y' must be equal-length strings and characters in 'x'
    # are replaced by characters in 'y'. 'z' is a string (string.punctuation here) where each character
    #  in the string is mapped to None.
    
    translator = str.maketrans("", "", string.punctuation)
    lemmatizer = WordNetLemmatizer()
    ingred_list = []

    for i in ingredients:
        i.translate(translator)
        # We split up with hyphens as well as spaces
        items = re.split(" |-", i)
        # Get rid of words containing non alphabet letters
        items = [word for word in items if word.isalpha()]
        # Turn everything to lowercase
        items = [word.lower() for word in items]
        # remove accents
        items = [
            unidecode.unidecode(word) for word in items
        ]  #''.join((c for c in unicodedata.normalize('NFD', items) if unicodedata.category(c) != 'Mn'))
        # Lemmatize words so we can compare words to measuring words
        items = [lemmatizer.lemmatize(word) for word in items]
        # Gets rid of measuring words/phrases, e.g. heaped teaspoon
        items = [word for word in items if word not in measures]
        # Get rid of common easy words
        items = [word for word in items if word not in words_to_remove]
        if items:
            ingred_list.append(" ".join(items))
    # ingred_list = " ".join(ingred_list)
    return ingred_list


#data = pd.read_csv('app\parsed_recipesv4.csv')
#test = ingredient_parser(data.RecipeIngredientParts.apply(ingredient_parser))
#for tes in test:
#    print(tes)

def culture_parser(keywords):

    cultur_no_words = ['&', '15', '30', '4', '60', '<', 'a', 'apple', 'appliance', 'artichoke', 'avocado', 'baked', 'baking', 'min', 'hour', 'cook', 'group', 'onion', 'oyster', 'raspberry', 'berry', 'pepper', 'green', 'blue', 'red', 'yellow', 'christmas', 'pear', 'nut', 
                    'bar', 'bass', 'bath/beauty', 'bean', 'beans', 'bear', 'beef', 'beginner', 'berries', 'beverage', 'beverages', 'birthday', 'black', 'bread', 'breads', 'breakfast', 'breast', 'breasts', 'broil/grill', 'brown', 'brownie', 'brunch', 'butter', 'cabbage', 'camping', 'candy', 'canning', 'cantonese', 'carbs', 'catfish', 'cauliflower', 'chard', 'cheese', 'cheesecake', 'cherries', 'chicken', 'chip', 'chocolate', 'cholesterol', 'chowders', 'citrus', 'cleaner', 'clear', 'cocktail', 'coconut', 'collard', 'college', 'contest', 'cooker', 'cookie', 'cookies', 'corn', 'crab', 'cranberry', 'crawfish', 'cream', 'creole', 'crock', 'cucumber', 'curries', 'dairy', 'day', 'deep', 'deer', 'dehydrator', 'dessert', 'desserts', 'diabetic', 'dish', 'dressings', 'duck', 'easy', 'egg', 'eggs', 'elbow', 
                    'elk', 'fiber', 'fish', 'food', 'foods', 'for', 'free', 'freezer', 'fried', 'friendly', 'from', 'frozen', 'fruit', 'fruits', 'fry', 'game', 'gelatin', 'goose', 'grain', 'grains', 'grapes', 'greens', 'groups', 'gumbo', 'halibut', 'halloween', 'ham', 'hanukkah', 'healthy', 'high', 'holiday/event', 'homeopathy/remedies', 'hot', 'hours', 'household', 'hunan', 'ice', 'in...', 'inexpensive', 'jellies', 'kid', 'kidney', 'kiwifruit', 'kosher', 'labor', 'lactose', 'lamb/sheep', 'large', 'leg', 'lemon', 'lentil', 'lime', 'liver', 'livers', 'lobster', 'loin', 'long', 'low', 
                    'lunch/snacks', 'machine', 'mahi', 'mango', 'manicotti', 'marinara', 'mashed', 'meal', 'meat', 'meatballs', 'meatloaf', 'meats', 'medium', 'melons', 'memorial', 'mex', 'microwave', 'mins', 'mixer', 'moose', 'mussels', 'navy', 'no', 'nuts', 'oatmeal', 'octopus', 'of...', 'one', 'onions', 'orange', 'oranges', 'organ', 'oven', 'oysters', 'papaya', 'pasta', 'patricks', 'peanut', 'pears', 'penne', 'pennsylvania', 'peppers', 'perch', 'pheasant', 'pie', 'pies', 'pineapple', 'plums', 'pork', 'pot', 'potato', 'potatoes', 'potluck', 'poultry', 'pressure', 'protein', 'pumpkin', 'punch', 'quail', 'quick', 'rabbit', 'raspberries', 'refrigerator', 'reynolds', 'rice', 'roast', 'roughy', 'salad', 'sandwiches', 'sauce', 'sauces', 'savory', 'scratch', 'served', 'shakes', 'shell', 'shells', 'short', 'slow', 'small', 'smoothies', 'soup', 'soy/tofu', 'spaghetti', 'spicy', 'spinach', 'spreads', 'spring', 'squid', 'st.', 
                    'steak', 'steam', 'stew', 'stews', 'stir', 'stocks', 'stove', 'strawberries', 'strawberry', 'summer', 'sweet', 'szechuan', 'tempeh', 'tex', 'thanksgiving', 'thigh', 'tilapia', 'toddler', 'tomato', 'top', 'tropical', 'trout', 'tuna', 'veal', 'vegan', 'vegetable', 'very', 'weeknight', 'white', 'whitefish', 'whole', 'wild', 'winter', 'wrap', 'yam/sweet', 'year', 'years', 'yeast', 'middle']

    if isinstance(keywords, list):
        keysw = keywords
        
    else:
        keysw = ast.literal_eval(keywords)    

    translator = str.maketrans("", "", string.punctuation)
    lemmatizer = WordNetLemmatizer()
    culture_words = []

    for i in keysw:
        i.translate(translator)
        # We split up with hyphens as well as spaces
        items = re.split(" |-", i)
        # Get rid of words containing non alphabet letters
        items = [word for word in items if word.isalpha()]
        # Turn everything to lowercase
        items = [word.lower() for word in items]
        # remove accents
        items = [unidecode.unidecode(word) for word in items]
        # Lemmatize words so we can compare words to measuring words
        items = [lemmatizer.lemmatize(word) for word in items]
        # Get rid of common easy words
        items = [word for word in items if word not in cultur_no_words]
        if items:
            culture_words.append(" ".join(items))
    return culture_words

category_no_words = ['caribbean','scandinavian', 'residents', 'madagascans', 'da', 'denmark', 'hawaiian', 'venezuelans', 'bruneian', 'slovenia', 'canada', 'bahrainis', 'caicos', 'native', 'territory', 'curacaoans', 'jordan', 'ethiopian', 'timor', 'nevisian', 'madagascan', 'algerian', 'vaticanian', 'surinamese', 'nigeriens', 'ivorian', 'aruba', 'réunionese', 'toméans', 'virgin', 'mayen', 'congo', 'guadeloupeans', 'kosovan', 'barbudan', 'australian', 'miquelon', 'ireland', 'chile', 'philippines', 'micronesian', 'france', 'marianans', 'israeliisraelite', 'american', 'congolese', 'venezuelan', 'senegal', 'habesha', 'latvia', 'eritrean', 'czech', 'guatemala', 'helenian', 'poles', 'norfolk', 'ukrainians', 'miquelonnaises', 'madagascar', 'burundi', 'estonian', 'z', 'zealand', 'rwanda', 'vincentian', 'qataris', 'emiri', 'futunawallisian', 'somali', 'arabians', 'puerto', 'kazakh', 'pakistani', 'tanzania', 'jamaicans', 'greeks', 'senegalese', 'sahrawisahrawiansahraouian', 'koreanssouth', 'comorians', 'qatar', 'panamanian', 'banyarwanda', 'danes', 'magyar', 'wallis', 'ugandan', 'helenians', 'indonesian', 'british', 'wallisians', 'anguilla', 'luxembourg', 'mayotte', 'portuguese', 'belize', 'cypriots', 'liechtenstein', 'koreansnorth', 'ukraine', 'jan', 'estonia', 'equatoguineans', 'turkmens', 'lankans', 'rico', 'bissau-guinean', 'liechtensteiner', 'omanis', 'pierre', 'sudanese', 'monaco', 'cayman', 'timorese', 'liberians', 'macedonians', 'tanzanians', 'venezuela', 'thai', 'eustatius', 'iraqis', 'mongoliansmongols', 'union', 'tomé', 'afghan', 'bermudian', 'sandwich', 'kyrgyzstan', 'koreans', 'herzegovinians', 'new', 'ecuadorians', 'somaliland', 'mauritius', 'nauru', 'saudi', 'colombian', 'cook', 'grenada', 
                        'persian', 'guatemalan', 'nepali', 'cambodians', 'malawian', 'saban', 'tongans', 'england', 'kyrgyzstanis', 'irishmen', 'guineans', 'malaysian', 'benin', 'andorran', 'kazakhstani', 'tonga', 'tunisian', 'tokelau', 'hungarian', 'turkmenistan', 'slovenian', 'haiti', 'jamaica', 'kazakhstan', 'falkland', 'kosovars', 'arubans', 'portugal', 'vietnamese', 'sierra', 'turkey', 'seychelloises', 'samoa', 'bahrain', 'vincentians', 'belgian', 'sweden', 'sahraouis', '&',
                        'gambian', 'konger', 'futunan', 'malawi', 'ghanaian', 'thailand', 'emiratis', 'cocos', 'kittitian', 'jordanian', 'nevisians', 'swedes', 'french', 'irishnorthern', 'formosan', 'islanderssouth', 'rica', 'armenia', 'kazakhs', 'britons', 'tokelauans', 'martin', 'guernseywomen', 'namibia', 'ossetia', 'comoros', 'ethiopians', 'gibraltar', 'timor-leste', 'ricans', 'india', 'marino', 'china', 'cambodia', 'somalilanders', 'angolans', 'cameroonian', 'czechs', 'kirgizkirghiz', 'antigua', 'iceland', 'maldives', 'antarctica', 'bahamians', 'montenegrins', 'samoans', 'djibouti', 'great', 'uzbekistanis', 'lithuanians', 'laolaotian', 'honduran', 'southern', 'barbadians', 'guam', 'martinican', 'são', 'burkina', 'city', 'ramadan', 'fiji', 'hungary', 'tongan', 'kittitians', 'gabonaise', 'philippine', 'papua', 'cantonesehong', 'belizeans', 'curacaoan', 'democratic', 'of', 'bruneians', 'finnish', 'namibians', 'icelandic', 'qatari', 'polynesians', 'mahorans', 'serbsserbians', 'guamanian', 'alanders', 'trinidadians', 'libyan', 'turks', 'luxembourgish', 'saudisaudi', 'guiana', 'swiss', 'angola', 'fijians', 'cuban', 'bosnia', 'brunei', 'cambodian', 'niger', 'guinean', 'tajikistanis', 'biot', 'paraguay', 'futunans', 'anguillan', 'egyptians', 'lithuanian', 'zealanders', 'verde', 'eustatiusstatian', 'bermudans', 'chilean', 'sahara', 'croatia', 'belizean', 'europeans', 'nicaraguan', 'malian', 'réunion', 'bermudan', 'guyana', 'kuwait', 'albanians', 'moldovans', 'colombia', 'gabon', 'barbudans', 'republic', 'norwegian', 'slovak', 'togolese', 'equatorial', 'spanish', 'yemenis', 'italians', 'scots', 'bonairean', 'beninois', 'lanka', 'brazilian', 'azerbaijan', 'barthélemois', 'suriname', 'frenchmen', 'bangladesh', 'mauritanians', 'eritreans', 'africans', 'curacao', 'islandsouth', 'taiwanese', 'hong', 'saint-pierrais', 'surinamers', 'dominican', 'cabo', 'chadians', 'japanese', 'caymanians', 'filipinas', 'ivory', 'lankan', 'greek', 'tobago', 'kitts', 'uruguayans', 'algeria', 'emirian', 'leone', 'mozambican', 'romania', 'nigerians', 'formosans', 'ocean', 'azerbaijani', 'saharan', 'malaysians', 'martiniquaises', 'guadeloupe', 'welshwomen', 'liechtensteiners', 'antarcticans', 'saint-pierraissaint-pierraises', 'canadian', 'burmese', 'nauruans', 'bhutanese', 'comorian', 'gambians', 'sammarinesemsão', 'brazil', 'mexican', 'argentina', 'uzbeks', 'gambia', 'armenian', 'niuean', 'kiribati', 'tokelauan', 'jersey', 'kuwaitis', 'vatican', 'verdean', 'liberia', 'monégasquesmonacans', 'myanmar', 'iranian', 'egypt', 'nigerien', 'niue', 'saint-martinoise', 'ivorians', 'bulgarians', 'mcdonald', 'gibraltarians', 'tuvaluan', 'ecuadorean', 'islanders', 'saudissaudi', 'slovakians', 'moroccan', 'pakistan', 'mozambique', 'guadeloupians', 'kenya', 'burundian', 'algerians', 'vaticanians', 'ghana', 'saint', 'hellenes', 'barthélemoises', 'equatoguinean', 'cunha', 'singapore', 'belarusians', 'malians', 'austrian', 'slovenians', 'swaziswati', 'luxembourgers', 'monégasque', 'icelanders', 'arabia', 'syrian', 'americans', 'palestinians', 'colombians', 'ecuador', 'omani', 'paraguayan', 'dutchmen', 'hongkongers', 'caledonian', 'latvian', 'mongolian', 'pakistanis', 'palau', 'lesotho', 'somalian', 'barbadian', 'austria', 'greenlanders', 'turkish', 'nicaragua', 'tunisia', 'trinidadiantobagonian', 'indians', 'seychelles', 'irishwomen', 'kenyans', 'bahamas', 'beninese', 'spain', 'ossetian', 'panamanians', 'seychellois', 'latviansletts', 'niueans', 'solomon', 'zanzibar', 'african', 'northern', 'belarus', 'southeast', 'tobagonians', 'bonaire', 'mexico', 'barbuda', 'tunisians', 'frenchwomen', 'uzbekistani', 'salvadoran', 'nevis', 'iran', 'malawians', 'rwandans', 'ukrainian', 'salvadorans', 'palestine', 'united', 'tuvaluans', 'afghanistan', 'tajiks', 'bulgarian', 'bolivians', 'polynesia', 'iraqi', 'turkmen', 'ascension', 'uk', 'arab', 'greece', 'zambia', 'guinea-bissau', 'kosovo', 'cameroonians', 'nicaraguans', 'maarten', 'dutch', 'antarctic', 'abkhazians', 'guianese', 'macedonian', 'swedish', 'futuna', 'abkhazia', 'albanian', 'guernsey', 'american', 'mexicans', 'somalia', 'martiniquais', 'azerbaijanis', 'guatemalans', 'somalis', 'príncipe', 'belgium', 'slovaks', 'jamaican', 'mauritanian', 'dutchwomen', 'emirians', 'bolivian', 'english', 'switzerland', 'bermuda', 'botswana', 'faroese', 'kingdom', 'ghanaians', 'bulgaria', 'statians', 'papuan', 'central', 'bolivia', 'abkhazabkhazian', 'mauritania', 'réunionnaises', 'korea', 'honduras', 'norway', 'austrians', 'burkinabe', 'argentines', 'ugandans', 'zambian', 'haitian', 'anguillans', 'magyars', 'helena,', 'montenegrin', 'persians', 'chileans', 'grenadines', 'costa', 'scotsmen', 'estonians', 'irish', 'barundi', 'irishirishmen', 'salvadoreans', 'fijian', 'antiguans', 'libya', 'marianan', 'southwest', 'ni-vanuatu', 'maldivians', 'macedonia', 'panama', 'kenyan', 'filipino', 'kuwaiti', 'east', 'wales', 'netherlands', 'hungarians', 'ethiopia', 'man', 'rwandan', 'montserratian', 'faso', 'lithuania', 'paraguayans', 'scotland', 'kyrgyz', 'greekhellenic', 'chadian', 'albania', 'lucia', 'finland', 'vanuatu', 'grenadian', 'zanzibaris', 'aruban', 'tristan', 'nepalisnepalese', 'guernseymen', 'somalilander', 'libyans', 'zanzibari', 'comorans', 'indonesians', 'kirghiz', 'emirati', 'asia', 'argentinians', 'azeri', 'jordanians', 'european', 'statesu.s.', 'the', 'sint', 'israel', 'kyrgyzstani', 'sudan', 'greenland', 'indonesia', 'malaysia', 'oman', 'rican', 'saint-martinoissaint-martinoises', 'togo', 'slovene', 'sri', 'poland', 'malta', 'singaporeans', 'martinique', 'mongolia', 'réunionnais', 'samoan', 'cubans', 'salvadorians', 'isle', 'japan', 'saba', 'liberian', 'djiboutians', 'mozambicans', 'grenadians', 'israelis', 'filipinos', 'montserratians', 'australians', 'barthélemy', 'serbia', 'tajikistani', 'russians', 'gabonese', 'monacan', 'tajikistan', 'mauritian', 'america', 'palauans', 'arabian', 'uzbekistan', 'lebanese', 'nigerian', 'nepalese', 'germans', 'bosnian', 
                        'croatian', 'pitcairn', 'djiboutian', 'angolan', 'tanzanian', 'burkinabé', 'welsh', 'states', 'armenians', 'tuvalu', 'papuans', 'sahrawis', 'eswatini', 'south', 'lebanon', 'scotswomen', 'leoneans', 'africa', 'cyprus', 'serbian', 'georgian', 'italy', 'argentinian', 'verdeans', 'polynesian', 'indian', 'caledonians', 'batswana', 'slovakia', 'andorrans', 'kosovar', 'finns', 'samoansandorra', 'bangladeshi', 'iraq', 'zimbabwean', 'the', 'territories', 'spaniards', 'georgia', 'haitians', 'polish', 'moroccans', 'salvador', 'coast', 'moldova', 'western', 'svalbard', 'jersianjèrriais', 'syria', 'afghans', 'macau', 'chinese', 'peruvian', 'toméan', 'asian', 'u.s.', 'eritrea', 'maltese', 
                        'sahrawiwestern', 'montserrat', 'bahamian', 'germany', 'heard', 'nauruan', 'welshmen', 'yemen', 'palestinian', 'el', 'netherlanders', 'romanians', 'croatianscroats', 'caymanian', 'vincent', 'korean', 'myanma', 'sahrawian', 'italian', 'georgians', 'micronesia', 'cuba', 'bangladeshis', 'laoslaotians', 'slovenes', 'cameroon', 'namibian', 'kongese', 'russia', 'bermudians', 'mariana', 'bouvet', 'kyrgyzkirgiz', 'singaporean', 'lettish', 'romanian', 'yemeni', 'malagasy', 'island', 'russian', 'britain', 'palauan', 'comoran', 'kong', 'mahoran', 'jerseymen', 'taiwan', 'manx', 'i-kiribati', 'basotho', 'macanese', 'syrians', 'herzegovina', 'hondurans', 'caledonia', 'scottish', 'zimbabwe', 'nepal', 'uganda', 'leonean', 'bahraini', 'uruguayan', 'marshallese', 'bosnians', 'morocco', 'jerseywomen', 'vanuatuan', 'guamanians', 'uruguay', 'vietnam', 'faroe', 'dominicans', 'sammarinese', 'guinea', 'argentine', 'barbados', 'laos', 'dominica', 'antiguan', 'chad', 'peruvians', 'nigeria', 'aland', 'belgians', 'moldovan', 
                        'norwegians', 'australia', 'sahrawi', 'mauritians', 'micronesians', 'lucian', 'cypriot', 'motswana', 'maarteners', 'kazakhstanis', 'canadians', 'north', 'emirates', 'uzbek', 'marshall', 'islands', 'lucians', 'ossetians', 'ecuadorian', 'herzegovinian', 'southwestern', 'saharans', 'swazis', 'trinidad', 'azeris', 'san', 'malinese', 'peru', 'belarusian', 'german', 'montenegro', 'zimbabweans', 'danish', 'maldivian', 'miquelonnais', 'brazilians', 'cajun', 'egyptian', 'zambians', 'mali', 'bhutan', 'iranians', 'guyanese', 'bissau-guineans', 'burundians']
#lemmatizer = WordNetLemmatizer()
#measures = [lemmatizer.lemmatize(m) for m in category_no_words]
#print(measures)
# words_to_remove = [lemmatizer.lemmatize(m) for m in words_to_remove]

def category_parser(category):

    category_no_words = ['caribbean', 'scandinavian', 'resident', 'madagascan', 'da', 'denmark', 'hawaiian', 'venezuelan', 'bruneian', 'slovenia', 
                            'canada', 'bahraini', 'caicos', 'native', 'territory', 'curacaoans', 'jordan', 'ethiopian', 'timor', 'nevisian', 'madagascan', 'algerian', 'vaticanian', 'surinamese', 'nigerien', 'ivorian', 'aruba', 'réunionese', 'toméans', 'virgin', 'mayen', 'congo', 'guadeloupeans', 'kosovan', 'barbudan', 'australian', 'miquelon', 'ireland', 'chile', 'philippine', 'micronesian', 'france', 'marianans', 'israeliisraelite', 'american', 'congolese', 'venezuelan', 'senegal', 'habesha', 'latvia', 'eritrean', 'czech', 'guatemala', 'helenian', 'pole', 'norfolk', 'ukrainian', 'miquelonnaises', 'madagascar', 'burundi', 'estonian', 'z', 'zealand', 'rwanda', 'vincentian', 'qatari', 'emiri', 'futunawallisian', 'somali', 'arabian', 'puerto', 'kazakh', 'pakistani', 'tanzania', 'jamaican', 'greek', 'senegalese', 'sahrawisahrawiansahraouian', 'koreanssouth', 'comorians', 'qatar', 
                            'panamanian', 'banyarwanda', 'dane', 'magyar', 'wallis', 'ugandan', 'helenians', 'indonesian', 'british', 'wallisians', 'anguilla', 'luxembourg', 'mayotte', 'portuguese', 'belize', 'cypriot', 'liechtenstein', 'koreansnorth', 'ukraine', 'jan', 'estonia', 'equatoguineans', 'turkmen', 'lankans', 'rico', 'bissau-guinean', 'liechtensteiner', 'omani', 'pierre', 'sudanese', 'monaco', 'cayman', 'timorese', 'liberian', 'macedonian', 'tanzanian', 'venezuela', 'thai', 'eustatius', 'iraqi', 'mongoliansmongols', 'union', 'tomé', 'afghan', 'bermudian', 'sandwich', 'kyrgyzstan', 'korean', 'herzegovinians', 'new', 'ecuadorian', 'somaliland', 'mauritius', 'nauru', 'saudi', 'colombian', 'cook', 'grenada', 'persian', 'guatemalan', 'nepali', 'cambodian', 'malawian', 'saban', 'tongan', 'england', 'kyrgyzstanis', 'irishman', 'guinean', 'malaysian', 'benin', 'andorran', 'kazakhstani', 'tonga', 'tunisian', 'tokelau', 'hungarian', 'turkmenistan', 'slovenian', 'haiti', 'jamaica', 'kazakhstan', 'falkland', 'kosovars', 'arubans', 'portugal', 'vietnamese', 'sierra', 'turkey', 'seychellois', 'samoa', 'bahrain', 'vincentians', 'belgian', 'sweden', 'sahraouis', '&', 'gambian', 'konger', 'futunan', 'malawi', 'ghanaian', 'thailand', 'emiratis', 'coco', 'kittitian', 'jordanian', 'nevisians', 'swede', 'french', 'irishnorthern', 'formosan', 'islanderssouth', 'rica', 'armenia', 'kazakh', 'briton', 'tokelauans', 'martin', 'guernseywomen', 'namibia', 'ossetia', 'comoros', 'ethiopian', 'gibraltar', 'timor-leste', 'ricans', 'india', 'marino', 'china', 'cambodia', 'somalilanders', 'angolan', 'cameroonian', 'czech', 'kirgizkirghiz', 'antigua', 'iceland', 'maldives', 'antarctica', 'bahamian', 'montenegrins', 'samoan', 'djibouti', 'great', 'uzbekistanis', 'lithuanian', 'laolaotian', 'honduran', 'southern', 'barbadian', 'guam', 'martinican', 'são', 'burkina', 
                            'city', 'ramadan', 'fiji', 'hungary', 'tongan', 'kittitians', 'gabonaise', 'philippine', 'papua', 'cantonesehong', 'belizeans', 'curacaoan', 'democratic', 'of', 'bruneian', 'finnish', 'namibian', 'icelandic', 'qatari', 'polynesian', 'mahorans', 'serbsserbians', 'guamanian', 'alanders', 'trinidadian', 'libyan', 'turk', 'luxembourgish', 'saudisaudi', 'guiana', 'swiss', 'angola', 'fijian', 'cuban', 'bosnia', 'brunei', 'cambodian', 'niger', 'guinean', 'tajikistanis', 'biot', 'paraguay', 'futunans', 'anguillan', 'egyptian', 'lithuanian', 'zealander', 'verde', 'eustatiusstatian', 'bermudan', 'chilean', 'sahara', 'croatia', 'belizean', 'european', 'nicaraguan', 'malian', 'réunion', 'bermudan', 'guyana', 'kuwait', 'albanian', 'moldovans', 'colombia', 'gabon', 'barbudans', 'republic', 'norwegian', 'slovak', 'togolese', 'equatorial', 'spanish', 'yemeni', 'italian', 'scot', 'bonairean', 'beninois', 'lanka', 'brazilian', 'azerbaijan', 'barthélemois', 'suriname', 'frenchman', 'bangladesh', 'mauritanian', 'eritrean', 'african', 'curacao', 'islandsouth', 'taiwanese', 'hong', 'saint-pierrais', 'surinamers', 'dominican', 'cabo', 'chadian', 'japanese', 'caymanians', 'filipinas', 'ivory', 'lankan', 'greek', 'tobago', 'kitts', 'uruguayan', 'algeria', 'emirian', 'leone', 'mozambican', 'romania', 'nigerian', 'formosan', 'ocean', 'azerbaijani', 'saharan', 'malaysian', 'martiniquaises', 'guadeloupe', 'welshwomen', 'liechtensteiner', 'antarcticans', 'saint-pierraissaint-pierraises', 'canadian', 'burmese', 'nauruan', 'bhutanese', 'comorian', 'gambian', 'sammarinesemsão', 'brazil', 'mexican', 'argentina', 'uzbek', 'gambia', 'armenian', 'niuean', 'kiribati', 'tokelauan', 'jersey', 'kuwaiti', 'vatican', 'verdean', 'liberia', 'monégasquesmonacans', 'myanmar', 'iranian', 'egypt', 'nigerien', 'niue', 'saint-martinoise', 'ivorians', 'bulgarian', 
                            'mcdonald', 'gibraltarian', 'tuvaluan', 'ecuadorean', 'islander', 'saudissaudi', 'slovakians', 'moroccan', 'pakistan', 'mozambique', 'guadeloupians', 'kenya', 'burundian', 'algerian', 'vaticanians', 'ghana', 'saint', 'hellene', 'barthélemoises', 
                            'equatoguinean', 'cunha', 'singapore', 'belarusian', 'malian', 'austrian', 'slovenian', 'swaziswati', 'luxembourger', 'monégasque', 'icelander', 'arabia', 'syrian', 'american', 'palestinian', 'colombian', 'ecuador', 'omani', 'paraguayan', 'dutchman', 'hongkongers', 'caledonian', 'latvian', 'mongolian', 'pakistani', 'palau', 'lesotho', 'somalian', 'barbadian', 'austria', 'greenlanders', 'turkish', 'nicaragua', 'tunisia', 'trinidadiantobagonian', 'indian', 'seychelles', 'irishwoman', 'kenyan', 'bahamas', 'beninese', 'spain', 'ossetian', 'panamanian', 'seychellois', 'latviansletts', 'niueans', 'solomon', 'zanzibar', 'african', 'northern', 'belarus', 'southeast', 'tobagonian', 'bonaire', 'mexico', 'barbuda', 'tunisian', 'frenchwoman', 'uzbekistani', 'salvadoran', 'nevis', 'iran', 'malawian', 'rwandan', 'ukrainian', 'salvadoran', 'palestine', 'united', 'tuvaluans', 'afghanistan', 'tajik', 'bulgarian', 'bolivian', 'polynesia', 'iraqi', 'turkmen', 'ascension', 'uk', 'arab', 'greece', 'zambia', 'guinea-bissau', 'kosovo', 'cameroonian', 'nicaraguan', 'maarten', 'dutch', 'antarctic', 'abkhazian', 'guianese', 'macedonian', 'swedish', 'futuna', 'abkhazia', 'albanian', 'guernsey', 'american', 'mexican', 'somalia', 'martiniquais', 'azerbaijani', 'guatemalan', 'somali', 'príncipe', 'belgium', 'slovak', 'jamaican', 'mauritanian', 'dutchwomen', 'emirians', 'bolivian', 'english', 'switzerland', 'bermuda', 'botswana', 'faroese', 'kingdom', 'ghanaians', 'bulgaria', 'statians', 'papuan', 'central', 'bolivia', 'abkhazabkhazian', 'mauritania', 'réunionnaises', 'korea', 'honduras', 'norway', 'austrian', 'burkinabe', 'argentine', 'ugandan', 'zambian', 'haitian', 'anguillan', 'magyar', 'helena,', 'montenegrin', 'persian', 'chilean', 'grenadine', 'costa', 'scotsman', 'estonian', 'irish', 'barundi', 'irishirishmen', 'salvadorean', 'fijian', 
                            'antiguan', 'libya', 'marianan', 'southwest', 'ni-vanuatu', 'maldivian', 'macedonia', 'panama', 'kenyan', 'filipino', 'kuwaiti', 'east', 'wale', 'netherlands', 'hungarian', 'ethiopia', 'man', 'rwandan', 'montserratian', 'faso', 'lithuania', 'paraguayan', 'scotland', 'kyrgyz', 'greekhellenic', 'chadian', 'albania', 'lucia', 'finland', 'vanuatu', 'grenadian', 'zanzibaris', 'aruban', 'tristan', 'nepalisnepalese', 'guernseymen', 'somalilander', 'libyan', 'zanzibari', 'comorans', 'indonesian', 'kirghiz', 'emirati', 'asia', 'argentinian', 'azeri', 'jordanian', 'european', 'statesu.s.', 'the', 'sint', 'israel', 'kyrgyzstani', 'sudan', 'greenland', 'indonesia', 'malaysia', 'oman', 'rican', 'saint-martinoissaint-martinoises', 'togo', 'slovene', 'sri', 'poland', 'malta', 'singaporean', 'martinique', 'mongolia', 'réunionnais', 'samoan', 'cuban', 'salvadorian', 'isle', 'japan', 'saba', 'liberian', 'djiboutian', 'mozambican', 'grenadian', 'israeli', 'filipino', 'montserratian', 'australian', 'barthélemy', 'serbia', 'tajikistani', 'russian', 'gabonese', 'monacan', 'tajikistan', 'mauritian', 'america', 'palauans', 'arabian', 'uzbekistan', 'lebanese', 'nigerian', 'nepalese', 'german', 'bosnian', 'croatian', 'pitcairn', 'djiboutian', 'angolan', 'tanzanian', 'burkinabé', 'welsh', 'state', 'armenian', 'tuvalu', 'papuan', 'sahrawis', 'eswatini', 'south', 'lebanon', 'scotswoman', 'leoneans', 'africa', 'cyprus', 'serbian', 'georgian', 'italy', 'argentinian', 'verdeans', 'polynesian', 'indian', 'caledonians', 'batswana', 'slovakia', 'andorran', 'kosovar', 'finn', 'samoansandorra', 'bangladeshi', 'iraq', 'zimbabwean', 'the', 'territory', 'spaniard', 'georgia', 'haitian', 'polish', 'moroccan', 'salvador', 'coast', 'moldova', 'western', 'svalbard', 'jersianjèrriais', 'syria', 'afghan', 'macau', 'chinese', 'peruvian', 'toméan', 'asian', 'u.s.', 'eritrea', 'maltese', 'sahrawiwestern', 'montserrat', 'bahamian', 'germany', 'heard', 'nauruan', 'welshman', 'yemen', 
                            'palestinian', 'el', 'netherlander', 'romanian', 'croatianscroats', 'caymanian', 'vincent', 'korean', 'myanma', 'sahrawian', 'italian', 'georgian', 'micronesia', 'cuba', 'bangladeshi', 'laoslaotians', 'slovene', 'cameroon', 'namibian', 'kongese', 'russia', 'bermudian', 'mariana', 'bouvet', 'kyrgyzkirgiz', 'singaporean', 'lettish', 'romanian', 'yemeni', 'malagasy', 'island', 'russian', 'britain', 'palauan', 'comoran', 'kong', 'mahoran', 'jerseymen', 'taiwan', 'manx', 'i-kiribati', 'basotho', 'macanese', 'syrian', 'herzegovina', 'honduran', 'caledonia', 'scottish', 'zimbabwe', 'nepal', 'uganda', 'leonean', 'bahraini', 'uruguayan', 'marshallese', 'bosnians', 'morocco', 'jerseywomen', 'vanuatuan', 'guamanians', 'uruguay', 'vietnam', 'faroe', 'dominican', 'sammarinese', 'guinea', 'argentine', 'barbados', 'lao', 'dominica', 'antiguan', 'chad', 'peruvian', 'nigeria', 'aland', 'belgian', 'moldovan', 'norwegian', 'australia', 'sahrawi', 'mauritian', 'micronesians', 'lucian', 'cypriot', 'motswana', 'maarteners', 'kazakhstani', 'canadian', 'north', 'emirate', 'uzbek', 'marshall', 'island', 'lucians', 
                            'ossetians', 'ecuadorian', 'herzegovinian', 'southwestern', 'saharan', 'swazi', 'trinidad', 'azeri', 'san', 'malinese', 'peru', 'belarusian', 'german', 'montenegro', 'zimbabwean', 'danish', 'maldivian', 'miquelonnais', 'brazilian', 'cajun', 'egyptian', 'zambian', 'mali', 'bhutan', 'iranian', 'guyanese', 'bissau-guineans', 'burundian']
    
    other_stop_words = ['high in...', 'bread machine', 'small appliance', 'yam/sweet potato', 'potato', 'onion', 'lemon', 'pork', 'whole chicken', 'chicken', 'poultry', 'lamb/sheep', 'green', 'pineapple', 'tropical fruit', 'potato', 'duck', 'raspberry', 'berry', 'apple', 'pear', 'pepper', 'long grain rice', 'black bean', 'bean', 'refrigerator', 'microwave', 'freezer', 'oven', 'stove top', 'free of...', 'gelatin', 'goose', 'grain', 'grape', 'gumbo', 'halibut', 'ham', 'lentil', 'lime', 'liver', 'lobster', 'long grain rice', 'cheese',
                        'meatball', 'meatloaf', 'medium grain rice', 'melon', 'mixer', 'moose', 'mussel', 'nut', 'orange', 'orange roughy', 'oyster', 'papaya', 'pasta shell', 'peanut butter', 'penne', 'perch', 'pheasant', 'plum', 'pressure cooker', 'quail', 'rabbit', 'rice', 'roast beef', 'scone', 'short grain rice', 'small appliance', 'soy/tofu', 'spaghetti', 'spinach', 'spread', 'squid', 'strawberry', 'tart', 'thigh & leg', 'tilapia', 'trout', 'tuna', 'turkey breast', 'welsh', 'white rice', 'whitefish', 'whole', 'whole turkey', 'yam/sweet'
                        'bass', 'bear', 'beef liver', 'beef organ meat', 'breast', 'brown rice', 'catfish', 'cauliflower', 'cheese', 'cheesecake', 'cherry', 'chocolate chip cooky', 'chowder', 'clear soup', 'coconut', 'crab', 'crawfish', 'cookie & brownie',  'corn']
    
    #check if the category passed is a list or not
    if isinstance(category, list):
        keysw = category
        
    else:
        keysw = ast.literal_eval(category)    

    translator = str.maketrans("", "", string.punctuation)
    lemmatizer = WordNetLemmatizer()
    category_words = []
    
    for i in keysw:
        i.translate(translator)
        # We split up with hyphens as well as spaces
        items = re.split(" |-", i)
        # Get rid of words containing non alphabet letters
        #items = [word for word in items if word.isalpha()]
        # Turn everything to lowercase
        items = [word.lower() for word in items]
        # remove accents
        items = [unidecode.unidecode(word) for word in items]
        # Lemmatize words so we can compare words to measuring words
        items = [lemmatizer.lemmatize(word) for word in items]
        # Gets rid of measuring words/phrases, e.g. heaped teaspoon
        #items = [word for word in items if word not in other_stop_words]
        # Get rid of common easy words
        #items = [word for word in items if word not in category_no_words]
        
        if items:
            category_words.append(" ".join(items))
            category_words = [word.strip() for word in category_words]
            category_words = [word for word in category_words if word not in other_stop_words]
    return category_words

#print(' < 60 min'.strip())
#test = data.Keywords_parsed.apply(category_parser)
#for i in test:
#    print(i)

#data = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\updated_Categories.csv')
#tester = data.Keywords_parsed.apply(category_parser)
#recipe_df = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\updated_Categories.csv')
#recipe_df["parsed_categorylist_keywords"] = tester
#df = recipe_df[["RecipeId","Name","CookTime","RecipeCategory","Keywords","RecipeIngredientParts","Calories","FatContent","CholesterolContent","SodiumContent","SugarContent","ProteinContent","RecipeInstructions","Keywords_parsed", "parsed_categorylist_keywords"]]
#df = recipe_df.dropna()

#df.to_csv(r'parsed_Categories', index=False)
#print("done adding parsed keywords.")

def category_fixer(keywords):
    
    desserts = ['Cakes', 'Cupcakes', 'Brownies', 'Muffins', 'Cheesecakes', 'Cookie','Cookies', 'Custard', 'Fudge', 'Pie', 'Puddings', 'Cobblers', 'Macarons', 'Tarts', 'Fruit', 'Fruit Salad', 'Gelatin', 'Biscuits', 'Chocolate', 'Candy', 'Donuts', 'Sweet', 'Crepes', 'Dessert', 'Mousse', 'Parfaits', 'Pie', 'Candy', 'Gelatin', 'Sourdough Breads', 'Yeast Breads', 'Chocolate Chip Cookies', 'Clear Soup', 'Peanut Butter Pie', 'Bread Pudding', 'Lemon Cake', 'Apple Pie', 'Fruit', 'Ice Cream', 'Coconut Cream Pie', 'Oatmeal', 'Mashed Potatoes' ]

    savory = ['Chicken Breast', 'Soy/Tofu', 'Vegetable', 'Pie', 'Chicken', 'Southwestern U.S.', 'Stew', 'Black Beans', 'Lactose Free', 'Weeknight', 'Yeast Breads', 'Whole Chicken', 'High Protein', 'Sauces', 'High In...', 'Brazilian', 'Breakfast', 'Breads', 'Brown Rice', 'Pork', 'Low Protein', 'Potato', 'Cheese', 'Meat', 'Lamb/Sheep', 'Spaghetti', 'Very Low Carbs', 'Pineapple', 'Low Cholesterol', 'Quick Breads', 'Sourdough Breads', 'Curries', 'Chicken Livers', 'Savory Pies', 'Free Of...', 'Coconut', 'Lunch/Snacks', 'Poultry', 'Steak', 'Healthy', 'Lobster', 'Halibut', 'Broil/Grill', 'Crab', 'Pears', 'Cauliflower', 'Candy', 'White Rice', 'Chowders', 'Tex Mex', 'Bass', 'Fruit', 'Hungarian', 'German', 'European', 'New Zealand', 'Chicken Thigh & Leg', 
                'Indonesian', 'Greek', 'Corn', 'Lentil', 'Summer', 'Long Grain Rice', 'Southwest Asia (middle East)', 'Oranges', 'Tuna', 'Citrus', 'Berries', 'Peppers', 'Asian', 'Mexican', 'Raspberries', 'Beans', 'Beef Organ Meats', 'Short Grain Rice', 'Manicotti', 'One Dish Meal', 'Onions', 'Cajun', 'Oven', '< 15 Mins', 'Rice', 'Apple', 'Gelatin', 'Clear Soup', 'Veal', 'Spanish', 'Roast', 'Shakes', 'Orange Roughy', 'Chutneys', 'Melons', '< 60 Mins', 'Mussels', 'Colombian', 'Microwave', 'Roast Beef', 'Perch', 'Gumbo', 'Turkish', 'For Large Groups', 'Christmas', 'Spreads', 'Chinese', '< 30 Mins', 'Meatloaf', 'Winter', 'Trout', 'Smoothies', 'Yam/Sweet Potato', 'Meatballs', 'Whole Duck', 'Strawberry', 'Caribbean', 'Scandinavian', 'Greens', 'Ham', 'Stocks', 'Savory', 'Crawfish', 'Vietnamese', 'Catfish', 'Thai', 'Deer', 
                'Wild Game', 'Pheasant', 'Japanese', 'Canadian', 'Salad Dressings', 'Spring', 'Vegan', 'Grains', 'Collard Greens', 'Tilapia', 'Penne', 'Refrigerator', 'Potluck', 'Spicy', 'Moroccan', 'Pressure Cooker', 'Papaya', 'Kid Friendly', 'Korean', 'Whole Turkey', 'Pasta Shells', 'Plums', 'Danish', 'Lebanese', 'Creole', 'Medium Grain Rice', 'Spinach', 'Squid', 'Homeopathy/Remedies', 'Thanksgiving', 'Moose', 'Native American', 'African', 'High Fiber', 'Kosher', 'Norwegian', 'Household Cleaner', 'Ethiopian', 'Polish', 'Belgian', 'Rabbit', 'Swedish', 'Goose', 'Austrian', 'Australian', 'Swiss', 'Pennsylvania Dutch', 'Elk', 'Bear', 'Mahi Mahi', 'Duck Breasts', 'Scottish', 'Quail', 'Tempeh', 'Cuban', 'Turkey Breasts', 
                'Cantonese', 'Peanut Butter', 'Hawaiian', 'Bath/Beauty', 'Szechuan', 'Portuguese', 'Summer Dip', 'Costa Rican', 'Duck', 'Dutch', 'Filipino', 'Welsh', 'Camping', 'Russian', 'St. Patricks Day', 'Pot Pie', 'Polynesian', 'Cherries', 'Egyptian', 'Chard', 'Lime', 'Lemon', 'Kiwifruit', 'Mango', 'No Shell Fish', 'Whitefish', 'Brunch', 'Malaysian', 'Toddler Friendly', 'Octopus', 'Nigerian', 'Mixer', 'Venezuelan', 'Bread Machine', 'South African', 'Finnish', 'No Cook', 'South American', 'Nepalese', 'Palestinian', 'Egg Free', 'Sweet', 'Czech', 'Icelandic', 'Beginner Cook', 'Hunan', 'Halloween', 'Avocado', 'Iraqi', '< 4 Hours', 'Pakistani', 'Chocolate Chip Cookies', 'Canning', 'Stove Top', 'Puerto Rican', 'Ecuadorean', 'Hanukkah', 'Chilean', 'Breakfast Eggs', 'Cambodian', 'Honduran', 'Peruvian', 'Nuts', 'Peanut Butter Pie', 'Deep Fried', 'Ham And Bean Soup', 'Bread Pudding', 'Margarita', 'Bean Soup', 'Turkey Gravy', 'Spaghetti Sauce', 'Freezer', 'Lemon Cake', 'Black Bean Soup', 'Somalian', 'Main Dish Casseroles', 'Pot Roast', 'Potato Soup', 'Broccoli Soup', 'Apple Pie', 'Oatmeal', 'Soups Crock Pot', 'Roast Beef Crock Pot', 'Chicken Crock Pot', 'Breakfast Casseroles', 'Grapes', 'Macaroni And Cheese', 'Mashed Potatoes', 'Desserts Fruit', 'Birthday', 'Pumpkin', 'Ice Cream', 'Artichoke', 'Indian', 'Baking', 'Beef Liver', 'Memorial Day', 'Sudanese', 'Coconut Cream Pie', 'Easy', 'Steam', 'Dehydrator', 'Mongolian', 'Small Appliance' ]
    #indices = pd.Series(data.index, index=data['RecipeCategory']).drop_duplicates
    #print(indices)
    
    x = 0
    addedcategory = []
     
    for i in keywords:
        #check for desserts and make sure keywords has dessert in it.
        checkwords = ast.literal_eval(data['Keywords'][x])
        if i in desserts:
            if not('Desserts' in checkwords) or not('Meat' in checkwords and 'Desserts' in checkwords):
                checkwords.append('Dessert')
        #check for savory food and make sure keywords has savoury in it.
        elif i in savory:
            if not('Desserts' in checkwords and 'Savory' in checkwords):
                checkwords.append('Savory')
        #checks if the category word was in the keywords or not 
        if not(i in checkwords):
            checkwords.append(i)

        if checkwords:
            addedcategory.append(checkwords)
        x = x+1
    return addedcategory


#data = pd.read_csv('app\parsed_recipesv4.csv')
#test = data.RecipeCategory.apply(category_fixer)
#lart = [1,2,3,4,5]
#test = data.RecipeCategory.values
#tr = data['RecipeCategory']
#tester = category_fixer(tr)

#recipe_df = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\parsed_recipesv4.csv')
#recipe_df["Keywords_parsed"] = tester
#df = recipe_df[["RecipeId","Name","CookTime","RecipeCategory","Keywords","RecipeIngredientParts","Calories","FatContent","CholesterolContent","SodiumContent","SugarContent","ProteinContent","RecipeInstructions","Keywords_parsed"]]
#df = recipe_df.dropna()

#df.to_csv(r'updated_Categories', index=False)


#if __name__ == "__main__":
#    recipe_df = pd.read_csv(r'app\csvfiles\parsed_recipesv4.csv')
#    recipe_df["ingredients_parsed"] = recipe_df["RecipeIngredientParts"].apply(
#        lambda x: ingredient_parser(x)
#    )
#    df = recipe_df[["RecipeId","Name","CookTime","RecipeCategory","Keywords","RecipeIngredientParts","Calories","FatContent","CholesterolContent","SodiumContent","SugarContent","ProteinContent","RecipeInstructions","ingredients_parsed"]]
#    df = recipe_df.dropna()

    # remove - Allrecipes.com from end of every recipe title
    #m = df.recipe_name.str.endswith("Recipe - Allrecipes.com")
    #df["recipe_name"].loc[m] = df.recipe_name.loc[m].str[:-23]
#    df.to_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles', index=False)

    # vocabulary = nltk.FreqDist()
    # for ingredients in recipe_df['ingredients']:
    #     ingredients = ingredients.split()
    #     vocabulary.update(ingredients)

    # for word, frequency in vocabulary.most_common(200):
    #     print(f'{word};{frequency}')
    # fdist = nltk.FreqDist(ingredients)

    # common_words = []
    # for word, _ in vocabulary.most_common(250):
    #     common_words.append(word)
    # print(common_words)


def addparsedddoctocsv(rec, input=0):
    
    with open('app\csvfiles\parseddocuments.csv', 'w', encoding='UTF8', newline='') as file:
    
        writer = csv.writer(file)

        writer.writerow(['RecipeId','Name','CookTime','RecipeCategory','Keywords_parsed','RecipeIngredientParts','RecipeInstructions','parsed_categorylist_keywords','ingredients_parsed'])
        
        df_recipes = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\parsed_Categories.csv')
        dff_recipes = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\parsed_ingredients.csv')
        
        rows = []
        print("started adding the docs to the file")
        for i in len(rec):
            rows.clear()
            recipeid = df_recipes["RecipeId"][i]
            name = df_recipes["Name"][i]
            cooktime = df_recipes["CookTime"][i]
            categories = df_recipes["RecipeCategory"][i]
            Keywords_parsed = df_recipes["Keywords_parsed"][i]
            ingredients = df_recipes["RecipeIngredientParts"][i]
            ingredientsparsed = dff_recipes["ingredients_parsed"][i]
            instructions = df_recipes["RecipeInstructions"][i]
            parsedcatergorylist = df_recipes["parsed_categorylist_keywords"][i]

            #check = all(u in parsed_catergoywords for u in input)

            
            rows.append([recipeid, name, cooktime, categories, Keywords_parsed, ingredients, instructions, parsedcatergorylist, ingredientsparsed])

            #t = ', '.join(map(lambda x: '"'+ str(x) + '"', rows[0]))
            
            writer.writerow(rows[0])

    file.close()
    print("added to csv successfully")    
    return 0


#data = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\updated_Categories.csv')
#tester = addparseddoctocsv(data["Keywords_parsed"])