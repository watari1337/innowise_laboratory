def generate_profile(age):
    """
    by user age return their life stage

    :param age: age of user
    :return: string, 1 word describing user life stage
    """
    if age >= 20: return "Adult"
    elif age >= 13: return "Teenager"
    elif age >= 0: return "Child"
    return None

if __name__ == "__main__":
    #collect name + age
    print("Enter your full name: ")
    user_name = input()
    print("Enter your birth year: ")
    birth_year_str = input()
    birth_year = int(birth_year_str)
    current_age = 2025 - birth_year

    life_stage = generate_profile(current_age)

    #collect hobbys
    hobbies = []
    while True:
        print("Enter a favourite hobby or type 'stop' to finish:")
        hobby = input()
        if hobby.lower() == "stop":
            break
        else:
            hobbies.append(hobby)

    #compare information
    user_profile = {
        "name": user_name,
        "age": current_age,
        "stage": life_stage,
        "hobbies": hobbies
    }
    print("\n---")
    print(f"Profile Summary:\nName: {user_name}\nAge: {current_age}\nLife Stage: {life_stage}")
    if len(hobbies) == 0: print("You didn't mention any hobbies")
    else:
        print(f"Favorite Hobbies ({len(hobbies)}):")
        for hobby in hobbies:
            print(f"- ", hobby)
    print("---")