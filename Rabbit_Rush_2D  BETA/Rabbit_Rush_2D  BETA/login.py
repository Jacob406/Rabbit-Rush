def login():
    username = input("Please enter your username: ")
    password = input("Enter your password: ")

    new_file = open("users.txt", "r")
    users_2d = eval(new_file.read())
    new_file.close()

    found = False
    for count in range(len(users_2d)):
        if username == users_2d[count][0]:
            found = True
            if password == users_2d[count][1]:
                print("logged in")
                execfile('file.py')
            else:
                print("incorrect password")
                login()

    if found == False:
        print("invalid username")
        login()

login()
