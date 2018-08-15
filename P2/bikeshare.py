
import time
import pandas as pd
import numpy as np
import datetime

CITY_DATA = { 'chicago': 'chicago.csv',
              'new york city': 'new_york_city.csv',
              'washington': 'washington.csv' }

def get_month(month):
    while True:
        try:
            months_tuple = ('all', 'january', 'february',
                            'march', 'april', 'may', 'june',
                            'july', 'august', 'september',
                            'october', 'november','december')
            if month in months_tuple:
                return month
                break
            else:
                print("\nThis month is not in analyze set\n")
        except:
            print('\nWARNING: Please input a valid month name!\n')

def get_day(day):
    while True:
        try:
            days_tuple = ('all', 'monday', 'tuesday',
                          'wednesday', 'thursday',
                          'friday', 'saturday', 'sunday')

            if day in days_tuple:
                return day
                break
            else:
                print("\nThis day is not in analyze set\n")
        except:
            print('\nWARNING: Please input a valid day!\n')


def get_filters():
    """
    Asks user to specify a city, month, and day to analyze.

    Returns:
        (str) city - name of the city to analyze
        (str) month - name of the month to filter by, or "all" to apply no month filter
        (str) day - name of the day of week to filter by, or "all" to apply no day filter
    """
    print('Hello! Let\'s explore some US bikeshare data!')

    # TO DO: get user input for city (chicago, new york city, washington).
    question_1 = "Would you like to see data for Chicago, New York City, or Washington?"
    print(question_1)
    while True:
        try:
            city = input("> ").lower()
            if city in ('chicago', 'new york city', 'washington'):
                break
            else:
                print("\nThis city is not in analyze set.Enter again!\n")
        except:
            print('\nWARNING: Please input a valid city name.\n')

    # TO DO: get user input for month (all, january, february, ... , june)
    question_2 = "Would you like to filter data by month, day, both, or not at all?Type 'no' for no time filter."
    print(question_2)
    day = 'all'
    month = 'all'
    while True: 
        filter = input("> ").lower()
        if filter == 'both':
            month = get_month(input('Enter the month you want to analyze! : ').lower())
            day = get_day(input('Enter the day you want to analyze! : ').lower())
            break
        elif filter == 'month':
            month = get_month(input('Enter the month you want to analyze! : ').lower())
            break
        elif filter == 'day':
            day = get_day(input('Enter the day you want to analyze! : ').lower())
            break
        elif filter == 'not at all':
            break
        else:
            if filter not in ('both','month','day','not at all'):
                print('Please input a valid filter condition!')
        
    return city, month, day, filter
    print('-'*40)
    


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
    # load data file into a DataFrame
    df = pd.read_csv(CITY_DATA[city])
    # convert Start Time column to a datetime
    df['Start Time'] = pd.to_datetime(df['Start Time'])
    # extract month, day of week and hour from Start Time to create 3 new column
    df['month'] = df['Start Time'].dt.month
    df['day_of_week'] = df['Start Time'].dt.weekday_name
    df['hour'] = df['Start Time'].dt.hour

    # filter by month if applicable
    months_tuple = ('january', 'february', 'march',
                    'april', 'may', 'june',
                    'july', 'august', 'september',
                    'october', 'november', 'december')
    if month != 'all':
        month = months_tuple.index(month) + 1
        df = df[df['month'] == month]
    # filter by day if applicable
    if day != 'all':
        df = df[df['day_of_week'] == day.title()]

    return df

