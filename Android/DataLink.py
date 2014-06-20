
Categories = ['APP_WALLPAPER', 'ARCADE', 'BOOKS_AND_REFERENCE', 'BRAIN', 'BUSINESS', 'CARDS',
			  'CASUAL', 'COMICS', 'COMMUNICATION', 'EDUCATION', 'ENTERTAINMENT', 'FINANCE',
			  'GAME_WALLPAPER', 'GAME_WIDGETS', 'HEALTH_AND_FITNESS', 'LIBRARIES_AND_DEMO',
			  'LIFESTYLE', 'MEDIA_AND_VIDEO', 'MEDICAL', 'MUSIC_AND_AUDIO', 'NEWS_AND_MAGAZINES',
 			  'PERSONALIZATION', 'PHOTOGRAPHY', 'PRODUCTIVITY', 'RACING', 'SHOPPING', 'SOCIAL',
 			  'SPORTS', 'SPORTS_GAMES', 'TOOLS', 'TRANSPORTATION', 'TRAVEL_AND_LOCAL', 'WEATHER']

Links = ['https://play.google.com/store/apps/collection/topselling_paid_game',
        'https://play.google.com/store/apps/collection/topselling_free',
        'https://play.google.com/store/apps/collection/topselling_paid',
        'https://play.google.com/store/apps/collection/topgrossing',
        'https://play.google.com/store/apps/collection/topselling_new_paid_game',
        'https://play.google.com/store/apps/collection/topselling_new_free',
        'https://play.google.com/store/apps/collection/topselling_new_paid']

Types = ['free', 'paid']

CategoriesType = map(None,
					Categories * 2,
					[Types[0]] * len(Categories)
					+ [Types[1]] * len(Categories))

categoryURL = "https://play.google.com/store/apps/category/"
categoryURLtype = "/collection/topselling_"

def generateURL():

	for category, categoryType in CategoriesType:
            yield categoryURL + category + categoryURLtype + categoryType


