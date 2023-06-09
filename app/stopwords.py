import nltk
import numpy as np
import pandas as pd
import ast
from nltk.stem import WordNetLemmatizer
import pandas as pd
import numpy as np
import ast
import unidecode

from sklearn.metrics.pairwise import cosine_similarity
#from words_parser import ingredient_parser
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import defaultdict
from gensim.models import Word2Vec
"""
This file was created to find stop words and create the lists used to parsed the data.
This file was also used as a testing area for snippets of code used/ not used in the final code.
"""


vocabulary = nltk.FreqDist()
vocab = nltk.FreqDist.clear
vocab = nltk.FreqDist()
# This was done once I had already preprocessed the ingredients
data = pd.read_csv(r'app\csvfiles\parsed_recipesv4.csv')
def get_and_sort_corpus(data):
    corpus_sorted = []
    for doc in data:
        print(data)
        corpus_sorted.append(doc)
    return corpus_sorted
#country_list = " American  Asia  Cajun  Ramadan  Native  Southwest  Southeast  Asian  Asia  Abkhazia	AbkhazAbkhazian	Abkhazians Afghanistan	Afghan	Afghans Aland	Åland Island	Alanders Albania	Albanian	Albanians Algeria	Algerian	Algerians American Samoa American Samoan American SamoansAndorra	Andorran	Andorrans Angola	Angolan	Angolans Anguilla	Anguillan	Anguillans Antarctica	Antarctic	Antarctic residents  Antarcticans Antigua  Barbuda	Antiguan Barbudan	Antiguans Barbudans Argentina	Argentine Argentinian	Argentines Argentinians Armenia	Armenian	Armenians Aruba	Aruban	Arubans Australia	Australian	Australians Austria	Austrian	Austrians Azerbaijan	Azerbaijani Azeri	Azerbaijanis  Azeris The Bahamas	Bahamian	Bahamians Bahrain	Bahraini	Bahrainis Bangladesh	Bangladeshi	Bangladeshis Barbados	Barbadian	Barbadians Belarus	Belarusian	Belarusians Belgium	Belgian	Belgians Belize	Belizean	Belizeans Benin	Beninese Beninois	Beninese Beninois Bermuda	Bermudian Bermudan	Bermudians Bermudans Bhutan	Bhutanese	Bhutanese Bolivia	Bolivian	Bolivians Bonaire	Bonaire Bonairean	Bonaire Dutch Bosnia  Herzegovina	Bosnian Herzegovinian	Bosnians Herzegovinians Botswana	Botswana	Batswana Motswana Bouvet Island	Bouvet Island	Bouvet Islanders Brazil	Brazilian	Brazilians British Indian Ocean Territory	BIOT	British Brunei	Bruneian	Bruneians Bulgaria	Bulgarian	Bulgarians Burkina Faso	Burkinabe	Burkinabe Burkinabé Burundi	Burundian	Burundians Barundi Cabo Verde	Cabo Verdean	Cabo Verdeans Cambodia	Cambodian	Cambodians Cameroon	Cameroonian	Cameroonians Canada	Canadian	Canadians Cayman Islands	Caymanian	Caymanians Central African Republic	Central African	Central Africans Chad	Chadian	Chadians Chile	Chilean	Chileans China	Chinese	Chinese Christmas Island	Christmas Island	Christmas Islanders Cocos  Islands	Cocos Island	Cocos Islanders Colombia	Colombian	Colombians Comoros	Comoran Comorian	Comorans Comorians Democratic Republic of the Congo	Congolese	Congolese Republic of the Congo	Congolese	Congolese Cook Islands	Cook Island	Cook Islanders Costa Rica	Costa Rican	Costa Ricans Croatia	Croatian	CroatiansCroats Cuba	Cuban	Cubans Curacao	Curacaoan	Curacaoans Cyprus	Cypriot	Cypriots Czech Republic	Czech	Czechs Denmark	Danish	Danes Djibouti	Djiboutian	Djiboutians Dominica	Dominican	Dominicans Dominican Republic	Dominican	Dominicans East Timor	Timorese	Timorese Ecuador	Ecuadorian	Ecuadorians Egypt	Egyptian	Egyptians El Salvador	Salvadoran	Salvadorans Salvadorians Salvadoreans England	English	English   Equatorial Guinea	Equatorial Guinean Equatoguinean	Equatorial Guineans Equatoguineans Eritrea	Eritrean	Eritreans Estonia	Estonian	Estonians Eswatini	SwaziSwati	Swazis Ethiopia	Ethiopian	Ethiopians Habesha European Union	European	Europeans Falkland Islands	Falkland Island	Falkland Islanders Faroe Islands	Faroese	Faroese Fiji	Fijian	Fijians Finland	Finnish	Finns France	French	French Frenchmen Frenchwomen French Guiana	French Guianese	French Guianese French Polynesia	French Polynesian	French Polynesians French Southern Territories	French Southern Territories	French Gabon	Gabonese	Gabonese Gabonaise The Gambia	Gambian	Gambians Georgia	Georgian	Georgians Germany	German	Germans Ghana	Ghanaian	Ghanaians Gibraltar	Gibraltar	Gibraltarians Greece	GreekHellenic	Greeks Hellenes Greenland	Greenland	Greenlanders Grenada	Grenadian	Grenadians Guadeloupe	Guadeloupe	Guadeloupians Guadeloupeans Guam	Guamanian	Guamanians Guatemala	Guatemalan	Guatemalans Guernsey	Guernsey	Guernseymen  Guernseywomen Guinea	Guinean	Guineans Guinea-Bissau	Bissau-Guinean	Bissau-Guineans Guyana	Guyanese	Guyanese Haiti	Haitian	Haitians Heard Island  McDonald Islands	Heard Island McDonald Island	Heard Islanders McDonald Islanders Honduras	Honduran	Hondurans Hong Kong	Hong Kong CantoneseHong Konger	Hongkongers Hong Kongese Hungary	Hungarian Magyar	Hungarians Magyars Iceland	Icelandic	Icelanders India	Indian	Indians Indonesia	Indonesian	Indonesians Iran	Iranian Persian	Iranians Persians Iraq	Iraqi	Iraqis Ireland	Irish	IrishIrishmen  Irishwomen Isle of Man	Manx	Manx Israel	IsraeliIsraelite	Israelis Italy	Italian	Italians Ivory Coast	Ivorian	Ivorians Jamaica	Jamaican	Jamaicans Jan Mayen	Jan Mayen	Jan Mayen residents Japan	Japanese	Japanese Jersey	Jersey	Jerseymen  Jerseywomen JersianJèrriais Jordan	Jordanian	Jordanians Kazakhstan	Kazakhstani Kazakh	Kazakhstanis Kazakhs Kenya	Kenyan	Kenyans Kiribati	Kiribati	I-Kiribati North Korea	North Korean	KoreansNorth Koreans South Korea	South Korean	KoreansSouth Koreans Kosovo	Kosovar Kosovan	Kosovars Kuwait	Kuwaiti	Kuwaitis Kyrgyzstan	Kyrgyzstani KyrgyzKirgiz Kirghiz	Kyrgyzstanis Kyrgyz KirgizKirghiz Laos	LaoLaotian	LaosLaotians Latvia	Latvian Lettish	LatviansLetts Lebanon	Lebanese	Lebanese Lesotho	Basotho	Basotho Liberia	Liberian	Liberians Libya	Libyan	Libyans Liechtenstein	Liechtensteiner	Liechtensteiners Lithuania	Lithuanian	Lithuanians Luxembourg	Luxembourg Luxembourgish	Luxembourgers Macau	Macanese	Macanese Madagascar	Malagasy Madagascan	Malagasy Madagascans Malawi	Malawian	Malawians Malaysia	Malaysian	Malaysians Maldives	Maldivian	Maldivians Mali	Malian Malinese	Malians Malta	Maltese	Maltese Marshall Islands	Marshallese	Marshallese Martinique	Martiniquais Martinican	Martiniquais Martiniquaises Mauritania	Mauritanian	Mauritanians Mauritius	Mauritian	Mauritians Mayotte	Mahoran	Mahorans Mexico	Mexican	Mexicans Micronesia	Micronesian	Micronesians Moldova	Moldovan	Moldovans Monaco	Monégasque Monacan	MonégasquesMonacans Mongolia	Mongolian	MongoliansMongols Montenegro	Montenegrin	Montenegrins Montserrat	Montserratian	Montserratians Morocco	Moroccan	Moroccans Mozambique	Mozambican	Mozambicans Myanmar	Myanma Burmese	Myanmar Namibia	Namibian	Namibians Nauru	Nauruan	Nauruans Nepal	Nepali Nepalese	NepalisNepalese Netherlands	Dutch	Dutch Dutchmen  Dutchwomen Netherlanders New Caledonia	New Caledonian	New Caledonians New Zealand	New Zealand	New Zealanders Nicaragua	Nicaraguan	Nicaraguans Niger	Nigerien	Nigeriens Nigeria	Nigerian	Nigerians Niue	Niuean	Niueans Norfolk Island	Norfolk Island	Norfolk Islanders North Macedonia	Macedonian	Macedonians Northern Ireland	Northern Irish	Northern IrishNorthern Irishmen  Northern Irishwomen Northern Mariana Islands	Northern Marianan	Northern Marianans Norway	Norwegian	Norwegians Oman	Omani	Omanis Pakistan	Pakistani	Pakistanis Palau	Palauan	Palauans Palestine	Palestinian	Palestinians Panama	Panamanian	Panamanians Papua New Guinea	Papua New Guinean Papuan	Papua New Guineans Papuans Paraguay	Paraguayan	Paraguayans Peru	Peruvian	Peruvians Philippines	Filipino Philippine	Filipinos Filipinas Pitcairn Islands	Pitcairn Island	Pitcairn Islanders Poland	Polish	Poles Portugal	Portuguese	Portuguese Puerto Rico	Puerto Rican	Puerto Ricans Qatar	Qatari	Qataris Réunion	Réunionese Réunionnais	Réunionese Réunionnais  Réunionnaises Romania	Romanian	Romanians Russia	Russian	Russians Rwanda	Rwandan	Rwandans Banyarwanda Saba	Saban	Saba Dutch Saint Barthélemy	Barthélemois	Barthélemois Barthélemoises Saint Helena, Ascension  Tristan da Cunha	Saint Helenian	Saint Helenians Saint Kitts  Nevis	Kittitian Nevisian	Kittitians Nevisians Saint Lucia	Saint Lucian	Saint Lucians Saint Martin	Saint-Martinoise	Saint-MartinoisSaint-Martinoises Saint Pierre  Miquelon	Saint-Pierrais Miquelonnais	Saint-PierraisSaint-Pierraises Miquelonnais Miquelonnaises Saint Vincent  the Grenadines	Saint Vincentian Vincentian	Saint Vincentians Vincentians Sahrawi	SahrawiWestern Saharan Sahrawian	Sahrawis Western Saharans Samoa	Samoan	Samoans San Marino	Sammarinese	SammarinesemSão Tomé  Príncipe	São Toméan	São Toméans Saudi Arabia	SaudiSaudi Arabian	SaudisSaudi Arabians Scotland	Scottish	Scots Scotsmen  Scotswomen Senegal	Senegalese	Senegalese Serbia	Serbian	SerbsSerbians Seychelles	Seychellois	Seychellois Seychelloises Sierra Leone	Sierra Leonean	Sierra Leoneans Singapore	Singapore Singaporean	Singaporeans Sint Eustatius	Sint EustatiusStatian	Statians Sint Maarten	Sint Maarten	Sint Maarteners Slovakia	Slovak	Slovaks Slovakians Slovenia	Slovenian Slovene	Slovenes Slovenians Solomon Islands	Solomon Island	Solomon Islanders Somalia	Somali	Somalis Somaliland	Somalilander	Somalilanders South Africa	South African	South Africans South Georgia  the South Sandwich Islands	South Georgia IslandSouth Sandwich Island	South Georgia IslandersSouth Sandwich Islanders South Ossetia	South Ossetian	South Ossetians South Sudan	South Sudanese	South Sudanese Spain	Spanish	Spaniards Sri Lanka	Sri Lankan	Sri Lankans Sudan	Sudanese	Sudanese Suriname	Surinamese	Surinamers Svalbard	Svalbard	Svalbard residents Sweden	Swedish	Swedes Switzerland	Swiss	Swiss Syria	Syrian	Syrians Taiwan	Taiwanese Formosan	Taiwanese Formosans Tajikistan	Tajikistani	Tajikistanis Tajiks Tanzania	Tanzanian	Tanzanians Thailand	Thai	Thai Timor-Leste	Timorese	Timorese Togo	Togolese	Togolese Tokelau	Tokelauan	Tokelauans Tonga	Tongan	Tongans Trinidad  Tobago	TrinidadianTobagonian	Trinidadians Tobagonians Tunisia	Tunisian	Tunisians Turkey	Turkish	Turks Turkmenistan	Turkmen	Turkmens Turks  Caicos Islands	Turks  Caicos Island	Turks  Caicos Islanders Tuvalu	Tuvaluan	Tuvaluans Uganda	Ugandan	Ugandans Ukraine	Ukrainian	Ukrainians United Arab Emirates	Emirati Emirian Emiri	Emiratis Emirians Emiri United Kingdom of Great Britain  Northern Ireland	British United Kingdom UK	Britons British United States of America	American United StatesU.S.	Americans Uruguay	Uruguayan	Uruguayans Uzbekistan	Uzbekistani Uzbek	Uzbekistanis Uzbeks Vanuatu	Ni-Vanuatu Vanuatuan	Ni-Vanuatu Vatican City	Vaticanian	Vaticanians Venezuela	Venezuelan	Venezuelans Vietnam	Vietnamese	Vietnamese British Virgin Islands	British Virgin Island	British Virgin Islanders United States Virgin Islands	U.S. Virgin Island	U.S. Virgin Islanders Wales	Welsh	Welshmen Welshwomen Wallis  Futuna	Wallis  FutunaWallisian Futunan	Wallis  Futuna Islanders Wallisians Futunans Western Sahara	SahrawiSahrawianSahraouian	Sahrawis Sahraouis Yemen Yemeni	Yemenis Zambia	Zambian	Zambians Zanzibar	Zanzibari	Zanzibaris Zimbabwe	Zimbabwean	Zimbabweans"
#country_list = country_list.split()
country_list = ['scandinavian', 'residents', 'madagascans', 'da', 'denmark', 'hawaiian', 'venezuelans', 'bruneian', 'slovenia', 'canada', 'bahrainis', 'caicos', 'native', 'territory', 'curacaoans', 'jordan', 'ethiopian', 'timor', 'nevisian', 'madagascan', 'algerian', 'vaticanian', 'surinamese', 'nigeriens', 'ivorian', 'aruba', 'réunionese', 'toméans', 'virgin', 'mayen', 'congo', 'guadeloupeans', 'kosovan', 'barbudan', 'australian', 'miquelon', 'ireland', 'chile', 'philippines', 'micronesian', 'france', 'marianans', 'israeliisraelite', 'american', 'congolese', 'venezuelan', 'senegal', 'habesha', 'latvia', 'eritrean', 'czech', 'guatemala', 'helenian', 'poles', 'norfolk', 'ukrainians', 'miquelonnaises', 'madagascar', 'burundi', 'estonian', 'z', 'zealand', 'rwanda', 'vincentian', 'qataris', 'emiri', 'futunawallisian', 'somali', 'arabians', 'puerto', 'kazakh', 'pakistani', 'tanzania', 'jamaicans', 'greeks', 'senegalese', 'sahrawisahrawiansahraouian', 'koreanssouth', 'comorians', 'qatar', 'panamanian', 'banyarwanda', 'danes', 'magyar', 'wallis', 'ugandan', 'helenians', 'indonesian', 'british', 'wallisians', 'anguilla', 'luxembourg', 'mayotte', 'portuguese', 'belize', 'cypriots', 'liechtenstein', 'koreansnorth', 'ukraine', 'jan', 'estonia', 'equatoguineans', 'turkmens', 'lankans', 'rico', 'bissau-guinean', 'liechtensteiner', 'omanis', 'pierre', 'sudanese', 'monaco', 'cayman', 'timorese', 'liberians', 'macedonians', 'tanzanians', 'venezuela', 'thai', 'eustatius', 'iraqis', 'mongoliansmongols', 'union', 'tomé', 'afghan', 'bermudian', 'sandwich', 'kyrgyzstan', 'koreans', 'herzegovinians', 'new', 'ecuadorians', 'somaliland', 'mauritius', 'nauru', 'saudi', 'colombian', 'cook', 'grenada', 
'persian', 'guatemalan', 'nepali', 'cambodians', 'malawian', 'saban', 'tongans', 'england', 'kyrgyzstanis', 'irishmen', 'guineans', 'malaysian', 'benin', 'andorran', 'kazakhstani', 'tonga', 'tunisian', 'tokelau', 'hungarian', 'turkmenistan', 'slovenian', 'haiti', 'jamaica', 'kazakhstan', 'falkland', 'kosovars', 'arubans', 'portugal', 'vietnamese', 'sierra', 'turkey', 'seychelloises', 'samoa', 'bahrain', 'vincentians', 'belgian', 'sweden', 'sahraouis', 
'gambian', 'konger', 'futunan', 'malawi', 'ghanaian', 'thailand', 'emiratis', 'cocos', 'kittitian', 'jordanian', 'nevisians', 'swedes', 'french', 'irishnorthern', 'formosan', 'islanderssouth', 'rica', 'armenia', 'kazakhs', 'britons', 'tokelauans', 'martin', 'guernseywomen', 'namibia', 'ossetia', 'comoros', 'ethiopians', 'gibraltar', 'timor-leste', 'ricans', 'india', 'marino', 'china', 'cambodia', 'somalilanders', 'angolans', 'cameroonian', 'czechs', 'kirgizkirghiz', 'antigua', 'iceland', 'maldives', 'antarctica', 'bahamians', 'montenegrins', 'samoans', 'djibouti', 'great', 'uzbekistanis', 'lithuanians', 'laolaotian', 'honduran', 'southern', 'barbadians', 'guam', 'martinican', 'são', 'burkina', 'city', 'ramadan', 'fiji', 'hungary', 'tongan', 'kittitians', 'gabonaise', 'philippine', 'papua', 'cantonesehong', 'belizeans', 'curacaoan', 'democratic', 'of', 'bruneians', 'finnish', 'namibians', 'icelandic', 'qatari', 'polynesians', 'mahorans', 'serbsserbians', 'guamanian', 'alanders', 'trinidadians', 'libyan', 'turks', 'luxembourgish', 'saudisaudi', 'guiana', 'swiss', 'angola', 'fijians', 'cuban', 'bosnia', 'brunei', 'cambodian', 'niger', 'guinean', 'tajikistanis', 'biot', 'paraguay', 'futunans', 'anguillan', 'egyptians', 'lithuanian', 'zealanders', 'verde', 'eustatiusstatian', 'bermudans', 'chilean', 'sahara', 'croatia', 'belizean', 'europeans', 'nicaraguan', 'malian', 'réunion', 'bermudan', 'guyana', 'kuwait', 'albanians', 'moldovans', 'colombia', 'gabon', 'barbudans', 'republic', 'norwegian', 'slovak', 'togolese', 'equatorial', 'spanish', 'yemenis', 'italians', 'scots', 'bonairean', 'beninois', 'lanka', 'brazilian', 'azerbaijan', 'barthélemois', 'suriname', 'frenchmen', 'bangladesh', 'mauritanians', 'eritreans', 'africans', 'curacao', 'islandsouth', 'taiwanese', 'hong', 'saint-pierrais', 'surinamers', 'dominican', 'cabo', 'chadians', 'japanese', 'caymanians', 'filipinas', 'ivory', 'lankan', 'greek', 'tobago', 'kitts', 'uruguayans', 'algeria', 'emirian', 'leone', 'mozambican', 'romania', 'nigerians', 'formosans', 'ocean', 'azerbaijani', 'saharan', 'malaysians', 'martiniquaises', 'guadeloupe', 'welshwomen', 'liechtensteiners', 'antarcticans', 'saint-pierraissaint-pierraises', 'canadian', 'burmese', 'nauruans', 'bhutanese', 'comorian', 'gambians', 'sammarinesemsão', 'brazil', 'mexican', 'argentina', 'uzbeks', 'gambia', 'armenian', 'niuean', 'kiribati', 'tokelauan', 'jersey', 'kuwaitis', 'vatican', 'verdean', 'liberia', 'monégasquesmonacans', 'myanmar', 'iranian', 'egypt', 'nigerien', 'niue', 'saint-martinoise', 'ivorians', 'bulgarians', 'mcdonald', 'gibraltarians', 'tuvaluan', 'ecuadorean', 'islanders', 'saudissaudi', 'slovakians', 'moroccan', 'pakistan', 'mozambique', 'guadeloupians', 'kenya', 'burundian', 'algerians', 'vaticanians', 'ghana', 'saint', 'hellenes', 'barthélemoises', 'equatoguinean', 'cunha', 'singapore', 'belarusians', 'malians', 'austrian', 'slovenians', 'swaziswati', 'luxembourgers', 'monégasque', 'icelanders', 'arabia', 'syrian', 'americans', 'palestinians', 'colombians', 'ecuador', 'omani', 'paraguayan', 'dutchmen', 'hongkongers', 'caledonian', 'latvian', 'mongolian', 'pakistanis', 'palau', 'lesotho', 'somalian', 'barbadian', 'austria', 'greenlanders', 'turkish', 'nicaragua', 'tunisia', 'trinidadiantobagonian', 'indians', 'seychelles', 'irishwomen', 'kenyans', 'bahamas', 'beninese', 'spain', 'ossetian', 'panamanians', 'seychellois', 'latviansletts', 'niueans', 'solomon', 'zanzibar', 'african', 'northern', 'belarus', 'southeast', 'tobagonians', 'bonaire', 'mexico', 'barbuda', 'tunisians', 'frenchwomen', 'uzbekistani', 'salvadoran', 'nevis', 'iran', 'malawians', 'rwandans', 'ukrainian', 'salvadorans', 'palestine', 'united', 'tuvaluans', 'afghanistan', 'tajiks', 'bulgarian', 'bolivians', 'polynesia', 'iraqi', 'turkmen', 'ascension', 'uk', 'arab', 'greece', 'zambia', 'guinea-bissau', 'kosovo', 'cameroonians', 'nicaraguans', 'maarten', 'dutch', 'antarctic', 'abkhazians', 'guianese', 'macedonian', 'swedish', 'futuna', 'abkhazia', 'albanian', 'guernsey', 'american', 'mexicans', 'somalia', 'martiniquais', 'azerbaijanis', 'guatemalans', 'somalis', 'príncipe', 'belgium', 'slovaks', 'jamaican', 'mauritanian', 'dutchwomen', 'emirians', 'bolivian', 'english', 'switzerland', 'bermuda', 'botswana', 'faroese', 'kingdom', 'ghanaians', 'bulgaria', 'statians', 'papuan', 'central', 'bolivia', 'abkhazabkhazian', 'mauritania', 'réunionnaises', 'korea', 'honduras', 'norway', 'austrians', 'burkinabe', 'argentines', 'ugandans', 'zambian', 'haitian', 'anguillans', 'magyars', 'helena,', 'montenegrin', 'persians', 'chileans', 'grenadines', 'costa', 'scotsmen', 'estonians', 'irish', 'barundi', 'irishirishmen', 'salvadoreans', 'fijian', 'antiguans', 'libya', 'marianan', 'southwest', 'ni-vanuatu', 'maldivians', 'macedonia', 'panama', 'kenyan', 'filipino', 'kuwaiti', 'east', 'wales', 'netherlands', 'hungarians', 'ethiopia', 'man', 'rwandan', 'montserratian', 'faso', 'lithuania', 'paraguayans', 'scotland', 'kyrgyz', 'greekhellenic', 'chadian', 'albania', 'lucia', 'finland', 'vanuatu', 'grenadian', 'zanzibaris', 'aruban', 'tristan', 'nepalisnepalese', 'guernseymen', 'somalilander', 'libyans', 'zanzibari', 'comorans', 'indonesians', 'kirghiz', 'emirati', 'asia', 'argentinians', 'azeri', 'jordanians', 'european', 'statesu.s.', 'the', 'sint', 'israel', 'kyrgyzstani', 'sudan', 'greenland', 'indonesia', 'malaysia', 'oman', 'rican', 'saint-martinoissaint-martinoises', 'togo', 'slovene', 'sri', 'poland', 'malta', 'singaporeans', 'martinique', 'mongolia', 'réunionnais', 'samoan', 'cubans', 'salvadorians', 'isle', 'japan', 'saba', 'liberian', 'djiboutians', 'mozambicans', 'grenadians', 'israelis', 'filipinos', 'montserratians', 'australians', 'barthélemy', 'serbia', 'tajikistani', 'russians', 'gabonese', 'monacan', 'tajikistan', 'mauritian', 'america', 'palauans', 'arabian', 'uzbekistan', 'lebanese', 'nigerian', 'nepalese', 'germans', 'bosnian', 
'croatian', 'pitcairn', 'djiboutian', 'angolan', 'tanzanian', 'burkinabé', 'welsh', 'states', 'armenians', 'tuvalu', 'papuans', 'sahrawis', 'eswatini', 'south', 'lebanon', 'scotswomen', 'leoneans', 'africa', 'cyprus', 'serbian', 'georgian', 'italy', 'argentinian', 'verdeans', 'polynesian', 'indian', 'caledonians', 'batswana', 'slovakia', 'andorrans', 'kosovar', 'finns', 'samoansandorra', 'bangladeshi', 'iraq', 'zimbabwean', 'the', 'territories', 'spaniards', 'georgia', 'haitians', 'polish', 'moroccans', 'salvador', 'coast', 'moldova', 'western', 'svalbard', 'jersianjèrriais', 'syria', 'afghans', 'macau', 'chinese', 'peruvian', 'toméan', 'asian', 'u.s.', 'eritrea', 'maltese', 
'sahrawiwestern', 'montserrat', 'bahamian', 'germany', 'heard', 'nauruan', 'welshmen', 'yemen', 'palestinian', 'el', 'netherlanders', 'romanians', 'croatianscroats', 'caymanian', 'vincent', 'korean', 'myanma', 'sahrawian', 'italian', 'georgians', 'micronesia', 'cuba', 'bangladeshis', 'laoslaotians', 'slovenes', 'cameroon', 'namibian', 'kongese', 'russia', 'bermudians', 'mariana', 'bouvet', 'kyrgyzkirgiz', 'singaporean', 'lettish', 'romanian', 'yemeni', 'malagasy', 'island', 'russian', 'britain', 'palauan', 'comoran', 'kong', 'mahoran', 'jerseymen', 'taiwan', 'manx', 'i-kiribati', 'basotho', 'macanese', 'syrians', 'herzegovina', 'hondurans', 'caledonia', 'scottish', 'zimbabwe', 'nepal', 'uganda', 'leonean', 'bahraini', 'uruguayan', 'marshallese', 'bosnians', 'morocco', 'jerseywomen', 'vanuatuan', 'guamanians', 'uruguay', 'vietnam', 'faroe', 'dominicans', 'christmas', 'sammarinese', 'guinea', 'argentine', 'barbados', 'laos', 'dominica', 'antiguan', 'chad', 'peruvians', 'nigeria', 'aland', 'belgians', 'moldovan', 
'norwegians', 'australia', 'sahrawi', 'mauritians', 'micronesians', 'lucian', 'cypriot', 'motswana', 'maarteners', 'kazakhstanis', 'canadians', 'north', 'emirates', 'uzbek', 'marshall', 'islands', 'lucians', 'ossetians', 'ecuadorian', 'herzegovinian', 'southwestern', 'saharans', 'swazis', 'trinidad', 'azeris', 'san', 'malinese', 'peru', 'belarusian', 'german', 'montenegro', 'zimbabweans', 'danish', 'maldivian', 'miquelonnais', 'brazilians', 'cajun', 'egyptian', 'zambians', 'mali', 'bhutan', 'iranians', 'guyanese', 'bissau-guineans', 'burundians']

