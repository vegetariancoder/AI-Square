from chains.classify_chain import classify_chain
from chains.reply_chain import reply_chain



ticket = input("Enter support ticket: ")

print("\n--- Classification ---")
category = classify_chain.invoke({"ticket": ticket})
print(category.content)

print("\n--- Suggested Reply ---")
reply = reply_chain.invoke({"ticket": ticket})
print(reply.content)



# stream process
# ticket = input("Enter support ticket: ")
#
# print("\n--- Classification ---")
# category = classify_chain.stream({"ticket": ticket})
# for i in category:
#     print(i.content, end="")
#
# print("\n--- Suggested Reply ---")
# reply = reply_chain.stream({"ticket": ticket})
# for i in reply:
#     print(i.content, end="")


# batch process
# tickets = [
#     {"ticket": "I was charged twice"},
#     {"ticket": "I cannot login"},
#     {"ticket": "Please add dark mode"}
# ]
#
# results = classify_chain.batch(tickets)
#
# print(results[0])