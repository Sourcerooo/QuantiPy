class SimpleStatistic:
    def __init__(self):
        self.gain_loss = 0
        self.gain_loss_pct = 0
        self.profit_factor = 0
        self.max_drawdown = 0
        self.max_drawdown_pct = 0
        self.high_gain_loss = 0
        self.low_gain_loss = 0
        self.dd_occurred = False

    def calculate(self, cost, gain_loss):
        if gain_loss >= self.high_gain_loss:
            # New equity high, reset parameters
            if self.dd_occurred:
                self.dd_occurred = False
                self.low_gain_loss = self.high_gain_loss
            self.high_gain_loss = gain_loss
        else:
            if not self.dd_occurred:
                self.low_gain_loss = gain_loss
            elif gain_loss < self.low_gain_loss:
                self.low_gain_loss = gain_loss
            self.dd_occurred = True

        if abs(self.high_gain_loss - self.low_gain_loss) > self.max_drawdown:
            self.max_drawdown = abs(self.high_gain_loss - self.low_gain_loss)
            self.max_drawdown_pct = self.max_drawdown / (cost + self.high_gain_loss)
        self.gain_loss = gain_loss
        if cost != 0:
            self.gain_loss_pct = gain_loss / cost
        else:
            self.gain_loss_pct = 0

    def output(self, date):
        print("----------------------------")
        print("  Statistics for {}".format(date))
        print("- Total Gain/Loss: {}".format(self.gain_loss))
        print("- Perc  Gain/Loss: {}".format(self.gain_loss_pct))
        print("- Max    Drawdown: {}".format(self.max_drawdown))
        print("- Max Perc DD    : {}".format(self.max_drawdown_pct))
        print("----------------------------")