import csv
def data():
    n = int (input ("how many datas elements you want to enter?-->"))
    name=[]
    for i in range(n):
        name.append(input(f"enter name of index no.{i}-->"))
    # Save to file


    with open("names.csv", "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerow(name)

    print("Names saved permanently in 'names.csv'")
    with open("names.csv", "r") as file:
        reader = csv.reader(file)
        names = next(reader)
    print(names)
    print ("name saved permanently?")
data()