categroy_no_words = ['&', '15', '30', '4', '60', '<', 'american', 'a', 'african', 'apple', 'appliance', 
'artichoke', 'asia', 'avocado', 'baked', 'baking', 'bar', 'bass', 'bath/beauty', 'bean', 'beans', 'bear', 'beef', 
'beginner', 'berries', 'beverage', 'beverages', 'birthday', 'black', 'bread', 'breads', 'breakfast', 'breast', 'breasts', 'broil/grill', 'brown', 'brownie', 'brunch', 'butter', 'cabbage', 'camping', 'candy', 'canning', 'cantonese', 'carbs', 'caribbean', 'catfish', 'cauliflower', 'chard', 'cheese', 'cheesecake', 'cherries', 'chicken', 'chip', 'chocolate', 'cholesterol', 'chowders', 'citrus', 'cleaner', 'clear', 'cocktail', 'coconut', 'collard', 'college', 'contest', 'cooker', 'cookie', 'cookies', 'corn', 'crab', 'cranberry', 'crawfish', 'cream', 'creole', 'crock',
'cucumber', 'curries', 'dairy', 'day', 'deep', 'deer', 'dehydrator', 'dessert', 'desserts', 'diabetic', 'dish', 'dressings', 'duck', 'easy', 'egg', 'eggs', 'elbow', 'elk', 'fiber', 'fish', 'food', 'foods', 'for', 'free', 'freezer', 'fried', 'friendly', 'from', 'frozen', 'fruit', 'fruits', 'fry', 'game', 'gelatin', 'goose', 'grain', 'grains', 'grapes', 'greens', 'groups', 'gumbo', 'halibut', 'halloween', 'ham', 'hanukkah', 'healthy', 'high', 'holiday/event', 'homeopathy/remedies', 'hot', 'hours', 'household', 'hunan', 'ice', 'in...', 'inexpensive', 'jellies', 'kid', 'kidney', 'kiwifruit', 'kosher', 'labor', 'lactose', 'lamb/sheep', 'large', 'leg', 'lemon', 'lentil', 'lime', 'liver', 'livers', 'lobster', 'loin', 'long', 'low', 'lunch/snacks', 'machine', 'mahi', 'mango', 'manicotti', 'marinara', 'mashed', 'meal', 'meat', 'meatballs', 'meatloaf', 'meats', 'medium', 'melons', 'memorial', 'mex', 'microwave', 'mins', 'mixer', 'moose', 'mussels', 'navy', 'new', 'no', 'nuts', 'oatmeal', 'octopus', 'of...', 'one', 'onions', 'orange', 'oranges', 'organ', 'oven', 'oysters', 'papaya', 'pasta', 'patricks', 'peanut', 'pears', 'penne', 'pennsylvania', 'peppers', 'perch', 'pheasant', 'pie', 'pies', 'pineapple', 'plums', 'pork', 'pot', 'potato', 'potatoes', 'potluck', 'poultry', 'pressure', 'protein', 'pumpkin', 'punch', 'quail', 'quick', 'rabbit', 'raspberries', 
'refrigerator', 'reynolds', 'rican', 'rice', 'roast', 'roughy', 'salad', 'sandwiches', 'sauce', 'sauces', 'savory', 'scratch', 'served', 'shakes', 'shell', 'shells', 'short', 'slow', 'small', 'smoothies', 'soup', 'soy/tofu', 'spaghetti', 'spicy', 'spinach', 'spreads', 'spring', 'squid', 'st.', 'steak', 'steam', 'stew', 'stews', 'stir', 'stocks', 'stove', 'strawberries', 'strawberry', 'summer', 'sweet', 'szechuan', 'tempeh', 'tex', 'thanksgiving', 'thigh', 'tilapia', 'toddler', 'tomato', 'top', 'tropical', 'trout', 'tuna', 'u.s.', 'veal', 'vegan', 'vegetable', 'very', 'weeknight', 'white', 'whitefish', 'whole', 'wild', 'winter', 'wrap', 'yam/sweet', 'year', 'years', 'yeast', 'zealand', 'middle']

