import time
import pandas as pd
import numpy as np
from calendar import day_name, month_name


CITY_DATA = { "chicago": "chicago.csv",
              "new york city": "new_york_city.csv",
              "washington": "washington.csv" }


def init_dataframe():
    """
    Asks user to specify a city, month, and day to analyze, then build the data frame base on those values.
    """
    print("\n\033[34mHello! Let\"s explore some US bikeshare data!\033[0m")
    # query the user for a city. We are going to take input as a integer instead of a string to avoid difficulties with capitalization, spelling, or spacing, then validate it.
    while True:
        try:
            city_num = int(input("\nPlease enter the number for the city you wish to see data for.\n1. Chicago\n2. New York City\n3. Washington\nEnter 1, 2 or 3: "))
            # use user input to define the city variable. We do it here so that we can format the error and confirmation messages
            if city_num == 1:
                city = "chicago"
            elif city_num == 2:
                city = "new york city"
            elif city_num == 3:
                city = "washington"
            # if the input is valid, notify the user and move on
            if 1 <= city_num <= 3:
                print("\n\033[32m{} selected.\033[0m".format(city.title()))
                break
            # if the input is an integer but not within the valid range, notify the user and re-query
            else:
                print("\n\033[91mInput not within the valid range, please try again.\033[0m")
        # if the user hits ctrl-c while in the input loop, exit the program
        except KeyboardInterrupt:
            print("\n\033[91mProgram interrupted by user!\033[0m")
            raise SystemExit
        # # if the user gives us something that isn't a number, catch the error, inform the user, and restart the loop
        except:
            print("\n\033[91mInvalid input, please try again.\033[0m")

    # read the csv file into a data frame using the CITY_DATA dictionary to define the file name.
    try:
        df = pd.read_csv(CITY_DATA[city])
    # if the file is not present, inform the user and exit
    except FileNotFoundError:
        print("\n\033[91mCSV file not found for {}. Please verify the files are present in the working directory and retry.\033[0m".format(city))
        raise SystemExit
    
    # convert the Start Time column into a datetime type
    df["Start Time"] = pd.to_datetime(df["Start Time"])

    # query the user to select a month. We're doing it in a while True and try loop so we can validate it and if it's not right redo the query.
    while True:
        try:
            # query the user for a number. We're using a number here to avoid typos, issues with capitalization, or shortening of month names (ie feb instead of febuary). If it's not a number, the except will catch it and restart the loop
            month = int(input("\nPlease select a month using a number or 0 for all months\nEnter a number 0-12: "))
            # if the user gives us zero, it means no filter so we'll break out of the loop and move on
            if month == 0:
                print("\n\033[32mSelecting all months.\033[0m")
                break
            # if the user gives us a number between 1 and 12, continue
            elif 1 <= month <= 12:
                # evaluate if the month selected has entries in the df. If it doesn't, it will throw errors when we try to pull the stats
                if df[df["Start Time"].dt.month == month].empty:
                    print("\n\033[91mThe selected month has no trips.\033[0m")
                else:
                    # if the input has passes all checks, filter the dataframe and move on.
                    print("\n\033[32m{} selected.\033[0m".format(month_name[month]))
                    df = df[df["Start Time"].dt.month == month]
                    break
            # if the user gives us a number that isn't int he valid range, inform the user and restart the loop
            else:
                print("\n\033[91mInput not within the valid range, please try again.\033[0m")
        # if the user hits ctrl-c while in the input loop, exit the program
        except KeyboardInterrupt:
            print("\n\033[91mProgram interrupted by user!\033[0m")
            raise SystemExit
        # if the user gives us something that isn't a number, catch the error, inform the user, and restart the loop
        except:
                print("\n\033[91mInput must be a number between 0 and 12, please try again.\033[0m")
        
    # query the user to select a day. We're doing it in a while True and try loop so we can validate it and if it's not right redo the query.
    while True:
        try:
            # query the user for a number. We're using a number here to avoid typos, issues with capitalization, or shortening of day names (ie mon instead of monday). If it's not a number, the except will catch it and restart the loop
            day = int(input("\nPlease select the day of the week using a number or 0 for all days. Monday is 1, Sunday is 7.\nEnter a number 0-7: "))
            # if the user gives us zero, it means no filter so we'll break out of the loop and move on
            if day == 0:
                print("\n\033[32mSelecting all days.\033[0m")
                break
            # if the user gives us a number between 1 and 7, continue
            elif 1 <= day <= 7:
                # subtract one from the number the user gives us. dt.dayofweek normally takes 0 for monday, but that might be unintuitive for users, so we let them do 1 for monday and adjust the numbers for our use behind the scene
                day -= 1
                # evaluate if the day selected has entries in the df. If it doesn't, it will throw errors when we try to pull the stats.
                if df[df["Start Time"].dt.dayofweek == day].empty:
                    print("\n\033[91mThe selected day has no trips!\033[0m")
                # if the input has passed all checks, filter the dataframe and move on.
                else:
                    print("\n\033[32m{} selected.\033[0m".format(day_name[day]))
                    df = df[df["Start Time"].dt.dayofweek == day]
                    break
                break
            # if the user gives us a number that isn't int he valid range, inform the user and restart the loop
            else:
                print("\n\033[91mInput not within the valid range, please try again.\033[0m")
        # if the user hits ctrl-c while in the input loop, exit the program
        except KeyboardInterrupt:
            print("\n\033[91mProgram interrupted by user!\033[0m")
            raise SystemExit
        # if the user gives us something that isn't a number, catch the error, inform the user, and restart the loop
        except:
            print("\n\033[91mInvalid input, please try again.\033[0m")

    print("\n", "-"*40)
    return df


