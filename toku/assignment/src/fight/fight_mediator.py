class Mediator:
    """
    The Mediator interface declares a method used by components to notify the
    mediator about various events. The Mediator may react to these events and
    pass the execution to other components.
    """
    def __init__(self, admin) -> None:
        self._admin = admin

    @property
    def admin(self):
        return self._admin
        
    @admin.setter
    def admin(self, admin) -> None:
        self._admin = admin

    def notify_attack(self, sender: object, damage: int) -> None:
        pass

    def notify_end_fight(self, sender: object) -> None:
        pass

class FightMediator(Mediator):
    def __init__(self, team1, team2):
        self._team1 = team1
        self._team1.mediator = self
        self._team2 = team2
        self._team2.mediator = self

    @property
    def team1(self):
        return self._team1

    @property
    def team2(self):
        return self._team2

    def notify_attack(self, sender: object, damage: int)-> None:
        if sender == self.team1:
            self.team2.receive_damage(damage)
            
        elif sender == self.team2:
            self.team1.receive_damage(damage)

    def notify_end_fight(self, sender: object) -> None:
        if sender == self.team1:
            self.admin.winner = self.team2
            self.admin.end_fight()

        elif sender == self.team2:
            self.admin.winner = self.team1
            self.admin.end_fight()

    def notify_defeat(self, sender: object) -> None:
        self.admin.defeated_character = sender