cultur_no_words = ['&', '15', '30', '4', '60', '<', 'a', 'apple', 'appliance', 'artichoke', 'avocado', 'baked', 'baking', 'min', 'hour', 'cook', 'group', 'onion', 'oyster', 'raspberry', 'berry', 'pepper', 'green', 'blue', 'red', 'yellow', 'christmas', 'pear', 'nut', 
                    'bar', 'bass', 'bath/beauty', 'bean', 'beans', 'bear', 'beef', 'beginner', 'berries', 'beverage', 'beverages', 'birthday', 'black', 'bread', 'breads', 'breakfast', 'breast', 'breasts', 'broil/grill', 'brown', 'brownie', 'brunch', 'butter', 'cabbage', 'camping', 'candy', 'canning', 'cantonese', 'carbs', 'catfish', 'cauliflower', 'chard', 'cheese', 'cheesecake', 'cherries', 'chicken', 'chip', 'chocolate', 'cholesterol', 'chowders', 'citrus', 'cleaner', 'clear', 'cocktail', 'coconut', 'collard', 'college', 'contest', 'cooker', 'cookie', 'cookies', 'corn', 'crab', 'cranberry', 'crawfish', 'cream', 'creole', 'crock', 'cucumber', 'curries', 'dairy', 'day', 'deep', 'deer', 'dehydrator', 'dessert', 'desserts', 'diabetic', 'dish', 'dressings', 'duck', 'easy', 'egg', 'eggs', 'elbow', 
                    'elk', 'fiber', 'fish', 'food', 'foods', 'for', 'free', 'freezer', 'fried', 'friendly', 'from', 'frozen', 'fruit', 'fruits', 'fry', 'game', 'gelatin', 'goose', 'grain', 'grains', 'grapes', 'greens', 'groups', 'gumbo', 'halibut', 'halloween', 'ham', 'hanukkah', 'healthy', 'high', 'holiday/event', 'homeopathy/remedies', 'hot', 'hours', 'household', 'hunan', 'ice', 'in...', 'inexpensive', 'jellies', 'kid', 'kidney', 'kiwifruit', 'kosher', 'labor', 'lactose', 'lamb/sheep', 'large', 'leg', 'lemon', 'lentil', 'lime', 'liver', 'livers', 'lobster', 'loin', 'long', 'low', 
                    'lunch/snacks', 'machine', 'mahi', 'mango', 'manicotti', 'marinara', 'mashed', 'meal', 'meat', 'meatballs', 'meatloaf', 'meats', 'medium', 'melons', 'memorial', 'mex', 'microwave', 'mins', 'mixer', 'moose', 'mussels', 'navy', 'no', 'nuts', 'oatmeal', 'octopus', 'of...', 'one', 'onions', 'orange', 'oranges', 'organ', 'oven', 'oysters', 'papaya', 'pasta', 'patricks', 'peanut', 'pears', 'penne', 'pennsylvania', 'peppers', 'perch', 'pheasant', 'pie', 'pies', 'pineapple', 'plums', 'pork', 'pot', 'potato', 'potatoes', 'potluck', 'poultry', 'pressure', 'protein', 'pumpkin', 'punch', 'quail', 'quick', 'rabbit', 'raspberries', 'refrigerator', 'reynolds', 'rice', 'roast', 'roughy', 'salad', 'sandwiches', 'sauce', 'sauces', 'savory', 'scratch', 'served', 'shakes', 'shell', 'shells', 'short', 'slow', 'small', 'smoothies', 'soup', 'soy/tofu', 'spaghetti', 'spicy', 'spinach', 'spreads', 'spring', 'squid', 'st.', 
                    'steak', 'steam', 'stew', 'stews', 'stir', 'stocks', 'stove', 'strawberries', 'strawberry', 'summer', 'sweet', 'szechuan', 'tempeh', 'tex', 'thanksgiving', 'thigh', 'tilapia', 'toddler', 'tomato', 'top', 'tropical', 'trout', 'tuna', 'veal', 'vegan', 'vegetable', 'very', 'weeknight', 'white', 'whitefish', 'whole', 'wild', 'winter', 'wrap', 'yam/sweet', 'year', 'years', 'yeast', 'middle']

