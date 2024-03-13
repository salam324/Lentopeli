import mysql.connector
import uuid
import random

icao_codes = {
    1: "EBBR",
    2: "EDDF",
    3: "EFHK",
    4: "EKCH",
    5: "ESSA",
    6: "LEMD",
    7: "LFPG",
    8: "LOWW",
    9: "LPPR",
    10: "LSZH"
}


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
    sql = "SELECT question, id FROM questions"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    questions = cursor.fetchall()
    return questions


def get_question(icao):
    sql = "select question from questions where airport = " + "'" + icao + "'"
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
    sql = f"SELECT type FROM airplanes WHERE quantity = {types}"
    cursor = yhteys.cursor()
    cursor.execute(sql)
    answer = cursor.fetchone()
    if answer:
        if correct_answers == types:
            return answer[0]
        else:
            return None
    else:
        return None

def save_name(name):
    player_id = uuid.uuid4()  # Generate a random UUID for the player
    sql = "INSERT INTO game (id, screen_name, co2_consumed, co2_budget, location) VALUES (%s, %s, 0, 0, 'EFhk')"
    cursor = yhteys.cursor()
    cursor.execute(sql, (str(player_id), name))
    yhteys.commit()
    return

def greetings(name):
    print("\nHello, " + name + ", after the spread of the virus in the city, \nhealthy people went to the airport to escape, \nbut most of the pilots were infected outside the airport, \nand since the number of people detained at the airport is large, \nyour mission is to save the largest possible number of people and get them out\nof the city through planes. Note that you must answer \nthe questions before operating the plane, and whenever \nIf you save more people, you get a reward. The reward is a larger \nplane that transports more people")
    save_name(name)
    questions = get_questions()
    return questions

def play_game():
    while True:
        player_answer = input("Do you want to play? (yes/no): ").lower()
        if player_answer == "yes":
            return True
        elif player_answer == "no":
            return False
        else:
            print("Please enter yes or no")

def ask_questions(question):
    correct_answers = 0
    for i in range(len(questions)):
        location = icao_codes[random.randint(0, len(icao_codes) - 1)]
        print(location)
        get_question(location)
        get_question(location)
        player_answer = input("Enter your answer: ")
        if player_answer.lower() == get_answer(question[1]).lower():
            correct_answers += 5
            print("Correct!"
                  "ًyou save people")
        else:
            print("Incorrect!"
                  "you lose save people")
    return correct_answers


yhteys = connect_to_database()
playerName = input("What is your name?")
greetings(playerName)
questions = get_questions()


if play_game():
    correct_answers = ask_questions(questions)
    print("\nYou saved " + str(correct_answers) + " people.")
    if correct_answers > 0:
        print("Congratulations! You earned a reward.")
    else:
        print("You didn't save any people.")
else:
    print("Thank you for playing.")
if correct_answers == plane_types(correct_answers):
    print("\n your the plane" + str(correct_answers))
else:
    print("none")