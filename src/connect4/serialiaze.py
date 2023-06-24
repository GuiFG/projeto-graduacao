import json


with open('qlearn.json', 'r') as file:
    result = json.load(file)


    count = 0
    for value in result.values():
        print(value)

        if count > 100:
            break

        count += 1

    print(len(result))