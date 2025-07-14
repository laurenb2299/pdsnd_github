import time
import pandas as pd
import numpy as np

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }
city_choices = ['Chicago','New York City','Washington']
month_choices = ['January', 'February', 'March', 'April', 'May', 'June', 'All']
day_choices = ['Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'All']

def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')
    
    # Get user input for city (chicago, new york city, washington). HINT: Use a while loop to handle invalid inputs
    
    while True:
        city_input = input('Please enter the city you wish to explore: Chicago, New York City, or Washington: ').lower()
        if city_input.lower() in [city.lower() for city in city_choices]:
            break
        else:
            print('That is not a valid choice!')
        
 # Get user input for month (all, january, february, ... , june)
   
    while True:
        month_input = input('Please enter the month you wish to retrieve data for: January, February, March, April, May, June, or All: ').lower()
        month_input = month_input.title()
        if month_input in month_choices:
            break
        else:
            print('That is not a valid choice!')
        
# Get user input for day of week (all, monday, tuesday, ... sunday)
    
    while True:
        day_input = input('Please enter the day of the week you wish to retrieve data for: Sunday, Monday, Tuesday, Wednesday, Thursday, Friday, or All: ').lower()
        day_input = day_input.title()
        if day_input in day_choices:
            break
        else:
            print('That is not a valid choice!')

    print('-'*40)
    return city_input, month_input, day_input


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
    # convert the Start Time Column to datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month and day of week from Start Time to create new columns 
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.day_name()
    df['hour'] = df['Start Time'].dt.hour
    # filter by month if applicable
    if month != 'All':
        # use the index of the months list to get the corresponding int
        month = month_choices.index(month) + 1
    # filter by month to create the new dataframe
        df = df.loc[df['month'] == month]
    # filter by day of week if applicable
    if day != 'All':
    # filter by day of week to create the new dataframe
        df = df.loc[df['day_of_week'] == day.title()]
    return df

def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # Display the most common month
    common_month = df['month'].mode()[0]
    print('The most common month is: ' + month_choices[common_month-1].title())
    
    # Display the most common day of week
    common_dow = df['day_of_week'].mode()[0]
    print('The most common day of the week is: ' + common_dow)

    # Display the most common start hour
    common_hour = df['hour'].mode()[0]
    print('The most common start hour is: ' + str(common_hour))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # Display most commonly used start station
    common_start = df['Start Station'].mode()[0]
    print('The most commonly used start station is: ' + common_start)

    # Display most commonly used end station
    common_end = df['End Station'].mode()[0]
    print('The most commonly used end station is: ' + common_end)

    # Display most frequent combination of start station and end station trip
    df['start_end_combo'] = df['Start Station'] + ' & ' + df['End Station']
    count_combos = df['start_end_combo'].value_counts()
    most_common_combo = count_combos.idxmax()
    print('The most frequent combination of start and end station is: ' + most_common_combo)

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # Display total travel time
    travel_time = df['Trip Duration'].sum()
    print('The total travel time was: ' + str(travel_time))

    # Display mean travel time
    mean_travel = df['Trip Duration'].mean()
    print('The mean travel time was: ' + str(mean_travel))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, city):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # Display counts of user types
    user_types = df['User Type'].value_counts()
    print('The count of user types are as follows: ')
    print(user_types)
    

    # Display counts of gender
    if city.lower() in ['chicago', 'new york city']:
        gender_count = df['Gender'].value_counts()
        print ('\nThe gender counts are as follows: ')
        print(gender_count)
    else:
        print('\nThere is no gender information for Washington')

    # Display earliest, most recent, and most common year of birth
    if city.lower() in ['chicago','new york city']:
        earliest_birth_year = df['Birth Year'].min()
        latest_birth_year = df['Birth Year'].max()
        most_common_birth_year = df['Birth Year'].mode()[0]
        print('\nThe earliest birth year was: ' + str(int(earliest_birth_year)))
        print('The latest birth year was: ' + str(int(latest_birth_year)))
        print('The most common birth year was: ' + str(int(most_common_birth_year)))
    else:
        print('There is no birth year information for Washington. Select Chicago or New York City for this statistic.')
    

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def display_data(df):
    i=0
    while True:
        raw_data = input('\nWould you like to review the first 5 lines of data? Please enter Yes or No: ')
        if raw_data.lower() == 'yes':
            if i<len(df):
                first_five = df.iloc[i:i+5]
                print(first_five)
                i += 5
            else:
                print('No more data to display.')
                break
        elif raw_data.lower()=='no':
            break
        else:
            print('Invalid input. Please enter Yes or No.')
           

def main():
    while True:
        city, month, day = get_filters()
        df = load_data(city, month, day)

        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df, city)
        display_data(df)

        restart = input('\nWould you like to restart? Enter yes or no.\n')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
