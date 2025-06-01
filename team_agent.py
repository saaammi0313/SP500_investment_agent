from valuation_agent import ValuationAgent
from technical_agent import TechnicalAgent

class TeamAgent:
    def __init__(self, agents):
        self.agents = agents

    def run(self, ticker="AAPL"):
        print(f"\nRunning analysis for {ticker} with {len(self.agents)} agents...\n")
        results = {}
        for agent in self.agents:
            name = agent.get_name()
            print(f"--- {name} ---")
            result = agent.run(ticker)
            print(result + "\n")
            results[name] = result
        # Output summary
        print("=== Team Summary ===")
        for name, result in results.items():
            print(f"{name}:\n{result}\n")
        print("(You can add more agents to the team by subclassing Agent and adding to the list!)")

if __name__ == "__main__":
    agents = [ValuationAgent(), TechnicalAgent()]
    team = TeamAgent(agents)
    team.run("AAPL")