def time_stats(df):
    """Displays statistics on the most frequent times of travel."""

    print("\n\033[34mCalculating The Most Frequent Times of Travel...\033[0m\n")
    start_time = time.time()

    # get the most common month by counting amount of trips in each month, and grabbing the highest as most_common_month
    most_common_month = month_name[df["Start Time"].dt.month.value_counts().idxmax()]

    # get the most common day of the week by counting amount of trips in each day and grabbing the highest as most_common_dow
    most_common_dow = day_name[df["Start Time"].dt.dayofweek.value_counts().idxmax()]

    # create a list for the most common hour, first entry is the hour, second is the AM/PM
    most_common_hour = [0, "A"]
    # get the most common hour by counting amount of trips in each hour and grabbing the highest, then save it to the first entry of the most_common_hour list
    most_common_hour[0] = df["Start Time"].dt.hour.value_counts().idxmax()
    # if the hour is over 12, convert it to a 12 hour format so it's more readable by the user
    if most_common_hour[0] > 12:
        most_common_hour[0] -= 12
        most_common_hour[1] = "P"

    # print the results of the most common hour
    print("Most trips happened in the month of {}.\nMost trips happened on {}.\nMost trips started at {}:00 {}M.".format(most_common_month, most_common_dow, most_common_hour[0], most_common_hour[1]))


    print("\nThis took {} seconds.".format(f'{(time.time() - start_time):.2f}'))
    print("-"*40)


def station_stats(df):
    """Displays statistics on the most popular stations and trip."""

    print("\n\033[34mCalculating The Most Popular Stations and Trip...\033[0m\n")
    start_time = time.time()

    # get the most common start station by counting amount trips from of each and finding the max
    most_common_start = df["Start Station"].value_counts().idxmax()

    # get the most common end station by counting amount of trips to each and finding the max
    most_common_end = df["End Station"].value_counts().idxmax()

    # get the most common start/end comination by grouping the dataframe by start and end station, return a series with each start/end being the index, and the count being the values, reset the index to the counts column, sort it by decending, then take the top result and save it to start_end_count
    start_end_count = df.groupby(["Start Station", "End Station"]).size().reset_index(name="Count").sort_values(by="Count", ascending=False).iloc[0]

    #p print the results
    print("The most common starting station was \"{}\". The most common ending station was \"{}\".\nThe most common trip started at \"{}\" station and ended at \"{}\" station. It occured {} times.".format(most_common_start, most_common_end, start_end_count[0], start_end_count[1], start_end_count[2]))


    print("\nThis took {} seconds.".format(f'{(time.time() - start_time):.2f}'))
    print("-"*40)


def trip_duration_stats(df):
    """Displays statistics on the total and average trip duration."""

    print("\n\033[34mCalculating Trip Duration...\033[0m\n")
    start_time = time.time()

    # get the total travel time for the selected period, then divide by 60 because the time is stored in seconds
    total_travel = int(df["Trip Duration"].sum() / 60)

    # get the mean travel time for the selected period, then divide by 60 because the time is stored in seconds
    mean_travel = int(df["Trip Duration"].mean() / 60)

    # print the results of total and mean travel time
    print("Customers rode for a total of {} minutes in the selected period.\nThe average trip was {} minutes long.".format(total_travel, mean_travel))

    print("\nThis took {} seconds.".format(f'{(time.time() - start_time):.2f}'))
    print("-"*40)


