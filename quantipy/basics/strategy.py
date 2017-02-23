import quantipy.system.base as base_system
import uuid


class Strategy(object):
    """ This class will hold all strategy data and trigger the system evaluation process """
    def __init__(self, **kwargs):
        self.id = uuid.uuid4()
        self.name = ""
        self.description = ""
        self.account_id = ""
        self.eval_from = ""
        self.eval_to = ""
        self.incl_commision = False
        self.incl_slippage = False
        self.compound = False
        self.risk_money = 0.0
        self.risk_pct = 0.0
        self.results = {}
        self.systems = {}

    def load_from_db(self, database):
        pass

    def evaluate_systems(self, eval_systems=[]):
        if eval_systems:
            for i in eval_systems:
                self.results[self.systems[i].ID] = self.systems[i].run()
        else:
            for system in self.systems:
                self.results[system.ID] = system.run()

        for i in range(5):
            r = base_system.create_system_result()
            self.results[str(i)] = r




