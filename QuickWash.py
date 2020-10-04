# This program will clean your data set
# IMPORTING MODULES
import pandas as pd


# Defining function to check for correct input for choosing columns
def user_drop_entry(data_cols, user_input_values):
    user_input_lower = [value.lower() for value in user_input_values]
    if 'exit' in user_input_lower:
        if set(user_input_values).issubset(data_cols):
            long_str = ', '.join(user_input_values)
            if len(user_input_values) == 1:
                print("This program will proceed now without the \"", user_input_values[0], "\" column",
                      sep='')
            else:
                print("This program will proceed further without these following columns:-\n",
                      long_str)
            return 1
        else:
            print("\nProgram terminated\nYou chose to exit")
            print("Bye ＼(*^▽^*)/ Bye\nCome back soon")
            exit()
    elif set(user_input_values).issubset(data_cols):
        long_str = ', '.join(user_input_values)
        if len(user_input_values) == 1:
            print("This program will proceed now without the \"", user_input_values[0], "\" column", sep='')
        else:
            print("This program will proceed further without these following columns:-\n",
                  long_str)
        return 1
    elif user_input_lower == ['']:
        print("\nSince you pressed enter without entering any column name\n"
              "This program will proceed with the complete data-set")
        return 1
    else:
        print("\nWrong Input. There is a minor mistake in the entry. "
              "\nCheck spellings or extra spaces.\nRe-enter your input:- ")
        return 0


# Function to return positive signal only
def column_choice(cols):
    while 1:
        user_input = list(map(str, input().split(', ')))
        if user_drop_entry(cols, user_input):
            break
    return user_input


# Defining function check user choices (Return 1 if True and 0 if False)
def user_entry_check_major(expected, entered):
    temp_string = str(entered).lower()
    if temp_string == 'exit' or entered == expected[-1]:
        print("\nProgram terminated\nYou chose to exit")
        print("Bye ＼(*^▽^*)/ Bye\nCome back soon")
        exit()
    elif entered in expected[:-1]:
        return 1
    else:
        print("Please enter a valid input:-")
        return 0


def user_entry_check_minor(expected, entered):
    if entered in expected:
        return 1
    elif entered.lower() == "exit":
        print("\nProgram terminated\nYou chose to exit")
        print("Bye ＼(*^▽^*)/ Bye\nCome back soon")
        exit()
    else:
        print("Please enter a valid input:-")
        return 0


# Verify if input is empty
def verify(value):
    if not (value and not value.isspace()):
        print("You gave an empty input")
        print("Please enter the value again:-")
        return 0
    else:
        return 1


# Function to take an input for missing value
def filler():
    while 1:
        input_value = input()
        if verify(input_value):
            break
    return input_value


# Function to return the user choice to perform operation
def check_input(condition_list, process):
    while 1:
        input_value = str(input())
        if process == 0:
            if user_entry_check_major(condition_list, input_value):
                break
        else:
            if user_entry_check_minor(condition_list, input_value):
                break
    return input_value


# Functions to define the cleaning operations (categorical)
# Function to drop rows where there is missing categorical values
def quick_cat_drop(dataframe, column_name):
    temp_data = dataframe.dropna(axis=0, subset=column_name)
    reset_data = temp_data.reset_index(drop=True)
    return reset_data


# Function to auto-fill categorical missing values
def quick_cat_autofill(dataframe, column_name):
    print("\nYou chose to fill missing values with most common or least common values.")
    print("How do you want to fill the missing data?")
    print("1. Complete database at once\n2. Fill each column individually")
    print("Give your input:- ")
    minor_option = ['1', '2']
    menu_option_1 = check_input(minor_option, process_2)
    if menu_option_1 == '1':
        print("\nYou choose to Auto-fill the missing values of the complete database at once.")
        print("Which of the following Data do you want?")
        print("1. Most common\n2. Least common")
        print("Give your input:- ")
        menu_option_2 = check_input(minor_option, process_2)
        if menu_option_2 == '1':
            for column in column_name:
                temp_value = tuple(dataframe[column].mode())[0]
                dataframe[column] = dataframe[column].fillna(temp_value)
        if menu_option_2 == '2':
            for column in column_name:
                temp_value = dataframe[column].value_counts().index[-1]
                dataframe[column] = dataframe[column].fillna(temp_value)
    if menu_option_1 == '2':
        print("\nYou chose to Auto-fill missing value for each columns.")
        for column in column_name:
            temp_value_1 = tuple(dataframe[column].mode())[0]
            temp_value_2 = dataframe[column].value_counts().index[-1]
            print("The name of column you will fill is \"" + column + "\".")
            print("\nThe most common", column, "is", temp_value_1.upper(),
                  "and the least common is", temp_value_2.upper() + ".")
            print("Which of the following Data do you want?")
            print("1. Most common\n2. Least common")
            print("Give your input:- ")
            menu_option_2 = check_input(minor_option, process_2)
            if menu_option_2 == '1':
                dataframe[column] = dataframe[column].fillna(temp_value_1)
            if menu_option_2 == '2':
                dataframe[column] = dataframe[column].fillna(temp_value_2)
    clean_data = dataframe
    return clean_data


