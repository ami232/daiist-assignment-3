"""Demo for the report: unanswerable question before and after add_document (approval given on purpose)."""
import agent

QUESTION = "What is the age of digital consent that Spain has set under Article 8 of the GDPR?"

def show(title, result):
    print(f"\n===== {title} =====\n{result['answer']}\n[tool calls: {[c['name'] for c in result['calls']]}]")

show("BEFORE (document not indexed)", agent.ask(QUESTION, approve=lambda path: False))
show("ADD", agent.ask("Please add the file demo/spain-digital-consent-age.txt to the index.", approve=lambda path: True))
show("AFTER (document indexed)", agent.ask(QUESTION, approve=lambda path: False))