vocab_list = ['&', 'middle', '15', '30', '4', '60', '<', 'African', 'American', 'And', 'Apple', 'Appliance', 'Artichoke', 'Asia', 'Asian', 'Australian', 'Austrian', 'Avocado', 'Baking', 'Bar', 'Bass', 'Bath/Beauty', 'Bean', 'Beans', 'Bear', 'Beef', 'Beginner', 'Belgian', 'Berries', 'Beverage', 'Beverages', 'Birthday', 'Black', 'Brazilian', 'Bread', 'Breads', 'Breakfast', 'Breast', 'Breasts', 'Broccoli', 'Broil/Grill', 'Brown', 'Brunch', 'Butter', 'Cajun', 'Cake', 'Cambodian', 'Camping', 'Canadian', 'Candy', 'Canning', 'Cantonese', 'Carbs', 'Caribbean', 'Casseroles', 'Catfish', 'Cauliflower', 'Chard', 'Cheese', 'Cheesecake', 'Cherries', 'Chicken', 'Chilean', 'Chinese', 'Chip', 'Chocolate', 'Cholesterol', 'Chowders', 'Christmas', 'Chutneys', 'Citrus', 'Cleaner', 'Clear', 'Coconut', 'Collard', 'Colombian', 'Cook', 'Cooker', 'Cookie', 'Cookies', 'Corn', 'Costa', 'Crab', 'Crawfish', 'Cream', 'Creole', 'Crock', 'Cuban', 'Curries', 'Czech', 'Danish', 'Day', 'Deep', 'Deer', 'Dehydrator', 'Dessert', 'Desserts', 'Dip', 'Dish', 'Dressings', 'Drop', 'Duck', 'Dutch', 'East)', 'Easy', 'Ecuadorean', 'Egg', 'Eggs', 'Egyptian', 'Elk', 'Ethiopian', 'European', 'Fiber', 'Filipino', 'Finnish', 'Fish', 'For', 'Free', 'Freezer', 'Fried', 'Friendly', 'Frozen', 'Fruit', 'Fruits', 'Game', 'Gelatin', 'German', 'Goose', 'Grain', 'Grains', 'Grapes', 'Gravy', 'Greek', 'Greens', 'Groups', 'Gumbo', 'Halibut', 'Halloween', 'Ham', 'Hanukkah', 'Hawaiian', 'Healthy', 'High', 'Homeopathy/Remedies', 'Honduran', 'Hours', 'Household', 'Hunan', 'Hungarian', 'Ice', 'Icelandic', 'In...', 'Indian', 'Indonesian', 'Iraqi', 'Japanese', 'Jellies', 'Kid', 'Kiwifruit', 'Korean', 'Kosher', 'Lactose', 'Lamb/Sheep', 'Large', 'Lebanese', 'Leg', 'Lemon', 'Lentil', 'Lime', 
                'Liver', 'Livers', 'Lobster', 'Long', 'Low', 'Lunch/Snacks', 'Macaroni', 'Machine', 'Mahi', 
                'Main', 'Malaysian', 'Mango', 'Manicotti', 'Margarita', 'Mashed', 'Meal', 'Meat', 'Meatballs', 'Meatloaf', 'Meats', 'Medium', 'Melons', 'Memorial', 'Mex', 'Mexican', 'Microwave', 'Mins', 'Mixer', 'Mongolian', 'Moose', 'Moroccan', 'Mussels', 'Native', 'Nepalese', 'New', 'Nigerian', 'No', 'Norwegian', 'Nuts', 'Oatmeal', 'Octopus', 'Of...', 'One', 'Onions', 'Orange', 'Oranges', 'Organ', 'Oven', 'Pakistani', 'Palestinian', 'Papaya', 'Pasta', 'Patricks', 'Peanut', 'Pears', 'Penne', 'Pennsylvania', 'Peppers', 'Perch', 'Peruvian', 'Pheasant', 'Pie', 'Pies', 'Pineapple', 'Plums', 'Polish', 'Polynesian', 'Pork', 'Portuguese', 'Pot', 'Potato', 'Potatoes', 'Potluck', 'Poultry', 'Pressure', 'Protein', 'Pudding', 'Puerto', 'Pumpkin', 'Punch', 'Quail', 'Quick', 'Rabbit', 'Raspberries', 'Refrigerator', 'Rican', 'Rice', 'Roast', 'Roughy', 'Russian', 'Salad', 'Sauce', 'Sauces', 'Savory', 'Scandinavian', 'scones', 'Scottish', 'Shakes', 'Shell', 'Shells', 'Short', 'Small', 'Smoothies', 'Somalian', 'Soup', 'Soups', 'Sourdough', 'South', 'Southwest', 'Southwestern', 'Soy/Tofu', 'Spaghetti', 'Spanish', 'Spicy', 'Spinach', 'Spreads', 'Spring', 'Squid', 'St.', 'Steak', 'Steam', 'Stew', 'Stocks', 'Stove', 'Strawberry', 'Sudanese', 'Summer', 'Swedish', 'Sweet', 'Swiss', 'Szechuan', 'Tarts', 'Tempeh', 'Tex', 'Thai', 'Thanksgiving', 'Thigh', 'Tilapia', 'Toddler', 'Top', 'Tropical', 'Trout', 'Tuna', 'Turkey', 'Turkish', 'U.S.', 'Veal', 'Vegan', 'Vegetable', 'Venezuelan', 'Very', 'Vietnamese', 'Weeknight', 'Welsh', 'White', 'Whitefish', 'Whole', 'Wild', 'Winter', 'Yam/Sweet', 'Yeast', 'Zealand']

