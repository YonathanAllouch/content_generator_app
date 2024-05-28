from openai import OpenAI
client = OpenAI()

response = client.beta.threads.delete("thread_eqKPWLqzdItDx8PV223i44al")
print(response)