def time_stats(df, month, day,filter):
    """Displays statistics on the most frequent times of travel."""

    print('\nCalculating The Most Frequent Times of Travel...\n')
    start_time = time.time()

    # TO DO: display the most common month
    if month == 'all':
        months_tuple = ('january', 'february', 'march',
                        'april', 'may', 'june',
                        'july', 'august', 'september',
                        'october', 'november', 'december')

        common_num_month = df['month'].mode()[0]
        common_month_count = df['month'].value_counts().max()
        common_month = months_tuple[common_num_month - 1]
        sentence = '''
Most popular month:{}, Count:{}, Filter:{}'''
        print(sentence.format(common_month,
                              common_month_count,
                              filter))

    # TO DO: display the most common day of week
    if day == 'all':
        most_common_day = df['day_of_week'].value_counts().idxmax()
        common_day_count = df['day_of_week'].value_counts().max()
        sentence = '''
Most popular day:{}, Count:{}, Filter:{}'''
        print(sentence.format(most_common_day,
                              common_day_count,
                              filter))

    # TO DO: display the most common start hour
    most_common_hour = df['hour'].value_counts().idxmax()
    common_hour_count = df['hour'].value_counts().max()
    sentence = '''
Most popular hour:{}, Count:{}, Filter:{}'''
    print(sentence.format(most_common_hour,
                              common_hour_count,
                              filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def station_stats(df, filter):
    """Displays statistics on the most popular stations and trip."""

    print('\nCalculating The Most Popular Stations and Trip...\n')
    start_time = time.time()

    # TO DO: display most commonly used start station
    common_start_station = df['Start Station'].value_counts().idxmax()
    start_station_count = df['Start Station'].value_counts().max()
    # TO DO: display most commonly used end station
    common_end_station = df['End Station'].value_counts().idxmax()
    end_station_count = df['End Station'].value_counts().max()

    # TO DO: display most frequent combination of start station and end station trip
    combination = df.groupby(['Start Station','End Station']).size()
    common_combination = combination.idxmax()
    common_combination_size = combination.loc[common_combination[0],common_combination[1]]


    sentence = '''Most commonly used start station is : {}, count:{},
Most commonly used end station is : {}, count: {},
Most frequent combination of start station and end station trip is {} and {},
a total number of this combination is {}, filter:{}.'''

    print(sentence.format(common_start_station,
                          start_station_count,
                          common_end_station,
                          end_station_count,
                          common_combination[0],
                          common_combination[1],
                          common_combination_size,
                          filter))

    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def trip_duration_stats(df, filter):
    """Displays statistics on the total and average trip duration."""

    print('\nCalculating Trip Duration...\n')
    start_time = time.time()

    # TO DO: display total travel time
    total_duration = df['Trip Duration'].sum()
    total_count = df['Trip Duration'].value_counts().sum()
    # TO DO: display mean travel time
    averg_duration = df['Trip Duration'].mean()
    sentence = '''
Total Duration: {}, count: {}, average duration: {}, filter: {}.'''
    print(sentence.format(total_duration,
                          total_count,
                          averg_duration,
                          filter))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def user_stats(df, filter):
    """Displays statistics on bikeshare users."""

    print('\nCalculating User Stats...\n')
    start_time = time.time()

    # TO DO: Display counts of user types
    user_type = df['User Type'].unique()
    user_type_count = df['User Type'].value_counts()

    # TO DO: Display counts of gender
    gender = df['Gender'].unique()
    gender_count = df['Gender'].value_counts()

    # TO DO: Display earliest, most recent, and most common year of birth
    most_common_birth = df['Birth Year'].value_counts().idxmax()
    most_birth_count = df['Birth Year'].value_counts().max()
    most_recent_birth = df.sort_values('Birth Year', ascending=False).iloc[0]['Birth Year']
    earliest_birth = df.sort_values('Birth Year', ascending=True).iloc[0]['Birth Year']
    sentence = '''
***user type***
{} : {}
{} : {}

***gender***
{} : {}
{} : {}

***year of birth***
earliest birth: {}
most recent birth: {}
most common birth: {}, count:{}, filter:{}'''
    print(sentence.format(user_type[0],user_type_count[0],
                            user_type[1],user_type_count[1],
                            gender[0],gender_count[0],
                            gender[1],gender_count[1],
                            earliest_birth,
                            most_recent_birth,
                            most_common_birth,
                            most_birth_count,
                            filter))
    print("\nThis took %s seconds." % (time.time() - start_time))
    print('-'*40)


def main():
    while True:
        city, month, day, filter = get_filters()
        df = load_data(city, month, day)
        time_stats(df, month, day, filter)
        time.sleep(2)
        station_stats(df,filter)
        time.sleep(2)
        trip_duration_stats(df, filter)
        time.sleep(2)
        user_stats(df, filter)
        time.sleep(2)

        restart = input('\nWould you like to restart? Enter yes or no.\n> ')
        if restart.lower() != 'yes':
            break


if __name__ == "__main__":
	main()