desserts = ['Cakes', 'Cupcakes', 'Brownies', 'Muffins', 'Cheesecakes', 'Cookie','Cookies', 'Custard', 'Fudge', 'Pie', 'Puddings', 'Cobblers', 'Macarons', 'Tarts', 'Fruit', 'salad', 'Gelatin', 'Biscuits', 'Chocolate', 'candy', 'Donuts', 'Sweet', 'crepes', 'Sweet', 'dessert', 'wines', 'Mousse', 'Parfaits', 'Pie', 'Sauces', 'Candy', 'Breakfast', 'Gelatin', 'Breads', 'Quick Breads', 'Smoothies', 'Shakes', 'One Dish Meal', 'Salad Dressings', 'Chutneys', 'Sourdough Breads', 'Yeast Breads', 'Spreads', 'Chocolate Chip Cookies', 'Clear Soup', 'Peanut Butter Pie', 'Bread Pudding', 'Margarita', 'Savory Pies', 'Stew', 'Lemon Cake', 'Apple Pie', 'Desserts Fruit', 'Ice Cream', 'Coconut Cream Pie', 'Oatmeal', 'Mashed Potatoes' ]

savory = ['Chicken Breast', 'Soy/Tofu', 'Vegetable', 'Pie', 'Chicken', 'Southwestern U.S.', 'Stew', 'Black Beans', 'Lactose Free', 'Weeknight', 'Yeast Breads', 'Whole Chicken', 'High Protein', 'Sauces', 'High In...', 'Brazilian', 'Breakfast', 'Breads', 'Brown Rice', 'Pork', 'Low Protein', 'Potato', 'Cheese', 'Meat', 'Lamb/Sheep', 'Spaghetti', 'Very Low Carbs', 'Pineapple', 'Low Cholesterol', 'Quick Breads', 'Sourdough Breads', 'Curries', 'Chicken Livers', 'Savory Pies', 'Free Of...', 'Coconut', 'Lunch/Snacks', 'Poultry', 'Steak', 'Healthy', 'Lobster', 'Halibut', 'Broil/Grill', 'Crab', 'Pears', 'Cauliflower', 'Candy', 'White Rice', 'Chowders', 'Tex Mex', 'Bass', 'Fruit', 'Hungarian', 'German', 'European', 'New Zealand', 'Chicken Thigh & Leg', 
            'Indonesian', 'Greek', 'Corn', 'Lentil', 'Summer', 'Long Grain Rice', 'Southwest Asia (middle East)', 'Oranges', 'Tuna', 'Citrus', 'Berries', 'Peppers', 'Asian', 'Mexican', 'Raspberries', 'Beans', 'Beef Organ Meats', 'Short Grain Rice', 'Manicotti', 'One Dish Meal', 'Onions', 'Cajun', 'Oven', '< 15 Mins', 'Rice', 'Apple', 'Gelatin', 'Clear Soup', 'Veal', 'Spanish', 'Roast', 'Shakes', 'Orange Roughy', 'Chutneys', 'Melons', '< 60 Mins', 'Mussels', 'Colombian', 'Microwave', 'Roast Beef', 'Perch', 'Gumbo', 'Turkish', 'For Large Groups', 'Christmas', 'Spreads', 'Chinese', '< 30 Mins', 'Meatloaf', 'Winter', 'Trout', 'Smoothies', 'Yam/Sweet Potato', 'Meatballs', 'Whole Duck', 'Strawberry', 'Caribbean', 'Scandinavian', 'Greens', 'Ham', 'Stocks', 'Savory', 'Crawfish', 'Vietnamese', 'Catfish', 'Thai', 'Deer', 
            'Wild Game', 'Pheasant', 'Japanese', 'Canadian', 'Salad Dressings', 'Spring', 'Vegan', 'Grains', 'Collard Greens', 'Tilapia', 'Penne', 'Refrigerator', 'Potluck', 'Spicy', 'Moroccan', 'Pressure Cooker', 'Papaya', 'Kid Friendly', 'Korean', 'Whole Turkey', 'Pasta Shells', 'Plums', 'Danish', 'Lebanese', 'Creole', 'Medium Grain Rice', 'Spinach', 'Squid', 'Homeopathy/Remedies', 'Thanksgiving', 'Moose', 'Native American', 'African', 'High Fiber', 'Kosher', 'Norwegian', 'Household Cleaner', 'Ethiopian', 'Polish', 'Belgian', 'Rabbit', 'Swedish', 'Goose', 'Austrian', 'Australian', 'Swiss', 'Pennsylvania Dutch', 'Elk', 'Bear', 'Mahi Mahi', 'Duck Breasts', 'Scottish', 'Quail', 'Tempeh', 'Cuban', 'Turkey Breasts', 
            'Cantonese', 'Peanut Butter', 'Hawaiian', 'Bath/Beauty', 'Szechuan', 'Portuguese', 'Summer Dip', 'Costa Rican', 'Duck', 'Dutch', 'Filipino', 'Welsh', 'Camping', 'Russian', 'St. Patricks Day', 'Pot Pie', 'Polynesian', 'Cherries', 'Egyptian', 'Chard', 'Lime', 'Lemon', 'Kiwifruit', 'Mango', 'No Shell Fish', 'Whitefish', 'Brunch', 'Malaysian', 'Toddler Friendly', 'Octopus', 'Nigerian', 'Mixer', 'Venezuelan', 'Bread Machine', 'South African', 'Finnish', 'No Cook', 'South American', 'Nepalese', 'Palestinian', 'Egg Free', 'Sweet', 'Czech', 'Icelandic', 'Beginner Cook', 'Hunan', 'Halloween', 'Avocado', 'Iraqi', '< 4 Hours', 'Pakistani', 'Chocolate Chip Cookies', 'Canning', 'Stove Top', 'Puerto Rican', 'Ecuadorean', 'Hanukkah', 'Chilean', 'Breakfast Eggs', 'Cambodian', 'Honduran', 'Peruvian', 'Nuts', 'Peanut Butter Pie', 'Deep Fried', 'Ham And Bean Soup', 'Bread Pudding', 'Margarita', 'Bean Soup', 'Turkey Gravy', 'Spaghetti Sauce', 'Freezer', 'Lemon Cake', 'Black Bean Soup', 'Somalian', 'Main Dish Casseroles', 'Pot Roast', 'Potato Soup', 'Broccoli Soup', 'Apple Pie', 'Oatmeal', 'Soups Crock Pot', 'Roast Beef Crock Pot', 'Chicken Crock Pot', 'Breakfast Casseroles', 'Grapes', 'Macaroni And Cheese', 'Mashed Potatoes', 'Desserts Fruit', 'Birthday', 'Pumpkin', 'Ice Cream', 'Artichoke', 'Indian', 'Baking', 'Beef Liver', 'Memorial Day', 'Sudanese', 'Coconut Cream Pie', 'Easy', 'Steam', 'Dehydrator', 'Mongolian', 'Small Appliance' ]