# Function to manually fill categorical missing values
def quick_cat_fill(dataframe, column_name):
    print("You choose to enter manual data.")
    print("There are 3 ways you can give manual entry.")
    print("Which of the following procedure you want to follow?")
    print("1. Give only one value to fill all missing values.")
    print("2. Enter specific value for each column.")
    print("3. Enter value for every cell with missing values. (CAUTION: This will take some time.)")
    print("\nEnter your choice:- ")
    minor_option = ['1', '2', '3']
    menu_option = check_input(minor_option, process_2)
    if menu_option == '1':
        print("Enter the data you want for all the missing values: ")
        missing_entry = filler()
        for column in column_name:
            dataframe[column] = dataframe[column].fillna(missing_entry)
    elif menu_option == '2':
        for column in column_name:
            print("Enter your data for column name:-", column)
            missing_entry = filler()
            dataframe[column] = dataframe[column].fillna(missing_entry)
    else:
        for column in column_name:
            for row_index in range(len(dataframe[column])):
                if dataframe[column].isnull()[row_index]:
                    print("This row has missing values:- ")
                    print(dataframe.loc[row_index])
                    print("Fill the missing value for:-")
                    print("Column:", column.upper(), "based on the data in columns stated above.")
                    print("Your input: ")
                    missing_entry = filler()
                    dataframe[column] = dataframe[column].fillna(value=missing_entry, limit=1)
    clean_data = dataframe
    return clean_data


# Function to ignore correction
def quick_cat_ignore(dataframe):
    return dataframe


# Functions to define the cleaning operations (numerical)
# Function to drop rows with missing numerical values
def quick_num_drop(dataframe, column_name):
    temp_data = dataframe.dropna(axis=0, subset=column_name)
    reset_data = temp_data.reset_index(drop=True)
    return reset_data


# Function to autofill missing numerical values
def quick_num_autofill(dataframe, column_name):
    print("\nYou chose to fill missing values with mean/median/mode or least common value.")
    print("How do you want to fill the missing data?")
    print("1. Complete database at once\n2. Fill each column individually")
    print("Give your input:- ")
    minor_option = ['1', '2']
    menu_option_1 = check_input(minor_option, process_2)
    minor_option_2 = ['1', '2', '3', '4', 'mean', 'median', 'mode',
                      'least common', 'least', 'leastcommon']
    if menu_option_1 == '1':
        print("\nYou choose to Auto-fill the missing values of the complete database at once.")
        print("Which of the following Data do you want?")
        print("1. Mean\n2. Median\n3. Mode\n4. Least Common")
        print("Give your input:- ")
        menu_option_2 = check_input(minor_option_2, process_2)
        if menu_option_2 in ['1', 'mean']:
            for column in column_name:
                temp_value = dataframe[column].mean()
                dataframe[column] = dataframe[column].fillna(temp_value)
        if menu_option_2 in ['2', 'median']:
            for column in column_name:
                temp_value = dataframe[column].median()
                dataframe[column] = dataframe[column].fillna(temp_value)
        if menu_option_2 in ['3', 'mode']:
            for column in column_name:
                temp_value = tuple(dataframe[column].mode())[0]
                dataframe[column] = dataframe[column].fillna(temp_value)
        if menu_option_2 in ['4', 'least common', 'least', 'leastcommon']:
            for column in column_name:
                temp_value = dataframe[column].value_counts().index[-1]
                dataframe[column] = dataframe[column].fillna(temp_value)
    if menu_option_1 == '2':
        print("\nYou chose to Auto-fill missing value for each columns.")
        for column in column_name:
            mean_value = dataframe[column].mean()
            median_value = dataframe[column].median()
            mode_value = tuple(dataframe[column].mode())[0]
            least = dataframe[column].value_counts().index[-1]
            print("The name of column you will fill is \"" + column + "\".")
            print("\nHere the mean is", mean_value, ", median is", median_value, "and the mode is",
                  mode_value, ".")
            print("Which of the following Data do you want?")
            print("1. Mean\n2. Median\n3. Mode\n4. Least Common")
            print("Give your input:- ")
            menu_option_2 = (check_input(minor_option_2, process_2)).lower()
            if menu_option_2 in ['1', 'mean']:
                dataframe[column] = dataframe[column].fillna(mean_value)
            if menu_option_2 in ['2', 'median']:
                dataframe[column] = dataframe[column].fillna(median_value)
            if menu_option_2 in ['3', 'mode']:
                dataframe[column] = dataframe[column].fillna(mode_value)
            if menu_option_2 in ['4', 'least common', 'least', 'leastcommon']:
                dataframe[column] = dataframe[column].fillna(least)
    clean_data = dataframe
    return clean_data


