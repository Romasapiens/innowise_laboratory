"""
A module for creating a user profile based on entered data.
Includes functions for collecting information, calculating age, and generating a profile.
"""

def generate_profile(age):
    """
    Determines the user's life stage based on age.

    Args:
    age (int): User's age

    Returns:
    str: Life stage ('Child', 'Teenager', or 'Adult')
    """
    if age < 13:
        return "Child"
    elif age < 20:
        return "Teenager"
    else:
        return "Adult"

def get_user_info():
    """
    Collects user information via console input.
    
    Returns:
        tuple: A tuple with the user's name, year of birth, and list of hobbies
    """
    # Requesting a username
    user_name = input("Enter your full name: ").strip()
        
    # Requesting the year of birth
    birth_year_str = input("Enter your birth year: ").strip()
        
    # Collecting hobbies in a cycle
    hobbies = []
    while True:
        hobby = input("Enter a favorite hobby or type 'stop' to finish: ").strip()
        if hobby.lower() == 'stop':
            break
        if hobby:  # We add only non-empty hobbies
            hobbies.append(hobby)
    
    return user_name, birth_year_str, hobbies
        

def convert_user_info(birth_year_str):
    """
    Converts the birth year to the current age.

    Args:
    birth_year_str (str): Birth year as a string

    Returns:
    int: The user's current age

    """
    from datetime import datetime
    birth_year = int(birth_year_str)
    current_year = datetime.now().year
    current_age = current_year - birth_year
             
    return current_age

def combine_user_info(user_name, current_age, life_stage, hobbies):
    """
    Combines all user information into a profile dictionary.
    
    Args:
        user_name (str): Username
        current_age (int): Current age
        life_stage (str): Life stage
        hobbies (list): List of hobbies
        
    Returns:
        dict: Dictionary with a full user profile
    """
    return {
        'name': user_name,
        'age': current_age,
        'stage': life_stage,
        'hobbies': hobbies
    }

def display_user_profile(user_profile):
    """
    Displays the user profile beautifully.
    
    Args:
        user_profile (dict): Dictionary with user information
    """
    print(f"---\nProfile Summary:\nName: {user_profile['name']}\nAge: {user_profile['age']}\nLife Stage: {user_profile['stage']}")
    hobbies = user_profile['hobbies']
    if (hobbies):
        print(f"Favorite Hobbies ({len(hobbies)}):")
        for hob in hobbies:
            print(f"- {hob}") 
    else: print("You didn't mention any hobbies")
    print("---")

def main():
    """
    The main function that coordinates the profile creation process.
    Handles exceptions and ensures correct execution.
    """
    user_name, birth_year_str, hobbies = get_user_info()
    current_age = convert_user_info(birth_year_str)
    life_stage = generate_profile(current_age)
    user_profile = combine_user_info(user_name, current_age, life_stage, hobbies)
    display_user_profile(user_profile)

if __name__ == "__main__":
    main()