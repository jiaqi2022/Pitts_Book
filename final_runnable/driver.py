import yelp_scraper as yelp
import place_scraper as place
import pandas as pd
from crime_map import googleMapApi

def find_restaurants():
    print('''
    Retriving data ...
    Please be patient as the scraping takes a minute or two
    ''')

    df = yelp.restaurants_html_to_df()

    print('Ready! You can start searching.\n')

    ans1 = ''
    while ans1 != 'Q' and ans1 != 'q':
        print('''
        Please select:

        1)  Search by Cusine Type
        2)  Search by Customer Rating
        3)  Find Restaurants Nearby
        B)  Back to the Main Menu
        Q)  Quit from this program
        ''')
        ans1 = input('    Your choice: ').strip()
        if ans1 == '1':
            types = yelp.get_types(df)
            while True:
                print('Please select a Cusine Type:\n')
                for idx, item in enumerate(types):
                    print('{})  {}'.format(idx+1, item))

                ans1_1 = input('    Your choice: ').strip()

                idx_ans1_1 = 0

                try:
                    idx_ans1_1 = int(ans1_1)-1
                except ValueError:
                    print('Invalid, your choice should be a number')
                    continue

                if idx_ans1_1 < len(types) and idx_ans1_1 >= 0:
                    break
                else:
                    print('Invalid, choice not found')
            type = types[idx_ans1_1]

            m = df['type'].apply(lambda x: type in x)
            df2 = df[m]
            df2 = df2.reset_index(drop=True)

            for idx, row in df2.iterrows():
                s = '------------------------------------------------------------\n' +\
                    '{:>3}.| Restaurant Name: {}\n' +\
                    '    | Customer Rating: {} \n' +\
                    '    | Cusine Type: {}'
                print(s.format(idx+1, row['name'], row['rating'],
                                ', '.join(df2.loc[idx,'type'])))
            print('------------------------------------------------------------')

        elif ans1 == '2':
            df2 = df.sort_values(by=['rating'], ascending=False)
            df2 = df2.reset_index(drop=True)
            count = 0
            while count < 240:
                for idx, row in df2.iloc[count:count+10].iterrows():
                    s = '------------------------------------------------------------\n' +\
                        '{:>3}.| Restaurant Name: {}\n' +\
                        '    | Customer Rating: {} \n' +\
                        '    | Cusine Type: {}'
                    print(s.format(idx+1, row['name'], row['rating'],
                                    ', '.join(df2.loc[idx,'type'])))
                ans1_2 = input('Continue? [Y/y]: ').strip()
                if ans1_2 == 'Y' or ans1_2 == 'y':
                    count += 10
                    continue
                break

        elif ans1 == '3':
            areas = yelp.get_areas(df)
            while True:
                print('Please select your Location:\n')
                for idx, item in enumerate(areas):
                    print('{})  {}'.format(idx+1, item))

                ans1_3 = input('    Your choice: ').strip()

                idx_ans1_3 = 0

                try:
                    idx_ans1_3 = int(ans1_3)-1
                except ValueError:
                    print('Invalid, your choice should be a number')
                    continue

                if idx_ans1_3 < len(areas) and idx_ans1_3 >= 0:
                    break
                else:
                    print('Invalid, choice not found')

            area = areas[idx_ans1_3]
            df2 = df.loc[df['area']==area]
            df2 = df2.reset_index(drop=True)
            for idx, row in df2.iterrows():
                s = '------------------------------------------------------------\n' +\
                    '{:>3}.| Restaurant Name: {}\n' +\
                    '    | Customer Rating: {} \n' +\
                    '    | Cusine Type: {}'
                print(s.format(idx+1, row['name'], row['rating'],
                                ', '.join(df2.loc[idx,'type'])))
            print('------------------------------------------------------------')

        elif ans1 == 'b' or ans1 == 'B':
            return
        elif ans1 == 'q' or ans1 == 'Q':
            print('Bye!')
            quit()
        else:
            print('\n    Invalid Choice:', ans1, '\n')