# Function to use Simple Impute
def quick_num_impute(dataframe, column_name):
    from sklearn.impute import SimpleImputer
    print("You choose to use Simple Impute.")
    print("Which of the following value you want to impute?")
    print("1. Mean\n2. Median\n3. Mode")
    print("Enter your choice:- ")
    minor_option = ['1', '2', '3']
    menu_option = check_input(minor_option, process_2)
    if menu_option.lower == ['1']:
        option = 'mean'
    elif menu_option.lower == ['2']:
        option = 'median'
    else:
        option = 'most_frequent'
    impute = SimpleImputer(strategy=option)
    impute.fit(dataframe[column_name])
    imputed_data = impute.transform(dataframe[column_name].values)
    dataframe[column_name] = imputed_data
    clean_data = dataframe
    return clean_data


# Function to manually fill missing numerical values
def quick_num_fill(dataframe, column_name):
    print("\nYou choose to enter manual data.")
    print("There are 3 ways you can give manual entry.")
    print("Which of the following procedure you want to follow?")
    print("1. Give only one value to fill all missing values.")
    print("2. Enter specific value for each column.")
    print("3. Enter value for every cell with missing values. (CAUTION: This will take some time.)")
    print("\nEnter your choice:- ")
    minor_option = ['1', '2', '3']
    menu_option = check_input(minor_option, process_2)
    if menu_option == '1':
        print("\nEnter the data you want for all the missing values: ")
        missing_entry = filler()
        for column in column_name:
            dataframe[column] = dataframe[column].fillna(missing_entry)
    elif menu_option == '2':
        for column in column_name:
            print("\nEnter your data for column name:-", column)
            missing_entry = filler()
            dataframe[column] = dataframe[column].fillna(missing_entry)
    else:
        for column in column_name:
            for row_index in range(len(dataframe[column])):
                if dataframe[column].isnull()[row_index]:
                    print("\nThis row has missing values:- ")
                    print(dataframe.loc[row_index])
                    print("\nFill the missing value for:-")
                    print("Column:", column.upper(), "based on the data in columns stated above.")
                    print("Your input: ")
                    missing_entry = filler()
                    dataframe[column] = dataframe[column].fillna(value=missing_entry, limit=1)
    clean_data = dataframe
    return clean_data


# Function to ignore filling numerical values
def quick_num_ignore(dataframe):
    return dataframe


# Function to define the switch functions
def switch(dataset, data_column, operation_choice, operation_type):
    if operation_type == 1:
        operation_list = ['quick_cat_drop(dataset, data_column)', 'quick_cat_autofill(dataset, data_column)',
                          'quick_cat_fill(dataset, data_column)', 'quick_cat_ignore(dataset)']
        index = int(operation_choice) - 1
        filtered_data = eval(operation_list[index])
        return filtered_data
    if operation_type == 2:
        operation_list = ['quick_num_drop(dataset, data_column)', 'quick_num_autofill(dataset, data_column)',
                          'quick_num_impute(dataset, data_column)', 'quick_num_fill(dataset, data_column)',
                          'quick_num_ignore(dataset)']
        index = int(operation_choice) - 1
        filtered_data = eval(operation_list[index])
        return filtered_data


def model_set(dataset):
    main_columns = list(tuple(dataset.columns))
    print("\nThe columns in this dataset are:-\n:::::::::::::::::::::::::::::::\n", main_columns, "\n")
    print("Type the name of columns you want to drop(separated by commas','and a space)"
          "\nPress enter to skip this operation or type 'exit' to terminate the program:-\n")
    user_entry = None
    if __name__ == '__main__':
        colom = column_choice(main_columns)
        user_entry = colom
    if user_entry == ['']:
        compact_data = dataset
    else:
        compact_data = dataset.drop(labels=user_entry, axis=1)
    return compact_data


