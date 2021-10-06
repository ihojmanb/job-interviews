import re
import time
from fight.fight import *
from teams.teams import *

regex = r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b"


class Client:
    """
    Client class stores user input, prints the fight information,
    and announces the winner to the end user.
    """

    def __init__(self, fight_admin: FightAdmin):
        self._client_name = ""
        self._client_email = ""
        self._fight_admin = fight_admin

    @property
    def client_name(self):
        return self._client_name

    @client_name.setter
    def client_name(self, client_name):
        self._client_name = client_name

    @property
    def client_email(self):
        return self._client_email

    @client_email.setter
    def client_email(self, client_email):
        self._client_email = client_email

    def welcome_user_and_ask_name(self):
        name = input("Bienvenido a TokuFight! Por favor, ingresa tu nombre: \n")
        return name

    def validate_email(self, email):
        if re.fullmatch(regex, email):
            return email
        else:
            raise ValueError

    def ask_for_valid_email(self):

        try:
            email = input("email: ")
            self.validate_email(email)
            return email

        except ValueError:
            print(
                "ups, parece que no es un email válido. Por favor inténtalo de nuevo. \n"
            )
            return self.ask_for_valid_email()

    def ask_user_input(self):
        name = self.welcome_user_and_ask_name()
        print(f"{name}, antes de comenzar por favor ingresa tu email: \n")
        email = self.ask_for_valid_email()
        print(f"tu email '{email}' es válido!\n")
        time.sleep(1)
        print("Ahora, procedamos a la pelea >:) \n")
        time.sleep(1)

    def present_teams(self):
        time.sleep(1)
        print("A continuación, te presentaremos los dos equipos.\n")
        time.sleep(1)
        for team in self._fight_admin.teams:
            print(f"""
            {team.name}:
            """)
            for member in team.members:
                print(f"{member.name}\n")
            time.sleep(3)

    def start_fight(self):
        time.sleep(1)
        print('Genial! Que comience la pelea!\n')
        self._fight_admin.start_fight()
        # self.hooligans()
        team1, team2 = self._fight_admin.teams
        attack_choice = ['mental_attack', 'strong_attack', 'fast_attack']
        fighter1 =team1.actual_fighter
        fighter2 =team2.actual_fighter
        self.present_fighters(team1, team2)

        while(not isinstance(self._fight_admin.state, FightEnded)):
            if(fighter1 != team1.actual_fighter or fighter2 != team2.actual_fighter):
                self.present_fighters(team1, team2)
                
            self.show_health_points(team1, team2)

            if team1.actual_fighter.health_points > 0:
                team1_attack = random.choice(attack_choice)
                team1.attack(team1_attack)
                attack_damage = team1.actual_fighter.__getattribute__(team1_attack)
                print(f'{fighter1.name} attack damage: {attack_damage}')
                time.sleep(1)
                
            if(fighter1 != team1.actual_fighter or fighter2 != team2.actual_fighter):
                defeated_character = self._fight_admin.defeated_character
                print(f'{defeated_character.name} ha sido derrotado.\n')
                self.present_fighters(team1, team2)
                fighter1 =team1.actual_fighter
                fighter2 =team2.actual_fighter
            
            self.show_health_points(team1, team2)


            if team2.actual_fighter.health_points > 0:
                team2_attack = random.choice(attack_choice)
                team2.attack(team2_attack)
                attack_damage = team2.actual_fighter.__getattribute__(team2_attack)
                print(f'{fighter2.name} attack damage: {attack_damage}')
                time.sleep(1)

            if(fighter1 != team1.actual_fighter or fighter2 != team2.actual_fighter):
                defeated_character = self._fight_admin.defeated_character
                print(f'{defeated_character.name} ha sido derrotado.\n')
                self.present_fighters(team1, team2)
                fighter1 =team1.actual_fighter
                fighter2 =team2.actual_fighter

        defeated_character = self._fight_admin.defeated_character
        print(f'{defeated_character.name} ha sido derrotado.\n')
    
    def fight_summary(self):
        winner_team = self._fight_admin.winner
        print(f'Enhorabuena, ha ganado {winner_team.name}\n')


    def present_fighters(self, team1, team2):
        team1, team2 = team1, team2
        print(f"""
        ¡Nueva pelea!
        | {team1.actual_fighter.name} V/S {team2.actual_fighter.name} |
        """)

    def show_health_points(self, team1, team2):
        team1, team2 = team1, team2
        fighter1 =team1.actual_fighter
        fighter2 =team2.actual_fighter
        print(f"""
        {fighter1.name} HP: {fighter1.health_points}
        {fighter2.name} HP: {fighter2.health_points}
        """)
    
    def hooligans(self):
        for i in range(10):
            print("¡FIGHT, FIGHT, FIGHT!")
            time.sleep(1)

def main():
    print('Cargando la simulación... Por favor espera.')
    superhero_api_consumer = SuperHeroApiConsumer(credentials["access-token"])
    character_factory = CharacterFactory(api_consumer=superhero_api_consumer)
    list_of_random_characters = superhero_api_consumer.get_random_list_of_characters(10)
    team_creator = TeamCreator(character_factory=character_factory)
    team1 = team_creator.build_team(
        team_name="Equipo 1", list_of_characters=list_of_random_characters[0:2]
    )
    team2 = team_creator.build_team(
        team_name="Equipo 2", list_of_characters=list_of_random_characters[2:4]
    )    
    fight_mediator = FightMediator(team1=team1, team2=team2)
    fight_admin = FightAdmin(fight_mediator)
    client = Client(fight_admin)
    client.ask_user_input()
    client.present_teams()
    client.start_fight()
    client.fight_summary()
main()
