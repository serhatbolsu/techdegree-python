import csv
import datetime


all_players = []
Sharks = []
Dragons = []
Raptors = []

def parse_csv():
    with open('soccer_players.csv', newline='') as file:
        reader = csv.DictReader(file)
        for row in reader:
            all_players.append(row)


    print(all_players)
    print("Number of Players :" + str(len(all_players)))
    print(str(len(list(filter(lambda x: x['Soccer Experience'] == 'YES', all_players)))))


def divide_to_teams(players=all_players):
    equal_number_of_exp = len(list(filter(lambda x: x['Soccer Experience'] == 'YES' , all_players))) // 3
    for player in all_players:
        if player['Soccer Experience'] == 'YES':
            if len(Sharks) < equal_number_of_exp :
                Sharks.append(player)
            elif len(Dragons) < equal_number_of_exp :
                Dragons.append(player)
            else:
                Raptors.append(player)

    for player in all_players:
        if player['Soccer Experience'] == 'NO':
            if len(Sharks) < 6:
                Sharks.append(player)
            elif len(Dragons) < 6:
                Dragons.append(player)
            else:
                Raptors.append(player)

def write_welcome_letter(player, team):
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
    with open('teams.txt', 'w') as file:
        fieldnames = ['Name', 'Height (inches)', 'Soccer Experience', 'Guardian Name(s)']

        for team in [('Sharks', Sharks), ('Dragons', Dragons), ('Raptors', Raptors)]:
            file.write(team[0] + '\n')
            for p in team[1]:
                file.write((','.join((p['Name'], p['Soccer Experience'], p['Guardian Name(s)'])) + '\n'))
                write_welcome_letter(p, team[0])
                # file.write()
            file.write('\n')
            file.write('\n')

if __name__ == '__main__':
    parse_csv()
    divide_to_teams(all_players)
    write_team_to_file()