category_words = ['savory', 'easy', '< 60 min', 'meat', 'dessert', '< 4 hour', 'vegetable', '< 30 min', 'healthy', 'low cholesterol', 'inexpensive', 'beginner cook', 'low protein', 'fruit', 'european', 'kid friendly', 'weeknight', 'lunch/snacks', 'for large group', 'one dish meal', '< 15 min', 'brunch', 'bread', 'breakfast', 'asian', 'sweet', 'very low carbs',
                'chicken breast', 'potluck', 'vegan', 'christmas', 'summer', 'spicy', 'winter', 'high protein', 'mexican', 'quick bread', 'from scratch', 'egg free', 'toddler friendly', 'sauce', 'thanksgiving', 'canadian', 'kosher', 'bar cookie', 'pie', 'lactose free', 'drop cooky', 'beverage', 'stew', 'southwestern u.s.', 'indian', 'citrus', 'yeast bread', 'spring',
                'australian', 'african', 'chinese', 'candy', 'greek', 'frozen dessert', 'savory pie', 'broil/grill', 'stir fry', 'southwest asia middle east', 'curry', 'tex mex', 'thai', 'german', 'camping', 'caribbean', 'cajun', 'no cook', 'scandinavian', 'deep fried', 'south american', 'canning', 'roast', 'spanish', 'creole', 'japanese', 'moroccan', 'salad dressing', 
                'baking', 'wild game', 'scottish', 'st. patrick day', 'halloween', 'hanukkah', 'new zealand', 'stock', 'birthday', 'smoothy', 'punch beverage', 'russian', 'hawaiian', 'polish', 'swedish', 'vietnamese', 'portuguese', 'hungarian', 'swiss', 'deer', 'korean', 'pumpkin', 'south african', 'filipino', 'pakistani', 'lebanese', 'turkish', 'cuban', 'ramadan', 'chutney', 
                'danish', 'dutch', 'indonesian', 'jelly', 'no shell fish', 'pennsylvania dutch', 'brazilian', 'norwegian', 'native american', 'austrian', 'shake', 'cantonese', 'belgian', 'dairy free food', 'egyptian', 'manicotti', 'czech', 'ice cream', 'polynesian', 'malaysian', 'finnish', 'southwest asia (middle east)', 'sourdough bread', 'peruvian', 'high fiber', 'puerto rican',
                'colombian', 'iraqi', 'labor day', 'bath/beauty', 'ethiopian', 'memorial day', 'tempeh', 'palestinian', 'chilean', 'nepalese', 'dehydrator', 'cambodian', 'homeopathy/remedies', 'icelandic', 'venezuelan', 'ecuadorean', 'hunan', 'college food', 'nigerian', 'costa rican', 'chinese new year', 
                'guatemalan', 'mongolian', 'georgian', 'honduran', 'somalian', 'sudanese']

