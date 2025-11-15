def generate_profile(age):
    if age < 13:
        return "Child"
    elif age < 20:
        return "Teenager"
    else:
        return "Adult"

user_name = input("Enter your full name:")
birth_year_str = input("Enter your birth year:")
birth_year = int(birth_year_str)
from datetime import datetime 
current_age = datetime.now().year - birth_year
hobbies = list()
while True:
    hobbie = input("Enter a favorite hobby or type 'stop' to finish:")
    if (hobbie.lower() == "stop"):
        break
    hobbies.append(hobbie)

life_stage = generate_profile(current_age)
user_profile = {'name': user_name, 'age': current_age, 'stage': life_stage, 'hobbies': hobbies}
print(f"---\nProfile Summary:\nName: {user_profile['name']}\nAge: {user_profile['age']}\nLife Stage: {user_profile['stage']}")
if (hobbies):
    print(f"Favorite Hobbies ({len(hobbies)}):")
    for hob in hobbies:
        print(f"- {hob}") 
print("---")