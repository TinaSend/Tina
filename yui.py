from arc_rig.core import Agent

class UmeAgent(Agent):
    def __init__(self, config_path):
        super().__init__(config_path)
    
    def run(self):
        self.say("Hello, I'm Ume! Ready to help you with your tasks.")
        while True:
            task = self.listen()
            if task == "exit":
                self.say("Goodbye!")
                break
            self.handle_task(task)

    def handle_task(self, task):
        response = self.reason(task)
        self.say(response)

if __name__ == "__main__":
    ume = UmeAgent("agents/ume_agent.yaml")
    ume.run()

#sendd it