# Checking the address of the CSV file entered by the user
def address_check(address):
    try:
        pd.read_csv(address)
        return 1
    except FileNotFoundError:
        print("\nYou entered a wrong address. Please, type the address again.")
        print("Type below:- ")
        return 0


# Creating a infinite loop until the user enters a valid output
def location_input():
    print("Enter the address of the CSV file including the name of the CSV:-\n")
    while 1:
        address = str(input())
        if address_check(address):
            break
    return address


# Main Program
print("\n*************************\nProgram Name:- QUICKWASH\n*************************\n")
print("Welcome to QuickWash, the program to quickly clean your sheet (ﾟ▽^*).\n")
location = location_input()
file = pd.read_csv(location)
pd.set_option('display.max_columns', None)
print("\n:::::::::::::::::::::::::::::::::")
print("The first 5 rows of the dataframe:\n:::::::::::::::::::::::::::::::::\n", file.head(5))
print("\n\n::::::::::::::::::::::::::::::::")
print("The last 5 rows of the dataframe:\n::::::::::::::::::::::::::::::::\n", file.tail(5))
print("\n:::::::::::::::::::::::::::::::")
print("Usually there may be a lot of unwanted columns in dataframe."
      " You can remove such unwanted columns.")
raw_data = model_set(file)
if raw_data.isnull().sum().sum() == 0:
    print("\nThe CSV file does not contain any missing values. Exiting program.")
    print("New csv file has been created with name:- (QUICKWASH dataset.csv)")
    raw_data.to_csv('QUICKWASH dataset.csv', index=False)
    exit()
# Separating data as objects and numerical
signal, choice = None, None
process_1, process_2 = 0, 1
operate_1, operate_2 = 1, 2
objects = raw_data.select_dtypes(include=object)
object_column = objects.columns.tolist()
continuous = raw_data.select_dtypes(exclude=object)
continuous_column = continuous.columns.tolist()
# Checking missing categorical values
print("\nChecking for categorical missing values:- ◕ ◡ ◕")
if objects.isnull().values.any():
    print("=======================================")
    print("\nDataframe contains missing categorical values.")
    obj_missing = objects.columns[objects.isna().any()].tolist()
    print("These columns have null values:-\n", obj_missing)
    # Performing Operations on missing Categorical values
    print("\n..................................................................")
    print("What operation would you like to perform for missing categorical values?")
    print("\t1. Remove the rows with missing categorical values.\n"
          "\t2. Fill missing values with most common or least common values\n"
          "\t3. Fill missing value with your own data.\n"
          "\t4. Ignore the operation and continue. (caution- Results may be unpredictable)\n"
          "\t5. Exit the program\n")
    print("Type the number representing the commands or type 'exit' to terminate the program:- ")
    expected_input = ['1', '2', '3', '4', '5']
    if __name__ == '__main__':
        return_signal = check_input(expected_input, process_1)
        signal = return_signal
    choice = signal
    object_data = switch(raw_data, object_column, choice, operate_1)
else:
    print("(No missing values)")
    object_data = raw_data
# Checking missing numerical values
print("\nChecking for numerical missing values:- ◕ ◡ ◕")
if continuous.isnull().values.any():
    print("=====================================")
    print("\nDataframe contains missing numerical values.")
    num_missing = continuous.columns[continuous.isna().any()].tolist()
    print("These columns have null values:-\n", num_missing)
    # Performing Operations on missing Numerical values
    print("\n......................................................................")
    print("What operation would you like to perform for missing numerical values?")
    print("\t1. Remove the rows with missing values.\n"
          "\t2. Fill missing values with mean/median or common values.\n"
          "\t3. Use Simple Impute\n"
          "\t4. Fill missing value with your own data.\n"
          "\t5. Ignore filling missing values and continue. (caution- Results may be unpredictable)\n"
          "\t6. Exit the program\n")
    print("Type the number representing the commands or type 'exit' to terminate the program:- ")
    expected_input = ['1', '2', '3', '4', '5', '6']
    if __name__ == '__main__':
        return_signal = check_input(expected_input, process_1)
        signal = return_signal
    choice = signal
    numerical_data = switch(object_data, continuous_column, choice, operate_2)
else:
    numerical_data = object_data
    print("(No missing values)")
    print("Clear to proceed\n\n")
final_data = numerical_data
print("\nYour data analysis is complete.")
csv_name = str(input("Give a name to the new csv file:- "))
print("\nYour CSV file has been created.")
name = csv_name + ".csv"
final_data.to_csv(name, index=False)
print("Thank you for using QUICKWASH.")
input("\nPress any key to exit.")
