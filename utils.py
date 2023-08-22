import os

def is_double(value):
    return isinstance(value, float)

def get_double_input():
    while True:
        user_input = input("Enter a threshold (between 0 and 1) for likeness of job titles: ")
        try:
            user_input = float(user_input)
            if is_double(user_input) and 0 <= user_input <= 1:
                return user_input
            else:
                print("Input must be a double between 0 and 1.")
        except ValueError:
            print("Invalid input. Please enter a valid double.")

def input_valid_file_path():
    while True:
        file_path = input('insert path like \nC:/Users/NiklasWernich/OneDrive - Diadrom Holding AB/Dokument/ALL_AB_Volvo_Postings.xlsx \n')

        if os.path.exists(file_path):
            return file_path
        else:
            print("The specified file path does not exist. Please provide a valid path.")

def VCC_or_AB():
    VCC = input("Is it postings for VCC -> y \nIs it postings for Volvo AB -> n: ")
    if (VCC == 'y' or VCC == 'n'):
        if VCC == 'y':
            return 'Job Posting Title'
        else :
            return 'Title'
    else :
        return VCC_or_AB()
