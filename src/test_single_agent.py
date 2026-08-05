from services.single_review_agent import SingleReviewAgent

code = """
x = None
print(x.upper())
"""

agent = SingleReviewAgent()

result = agent.execute(code)

print(result)