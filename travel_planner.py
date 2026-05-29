tourist_places = {
    "Hyderabad":
        ["Charminar",
         "Golconda Fort",
         "Ramoji Film City"],

    "Vizag":
        ["RK Beach",
         "Kailasagiri",
         "Submarine Museum"],

    "Delhi":
        ["Red Fort",
         "India Gate",
         "Qutub Minar"]
}

budget = int(input("Enter Budget: "))

city = input("Enter City: ")

if city in tourist_places:

    print("\nRecommended Places")

    for place in tourist_places[city]:
        print(place)

    print("\nEstimated Cost:", budget)

else:
    print("City not found")
