import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    # List valid cities
    listOfCities = ['chicago' , 'new york city', 'washington']
    
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    city_raw = input("Would you like to see data for Chicago, New York or Washington?")
    city = city_raw.lower()
    
    # Transform input for New York City
    ListOfNYC = ['new york' , 'nyc', 'ny', 'newyork', 'n y']
    if city in ListOfNYC:
        city = 'new york city'
    
    # Check if input is valid
    while city not in listOfCities:
        city_raw = input("That's not a valid city, please specify: Would you like to see data for Chicago, New York or Washington?")
        city_raw = input("Would you like to see data for Chicago, New York or Washington?")
        city = city_raw.lower()
    
        # Transform input for New York City
        ListOfNYC = ['new york' , 'nyc', 'ny']
        if city in ListOfNYC:
           city = 'new york city'
     
    # Get user input for filers
    filters_raw = input("Would you like to filter by month, day, both or not at all? Type \'none\' for no time filter.")
    filters = filters_raw.lower()
    
    if filters in ['month', 'both']:
        # Get user input for month (all, january, february, ... , june)
        listOfMonths = ['all', 'january', 'february', 'march', 'april', 'may' , 'june']
        month = 'x'
        while month not in listOfMonths:
            month_raw = input("Which month? All, January, February, March, April, May or June?")
            month = month_raw.lower()
            day = 'all'

    if filters in ['day', 'both']:
        # Get user input for day of week (all, monday, tuesday, ... sunday)
        day = 'x'
        listOfDays = ['all', 'monday', 'tuesday', 'wednesday', 'friday', 'saturday', 'sunday']
        while day not in listOfDays:
            day_raw = input("Which day? Monday, Tuesday, Wednesday, Friday, Saturday or Sunday?")
            day = day_raw.lower()
            month = 'all'
    
    if filters == 'none':
        month = 'all'
        day = 'all'


    print('-'*40)
    return city, month, day

def load_data(city, month, day):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """

    # load data file into a dataframe
    df = pd.read_csv(CITY_DATA[city])

    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extract month and day of week from Start Time to create new columns
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name

    # filter by month if applicable
    if month != 'all':
        # use the index of the months list to get the corresponding int
        months = ['january', 'february', 'march', 'april', 'may', 'june']
        month = months.index(month) + 1

        # filter by month to create the new dataframe
        df = df[df['month'] == month]

    # filter by day of week if applicable
    if day != 'all':
        # filter by day of week to create the new dataframe
        df = df[df['day_of_week'] == day.title()]

    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Calculating the most common month
    # extract month from the Start Time column to create a month column
    df['month'] = df['Start Time'].dt.month

    # find the most popular month
    popular_month_idx = df['month'].mode()[0]
    months = ['January', 'February', 'March', 'April', 'May', 'June']
    popular_month = months[popular_month_idx-1]
    print("Popular month: " , popular_month)

    # Calculating the most common day of week
    # extract day of the week from the Start Time column to create a day_of_week column
    df['day_of_week'] = df['Start Time'].dt.dayofweek

    # find the most popular day of the week
    popular_day_of_week_idx = df['day_of_week'].mode()[0]
    weekDays = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
    popular_day_of_week = weekDays[popular_day_of_week_idx]
    print("Popular day of the week: " , popular_day_of_week)


    # Calculating the most common start hour
    # convert the Start Time column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])

    # extract hour from the Start Time column to create an hour column
    df['hour'] = df['Start Time'].dt.hour

    # find the most popular hour
    popular_hour = df['hour'].mode()[0]
    print("Popular hour: " , popular_hour)


    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    popular_Start_Station = df['Start Station'].mode()[0]
    print("Most popular Start Station: " ,popular_Start_Station)

    # Display most commonly used end station
    popular_End_Station = df['End Station'].mode()[0]
    print("Most popular End Station: " ,popular_End_Station)
    
    # Combine Start and End Station in one column
    df['combination'] = df['Start Station'] + " - " + df['End Station']
    
    #Display most popular combination of Start and End Station
    popular_combination = df['combination'].mode()[0]
    print("Most popular combination: " ,popular_combination)
    
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Calculate travel time per trip
    df['travel_time']=df['End Time']-df['Start Time']
    
    # Display total travel time
    total_travel_time = df['travel_time'].sum(axis = 0)
    print("Total travel time: " , total_travel_time)

    # Display mean travel time
    mean_travel_time = df['travel_time'].mean(axis = 0)
    print("Mean travel time: " , mean_travel_time)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # print value counts for each user type
    user_types = df['User Type'].value_counts()

    print(user_types)
    
    # Check if Gender column is in dataframe
    listOfColumns = list(df.columns.values.tolist())
    
    if 'Gender' in listOfColumns:
        # print value counts for each gender if city is chicago or new york city
        gender = df['Gender'].value_counts()
        print(gender)

    # Check if Birth Year column is in dataframe
    if 'Birth Year' in listOfColumns:
        # Display earliest, most recent, and most common year of birth
        earliest_birth_year = df['Birth Year'].min()
        print("Earliest Birth Year: " , earliest_birth_year)
    
        most_recent_birth_year = df['Birth Year'].max()
        print("Most Recent Birth Year: " , most_recent_birth_year)
    
        most_common_birth_year = df['Birth Year'].mode()[0]
        print("Most Common Birth Year: " , most_common_birth_year)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)
       
        view_data = input('\nWould you like to view 5 rows of individual trip data? Enter yes or no\n')
        start_loc = 0
        view_display = 'yes'
        while (view_display != 'no'):
            print(df.iloc[start_loc:start_loc+5])
            start_loc += 5
            view_display = input('Do you wish to continue?:')
            view_display = view_display.lower()
        
        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
