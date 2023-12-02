import openai
import os
from IPython.display import Markdown,display_markdown
import time

openai.api_key = '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'


def ask_GPT4(system_intel, prompt):
    result = openai.ChatCompletion.create(model="gpt-4",
    messages=[{"role": "system", "content": system_intel},
              {"role": "user", "content": prompt}])   # openAI API
    # print (result['choices'][0]['message']['content'])
    display_markdown((result['choices'][0]['message']['content']))
    return result['choices'][0]['message']['content']

def ask_GPT4_multi_times(system_intel, history_messages, new_query, max_length=11): ### ask gpt multiple times, but with max query length. so it only support 5 rounds talking. 
#### If using GPT4-turbo, support more rounds of talking, but the delay is more. 
    current_time = time.time()
    if len(history_messages) == 0 or history_messages == None: # new topic 
        history_messages = []
        history_messages.append({"role": "system", "content": system_intel})
        history_messages.append({"role": "user", "content": new_query})
        answer = ask_GPT4(system_intel, new_query)
        history_messages.append({"role": "assistant", "content": answer})
        print(time.time() - current_time) 
        return answer, history_messages
    elif len(history_messages) < max_length: 
        history_messages.append({"role": "user", "content": new_query})
        answer = openai.ChatCompletion.create(model="gpt-4",messages=history_messages)['choices'][0]['message']['content']
        history_messages.append({"role": "user", "content": new_query})
        display_markdown(answer)
        print(time.time() - current_time) 
        return answer, history_messages
    else: # clear the messages
        display_markdown('Sorry, I only support 5 round talking, The historical context will be cleared')
        return 'Sorry, I only support 5 round talking, The historical context will be cleared', []




if __name__ == '__main__':
    system_intel = "My name is Sam.I am an elder person who is 80 years old.Please talk to me.please keep your answer as short as possible. Answer me as my 30 years old child"
    prompt = 'how to keep healthy' 
    history_messages = []
    while True:   ### test
        prompt = input("Please ask me question：")
        answer, history_messages = ask_GPT4_multi_times(system_intel, history_messages, prompt)