time_words = ['< 60 min', '< 4 hour', '< 30 min', '< 15 min' ]
other_stop_words = ['high in...', 'bread machine', 'small appliance', 'yam/sweet potato', 'potato', 'onion', 'lemon', 
                    'pork', 'whole chicken', 'chicken', 'poultry', 'lamb/sheep', 'green', 'pineapple', 'tropical fruit', 'duck', 'raspberry', 'berry', 'apple', 'pear', 'pepper', 'long grain rice', 'black bean', 'bean', 'refrigerator', 'microwave', 'chicken thigh & leg', 
                    'freezer', 'oven', 'stove top', 'free of...', 'gelatin', 'goose', 'grain', 'grape', 'gumbo', 'halibut', 'ham', 'lentil', 'lime', 'liver', 'lobster', 'cheese', 'meatball', 'meatloaf', 'medium grain rice', 'melon', 'mixer', 'moose', 'chicken brest',
                    'mussel', 'nut', 'orange', 'orange roughy', 'oyster', 'papaya', 'pasta shell', 'peanut butter', 'penne', 'perch', 'pheasant', 'plum', 'pressure cooker', 'quail', 'rabbit', 'rice', 'roast beef', 'scone', 'short grain rice', 'soy/tofu', 'steak',
                    'spaghetti', 'spinach', 'spread', 'squid', 'strawberry', 'tart', 'thigh & leg', 'tilapia', 'trout', 'tuna', 'turkey breast', 'welsh', 'white rice', 'whitefish', 'whole', 'whole turkey', 'yam/sweetbass', 'bear', 'beef liver', 'beef organ meat', 
                    'breast', 'brown rice', 'catfish', 'cauliflower', 'cheesecake', 'cherry', 'chocolate chip cooky', 'chowder', 'clear soup', 'coconut', 'crab', 'crawfish', 'cookie & brownie', 'corn', 'beef kidney', 'pasta elbow', 'halloween cocktail', 'pot roast', 
                    'breakfast egg', 'bean soup', 'egg breakfast', 'spaghetti sauce', 'crock pot slow cooker', 'turkey gravy', 'cabbage', 'lemon cake', 'chicken stew', 'marinara sauce', 'summer dip', 'peanut butter pie', 'served hot new year', 'ham and bean soup', 'bread pudding', 
                    'margarita', 'beef sauce', 'for large group holiday/event', 'navy bean soup', 'cranberry sauce', 'pork loin', 'baked bean', 'black bean soup', 'cucumber', 'main dish casserole', 'potato soup', 'beef crock pot', 'broccoli soup', 'apple pie', 'soup crock pot', 'roast beef crock pot', 
                    'tomato sauce', 'chicken crock pot', 'beef sandwich', 'breakfast potato', 'breakfast casserole', 'strawberry dessert', 'dessert easy', 'dessert fruit', 'coconut dessert', 'coconut cream pie', 'pork crock pot', 'high in... diabetic friendly', 'octopus', 'household cleaner', 'elk', 
                    'pot pie', 'bass', 'artichoke', 'kiwifruit', 'duck breast', 'whole duck', 'mahi mahi', 'oatmeal', 'avocado', 'chicken liver', 'reynolds wrap contest', 'chard', 'macaroni and cheese', 'szechuan', 'collard green', 'mashed potato', 'veal', 'mango', 'steam']