def user_stats(df):
    """Displays statistics on bikeshare users."""

    print("\n\033[34mCalculating User Stats...\033[0m\n")
    start_time = time.time()

    # get counts of user types
    # make sure there is User Type info within the dataframe
    if "User Type" in df.columns:
        # get counts of rides with each type of User Types
        sub_count = df[df["User Type"] == "Subscriber"].shape[0]
        cust_count = df[df["User Type"] == "Customer"].shape[0]
        dep_count = df[df["User Type"] == "Dependent"].shape[0]
        # get a count of rides with no specified User Type
        nan_user_count = df["User Type"].isna().sum()
        # print the results
        print("There are {} rides by subscribers, {} rides by customers, {} rides by dependents, and {} rides without a specified customer type.".format(sub_count, cust_count, dep_count, nan_user_count))
    else:
        # if there is no user type data, inform the user
        print("\033[91mThere is no data on user types for your selected filters.\033[0m")

    # get counts of gender
    # make sure there is gender data within the dataframe
    if "Gender" in df.columns:
        # get counts of rides for each gender
        male_count = df[df["Gender"] == "Male"].shape[0]
        female_count = df[df["Gender"] == "Female"].shape[0]
        # get a count of rides with no specified gender
        nan_gender_count = df["Gender"].isna().sum()
        # print the results
        print("There are {} rides with male riders, {} rides with female riders, and {} rides without a specified gender.".format(male_count, female_count, nan_gender_count))
    else:
        # if there is no gender data, inform the user
        print("\033[91mThere is no gender data for your selected filters.\033[0m")

    # get birth year data
    # make sure there is birth year data in the dataframe
    if "Birth Year" in df.columns:
        # find the earliest, most recent, and most common birth years
        this_year = time.localtime().tm_year
        earliest_year = int(df["Birth Year"].dropna().min())
        most_recent_year = int(df["Birth Year"].dropna().max())
        most_common_year = int(df["Birth Year"].dropna().value_counts().index[0])
        # print the results
        print("The earliest birth year is {} making the oldest rider {}. The most recent birth year is {} making the youngest rider {}. The most common birth year is {} making {} the most common age.".format(earliest_year, this_year - earliest_year, most_recent_year, this_year - earliest_year, most_common_year, this_year - most_common_year))
    else:
        # if there is no birth year data, inform the user
        print("\033[91mThere is no birth year data for this city.\033[0m")

    print("\nThis took {} seconds.".format(f'{(time.time() - start_time):.2f}'))
    print("-"*40)


def main():
    while True:
        df = init_dataframe()
        time_stats(df)
        station_stats(df)
        trip_duration_stats(df)
        user_stats(df)

        # Ask if the user wants to see the raw data, if they don't, move on
        if input("\nWould you like to see the raw data? (default: yes): ").lower() in ["yes", "y", ""]:
            # pre set the starting index at 0
            start_index = 0
            # while loop to check make sure we are still within the contents of the data frame
            while start_index < len(df):
                # set the end index to 5 after the start. This is where you can change how many lines you want to see per print
                end_index = start_index + 5
                # print the selection of the raw data frame
                print(df[start_index:end_index])
                # inform the user how far into the dataframe they are
                print("Entries {} - {} of {}".format(start_index + 1, end_index, len(df)))
                # if you are at or past the end of the data frame, notify the user and exit the loop
                if end_index >= len(df):
                    print("\033[91mYou're at the end of the data!\033[0m")
                    break
                # ask the user if they want to continue. If they do, reset the start index to just after the current end, and restart to loop. If not, move on.
                if input("Continue? (default: yes): ").lower() not in ["yes", "y", ""]:
                    break
                else:
                    start_index = end_index + 1
        # ask the user if they want to restart the program, if not exit.
        if input("Would you like to restart? (default: no): ").lower() not in ["yes", "y"]:
            print("Exiting...")
            raise SystemExit

if __name__ == "__main__":
    try:
        while True:
            main()
    except KeyboardInterrupt:
        print("\n\033[91mProgram interrupted by user!\033[0m\n")
        raise SystemExit