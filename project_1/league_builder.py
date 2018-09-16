"""
Build a Soccer League
Aim is to divice players to equally balanced teams and send invite letters to families.
Creator: Serhat Bolsu
"""

import csv
import datetime

#Empty lists for creating teams and sharing between methods
all_players = []
Sharks = []
Dragons = []
Raptors = []

def parse_csv():
    """
    Parse CSV file and create a dictionary of all players
    :return: Update global `all_players` object as dictionary
    """
    with open('soccer_players.csv', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_players.append(row)


    print(all_players)
    print("Number of Players :" + str(len(all_players)))
    print(str(len(list(filter(lambda x: x['Soccer Experience'] == 'YES', all_players)))))


def divide_to_teams(players=all_players):
    """Equally divide players to Sharks, Dragons and Raptors"""
    # Find the experienced player number
    equal_number_of_exp = len(list(filter(lambda x: x['Soccer Experience'] == 'YES' , all_players))) // 3
    # Fill teams only for experienced players
    for player in all_players:
        if player['Soccer Experience'] == 'YES':
            if len(Sharks) < equal_number_of_exp :
                Sharks.append(player)
            elif len(Dragons) < equal_number_of_exp :
                Dragons.append(player)
            else:
                Raptors.append(player)

    # Fill teams only for NOT experienced players
    for player in all_players:
        if player['Soccer Experience'] == 'NO':
            if len(Sharks) < 6:
                Sharks.append(player)
            elif len(Dragons) < 6:
                Dragons.append(player)
            else:
                Raptors.append(player)

def write_welcome_letter(player, team):
    """Create Welcome letters in .txt files"""
    capitalized_name = player['Name'].split()
    file_name = capitalized_name[0].lower() + '_' + capitalized_name[1].lower() + '.txt'
    date_of_exercise = datetime.datetime.today() + datetime.timedelta(days=30)
    with open(file_name, 'w') as file:
        file.write('Dear {},'.format(player['Guardian Name(s)']) + '\n')
        file.write('We are glad to know that your -{}- has been accepted to school \n'.format(player['Name']) +
                   'Team name: {}'.format(team) + '\n'+
                   'First practice will be on: {}'.format(date_of_exercise.strftime("%d/%m/%Y %H:%M")) + '\n'+
                   'Please join this enjoyable date!')


def write_team_to_file():
    """Output team composition as an .txt file"""
    with open('teams.txt', 'w') as file:
        fieldnames = ['Name', 'Height (inches)', 'Soccer Experience', 'Guardian Name(s)']

        for team in [('Sharks', Sharks), ('Dragons', Dragons), ('Raptors', Raptors)]:
            file.write(team[0] + '\n')
            for p in team[1]:
                file.write((','.join((p['Name'], p['Soccer Experience'], p['Guardian Name(s)'])) + '\n'))
                write_welcome_letter(p, team[0])

            file.write('\n')
            file.write('\n')

if __name__ == '__main__':
    # Step by step execution of script
    parse_csv()
    divide_to_teams(all_players)
    write_team_to_file()