lemmatizer = WordNetLemmatizer()
txy = []
tyt=[]
for i in category_words:
    if i in country_list or i in time_words:
        txy.append(i)
    else:
        tyt.append(i)
print("new country list",tyt)

#other_stop_words = [word.lower() for word in other_stop_words]
#other_stop_words =  list(dict.fromkeys(other_stop_words))
#print("this is otherstop words",other_stop_words)

#words_to_remove = [lemmatizer.lemmatize(m) for m in cultur_no_words]
#print(words_to_remove)
#corpus = data.Keywords.apply(get_and_sort_corpus)
#test =[]

#ct =[x.lower() for x in categroy_no_words]
#cultur_no_words = [x.lower() for x in cultur_no_words]
#print("before change actegory words:", ct)
#for s in cultur_no_words:
#    if s in country_list:
#        test.append(s)
#        cultur_no_words.remove(s)


#country_list =[x.lower() for x in country_list] 
 
#categroy_no_words =[x.lower() for x in categroy_no_words] 

#if 'American' in country_list:
#    print("wordek")
#x = 0
#show =[]

#for ingredients in data['RecipeCategory']:
    #for wot in savory:    
    #if not(ingredients in test):
    #    test.append(ingredients)
    #else:
    #    continue

#print(test)

    #for x in data['Keywords']:
    #ing = ast.literal_eval(x)
    #ingredients = ast.literal_eval(ingredients)
    #print("see ingredients",ingredients)
    #for i in ing:
    #print("this is the keywords for the category:", ingredients, data['Keywords'][x])
    #ingredient = ingredients.split()
    
    #for i in ingredient:
    #if ingredients == 'Healthy':
    #    test.append((ingredients, data['Keywords'][x], data['Name'][x]))
    #    for s in ast.literal_eval(data['Keywords'][x]):
    #        if s == 'Dessert':
    #            show.append((ingredients))
        #print("this is the words tafter", ingredient)
        #vocab.update(ingredient)
    #x = x+1
#wors_list=[]
#for word, frequency in vocab.most_common(len(vocab)):
    #print(f'{word};{frequency}')
    #wors_list.append(word)
#wors_list.sort()
#sty = [*set(test)]
#for i in test:
#    print("test", i)
#for t in show:
#    print("show", t)
#sy = list(dict.fromkeys(show))
#print(sy)
#print("this si country list", country_list)
#print("test list",cultur_no_words)
#print("words list",wors_list)



#recipe_df = pd.read_csv(r'app\csvfiles\parseddocuments.csv')

#vocabulary = nltk.FreqDist()
#for ingredients in recipe_df['ingredients_parsed']:
    #print("see if its a list",ast.literal_eval(ingredients) ,  type(ast.literal_eval(ingredients)))
#    ingredients = ast.literal_eval(ingredients)
#    vocabulary.update(ingredients)
#wdlist= []
#for word, frequency in vocabulary.most_common(len(vocabulary)):
    #print(f'{word};{frequency}')
#    wdlist.append([word, frequency])
#print(wdlist)
#fdist = nltk.FreqDist(ingredients)

#common_words = []
#for word, _ in vocabulary.most_common(len(vocabulary)):
#    common_words.append(word)
#print("common words:",common_words)




#import re
#steps = data.RecipeInstructions.values
#for i in steps:
#    i= i.replace("[", "")
#    i=i.replace("]","")
#    i=i.replace(".","")
    #i=i.replace(",","")
#    i = i.split(",")
    #i= re.findall('[A-Z][^A-Z]*', i)
#    print((i))

def get_recommendations(N, scores):
    """
    Top-N recomendations order by score
    """
    df_recipes = pd.read_csv(r'C:\xampp\htdocs\3161Database files\recipe_recommender\app\csvfiles\parseddocuments.csv')
    
    # order the scores with and filter to get the highest N scores
    S = len(scores)
    top = sorted(range(S), key=lambda x: scores[x], reverse=True)[:S]
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
    print(len(top))
    #return recommendation
    return top

class MeanEmbeddingVectorizer(object):
    def __init__(self, word_model):
        self.word_model = word_model
        self.vector_size = word_model.wv.vector_size

    def fit(self):  # comply with scikit-learn transformer requirement
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
                mean.append(self.word_model.wv.get_vector(word))

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
            #t= ""
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

def changetolist(values):
    if isinstance(values, list):
        keysw = values
        
    else:
        keysw = ast.literal_eval(values)
    return keysw



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

    # get average embdeddings for each document
    mean_vec_tr = MeanEmbeddingVectorizer(model)
    doc_vec = mean_vec_tr.transform(corpus)
    doc_vec = [doc.reshape(1, -1) for doc in doc_vec]
    assert len(doc_vec) == len(corpus)
    
    
    # use TF-IDF as weights for each word embedding
    #tfidf_vec_tr = TfidfEmbeddingVectorizer(model)
    #tfidf_vec_tr.fit(corpus)
    #doc_vec = tfidf_vec_tr.transform(corpus)
    #doc_vec = [doc.reshape(1, -1) for doc in doc_vec]
    #assert len(doc_vec) == len(corpus)

    # create embessing for input text
    input = ingredients
    # create tokens with elements
    input = input.split(",")
    # parse ingredient list
    input = category_parser(input)
    print("This is is the input : ", input)
    
    # get embeddings for ingredient doc
    #input_embedding = tfidf_vec_tr.transform([input])[0].reshape(1, -1)
    input_embedding = mean_vec_tr.transform([input])[0].reshape(1, -1)
    # get cosine similarity between input embedding and all the document embeddings
    cos_sim = map(lambda x: cosine_similarity(input_embedding, x)[0][0], doc_vec)
    scores = list(cos_sim)
    
    # Filter top N recommendations
    recommendations = get_recommendations(N, scores)
    addsorteddoctocsv(recommendations, input)

    return recommendations   
 