def find_fun_places():
    df = place.get_places_df()
    ans2 = ''
    while ans2 != 'Q' and ans2 != 'q':
        print('''
        Is there a specific area you want to explore?:

        1)  yes
        2)  no
        ''')
        ans2 = input('    Your choice: ').strip()

        if ans2 == '1':
            areas = yelp.get_areas(df)
            while True:
                print('Please select a Location:\n')
                for idx, item in enumerate(areas):
                    print('{})  {}'.format(idx+1, item))

                ans2_1 = input('    Your choice: ').strip()

                idx_ans2_1 = 0

                try:
                    idx_ans2_1 = int(ans2_1)-1
                except ValueError:
                    print('Invalid, your choice should be a number')
                    continue

                if idx_ans2_1 < len(areas) and idx_ans2_1 >= 0:
                    break
                else:
                    print('Invalid, choice not found')

            area = areas[idx_ans2_1]
            df2 = df.loc[df['area']==area]
            df2 = df2.reset_index(drop=True)
            for idx, row in df2.iterrows():
                s = '------------------------------------------------------------\n' +\
                    '{:>3}.| Place Name: {}\n' + '    | Description: {} \n'
                print(s.format(idx+1, row['name'], row['description']))
            print('------------------------------------------------------------')

        elif ans2 == '2':
            for idx, row in df.iterrows():
                s = '------------------------------------------------------------\n' +\
                    '{:>3}.| Place Name: {}\n' +\
                    '    | Area: {} \n' +\
                    '    | Description: {}'
                print(s.format(idx+1, row['name'], row['area'], row['description']))
                ans2_2 = input('Continue? [Y/y]: ').strip()
                if ans2_2 == 'Y' or ans2_2 == 'y':
                    continue
                return

        else:
            print('\n    Invalid Choice:', ans2, '\n')


def display_crime_map():

    print('''
    View a map of Pittsburgh crime status (prev 30-day)?:

    1)  yes
    2)  no
    ''')
    ans3 = input('    Your choice: ').strip()

    if ans3 == '1':
        cmu_geolocation = (40.443336, -79.944023)
        gma = googleMapApi()

        filepath='INCIDENT_DATA.csv'
        df = pd.read_csv(filepath, engine='python')
        count_row=df.shape[0]
        crime_location=[]
        for i in range(count_row):
            if df.iloc[i][-1] > 40:
                crime_tuple=(df.iloc[i][-1],df.iloc[i,-2])
                crime_location.append(crime_tuple)

        # Test gmPlotter
        lat_list=[]
        long_list=[]
        for n in range(len(crime_location)):
            (lats,longs)=crime_location[n]
            lat_list.append(lats)
            long_list.append(longs)

        gma.gmPlotter_init(cmu_geolocation)
        gma.gmPlotter_heatmap(lat_list, long_list)
        #gma.gmPlotter.scatter(lat_list, long_list, "#6e2142", marker=False, size=12)
        gma.draw_and_display_gm_plot()

    elif ans3 == '2':
        return

    else:
        print('\n    Invalid Choice:', ans3, '\n')


print('Welcome to Pittsburgh!\n')

answer = ''
while answer != 'Q' and answer != 'q':
    print('''
    Please select from below to explore:

    1)  Find a Restaurant
    2)  Fun Things to Do
    3)  Safety
    Q)  Quit from this program
    ''')

    answer = input('    Your choice: ').strip()
    if answer == '1':
        # proceed to search for restaurants
        find_restaurants()

    elif answer == '2':
        # proceed to search for fun places
        find_fun_places()

    elif answer == '3':
        # display the crime map
        display_crime_map()

    elif answer == 'q' or answer == 'Q':
        print('Bye!')
        pass   # terminate the loop

    else:
        print('\n    Invalid Choice:', answer, '\n')