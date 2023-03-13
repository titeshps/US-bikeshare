import time
import pandas as pd
import numpy as np

city_data = { 'chicago': 'chicago.csv',
              'new york': 'new_york_city.csv',
              'washington': 'washington.csv' }
months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','All']
days = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'all']
options = ['month', 'day', 'both']
day = ''
month = ''
option = ''

def get_filters():
    global day, month, option
    
    print('Hello! Let\'s explore some US bikeshare data!')
    # get user input for city (chicago, new york city, washington).
    city = input('Which city data would you like to explore Chicago, New York, Washington?\n').lower()
    while city not in city_data.keys():
        print('sorry, you must have entered an un available city, or you made a typo, please try again')
        city = input('Which city data would you like to explore Chicago, New York City, Washington?\n').lower()

    # get user input for filter option
    option = input('Would you like to sort by month, day or both?\n').lower()
    while option not in options:
        print('Sorry, but that\'s not a valid option please try again')
        option = input('Would you like to sort by month, day or both?\n').lower()

    # get user input for month (all, january, february, ... , june)
    if option == 'month':
        month = input('Chose a month to filter the data: Jan, Feb, Mar, Apr, May, June, All \n').title()
        while month not in months:
            print('sorry, you must have made a typo, please try again and make sure you\'re useing the abbreviation :)')
            month = input('Chose a month to filter the data: Jan, Feb, Mar, Apr, May, Jun, All \n').title()
        if month == 'All':
            month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

    # get user input for day        
    elif option == 'day':    
        day = input('Chose a day to filter the data: Sun, Mon, Tues, Wed, Thurs, Fri, Sat, All \n').title()
        while day not in days:
            print('sorry, you must have made a typo, please try again and make sure you\'re useing the abbreviation :)')
            day = input('Chose a day to filter the data: Sun, Mon, Tue, Wed, Thu, Fri, Sat, All\n').title()
        if day == 'All':
            day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']

    # get user input for both
    elif options == 'both':
        month = input('Chose a month to filter the data: Jan, Feb, Mar, Apr, May, June, All \n').title()
        while month not in months:
            print('sorry, you must have made a typo, please try again and make sure you\'re useing the abbreviation :)')
            month = input('Chose a month to filter the data: Jan, Feb, Mar, Apr, May, Jun, All \n').title()
        if month == 'All':
            month = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun']

        day = input('Chose a day to filter the data: Sun, Mon, Tues, Wed, Thurs, Fri, Sat, All \n').title()
        while day not in days:
            print('sorry, you must have made a typo, please try again and make sure you\'re useing the abbreviation :)')
            day = input('Chose a day to filter the data: Sun, Mon, Tue, Wed, Thu, Fri, Sat, All \n').title()
        if day == 'All':
            day = ['Sun', 'Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat']
        

    print('-'*40)
    return city, month, day, option

def load_data(city, month, day, option):
    """
    Loads data for the specified city and filters by month and day if applicable.

    Args:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    Returns:
        df - Pandas DataFrame containing city data filtered by month and day
    """
    df = pd.read_csv(city_data[city])
     
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    df['End Time'] = pd.to_datetime(df['End Time'])

    # extracts months
    df['Month'] = df['Start Time'].dt.month

    #converts month from int to words
    Months = {1:'Jan',2:'Feb',3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}
    df['Month'].replace(Months, inplace=True)

    # extracts days
    df['Day'] = df['Start Time'].dt.weekday

    # converts days from ints to words
    Weekday = {0:"Mon", 1:"Tue", 2:"Wed", 3:"Thu", 4:"Fri", 5:"Sat", 6:"Sun"}
    df['Day'].replace(Weekday, inplace=True)

    # filters the data
    if option == 'month':
        df = df.query("Month == @month")
    elif option == 'day':
        df = df.query("Day == @day")
    elif option == 'both':
        df = df.query("Month == @month and Day == @day")

    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # display the most common month
    print('The most common month is: ', df['Month'].mode(), '\n')

    # display the most common day of week
    print('The most common day is: ', df['Day'].mode(), '\n')

    # display the most common start hour
    print('The monst common hour is: ', df['Start Time'].dt.hour.mode(), '\n')
    
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()
    
    # display most commonly used start station
    print('The most commonly used Start Station is: ', df['Start Station'].mode(), '\n')

    # display most commonly used end station
    print('The most commonly used End station is: ', df['End Station'].mode(), '\n')

    # display most frequent combination of start station and end station trip
    df['Trip'] = 'From ' + df['Start Station'] + ' to ' + df['End Station']
    print('The most common trip is: ', df['Trip'].mode(), '\n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # display total travel time
    print('Total travel time is : ', (df['Trip Duration'].sum()) / 86400, ' days\n')

    # display mean travel time
    print('Average travel time is: ', (df['Trip Duration'].mean()) / 60, 'minutes \n')

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)

def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    print('The counts of user types are: \n', df['User Type'].value_counts())

    # Display counts of gender
    if city != 'washington':
        print('The counts of Gender is: \n', df['Gender'].value_counts())

    # Display earliest, most recent, and most common year of birth
    if city != 'washington':
        print('Earlist birth date is: ', df['Birth Year'].min(), '\n' )
        print('Most recent birth date is: ', df['Birth Year'].max(), '\n' )
        print('Most common birth date is: ', df['Birth Year'].mode(), '\n' )

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, option = get_filters()
        df = load_data(city, month, day, option)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()