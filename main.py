import mysql.connector
import uuid
import time

def connect_to_database():
    yhteys = mysql.connector.connect(
        host='127.0.0.1',
        port=3306,
        database='game',
        user='root',
        password='12345salam',
        autocommit=True
    )
    return yhteys

def get_questions():
    sql = f"SELECT id, question, airport FROM questions"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    questions = cursor.fetchall()
    return questions

def get_answer(question_id):
    sql = f"SELECT answer FROM questions WHERE id = {question_id}"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    answer = cursor.fetchone()[0]
    return answer
def plane_types(types):
    global correct_answers

    sql = f"SELECT type FROM airplanes WHERE point_min <= {correct_answers} AND point_max >= {correct_answers} LIMIT 1;"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    answer = cursor.fetchone()
    if correct_answers == types:
        return answer[0]
    else:
        return None

def save_name(name):
    player_id = uuid.uuid4()  # Generate a random UUID for the player
    sql = "INSERT INTO game (id, screen_name, co2_consumed, co2_budget, location) VALUES (%s, %s, 0, 0, 'EFhk')"
    cursor = yhteys.cursor()
    cursor.execute(sql, (str(player_id), name))
    yhteys.commit()
    return player_id
def update_budget(player_id, co2_budget):
    sql = f"UPDATE game SET co2_budget = {co2_budget} WHERE id = '{player_id}'"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    yhteys.commit()
    return

def greetings(name):
    time.sleep(0.5)
    story = ("\nHello, " + name + "\n, after the spread of the virus in the city, \nhealthy people went to the airport to escape, \nbut most of the pilots were infected outside the airport, \nand since the number of people detained at the airport is large, \nyour mission is to save the largest possible number of people and get them out\nof the city through planes. Note that you must answer \nthe questions before operating the plane, and whenever \nIf you save more people, you get a reward. The reward is a larger \nplane that transports more people")
    words = story.split()
    for word in words:
        print(word, end=" ")
        time.sleep(0.1)

    save_name(name)
    questions = get_questions()
    return questions
def airport():
    sql = "select id, airport from questions"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    yhteys.commit()
    return
def play_game():
    while True:
        player_answer = input(f"\nDo you want to play? (yes/no): ").lower()
        if player_answer == "yes":
            return True
        elif player_answer == "no":
            return False
        else:
            print("Please enter yes or no")

def ask_questions(questions):
    correct_answers = 0
    for question in questions:
        print(f"Airport is {question[2]}" f"\n{question[0]}-{question[1]}" )
        player_answer = input("Enter your answer: ")
        if player_answer.lower() == get_answer(question[0]).lower():
            correct_answers += 5
            print(f"Correct! Get 5 points. You saved people!")
        else:
            print("Incorrect! You lose save people.")
    return correct_answers  # Only return correct_answers




yhteys = connect_to_database()
play_game()
playerName = input("What is your name?")
greetings(playerName)
questions = get_questions()


if play_game():
    correct_answers = ask_questions(questions)
    print("\nYou saved " + str(correct_answers) + " people.")
    if correct_answers > 0:
        player_id = save_name(playerName)  # Call save_name and capture the returned player_id
        update_budget(player_id, correct_answers)  # Pass both arguments
        plane_type = plane_types(correct_answers)
        print(f"\nCongratulations! You earned a reward. Your plane type is: {plane_type}")
    else:
        print("You didn't save any people.")
else:
    print("Thank you for playing.")


