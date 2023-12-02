from speechre import speech_recognition_api
from gptApi import ask_GPT4, ask_GPT4_multi_times
from text2audio import text_to_speech
import time

hotKeys = ["hello gpt", "thank you gpt"] ### start and stop words
responses = {
            "hello gpt" : "Hi,What can i do for you?",
            "thank you gpt" : "Have a nice day!"
}
model = 'google' 
def chat_response(input_filename,output_filename): # ask gpt one time
    time_start = time.time() # cal delay
    voice_file = input_filename

    question,delay = speech_recognition_api(voice_file,model) # text to audio api 
    print(question)
    time_after_speechrec = time.time()
    print('delay of speech recognition: ',time_after_speechrec - time_start)
    system_intel = "My name is Sam.I am an elder person who is 80 years old.Please talk to me.please keep your answer as short as possible. Answer me as my 30 years old child"
    answer = ask_GPT4(system_intel,question) ## ask gpt once
    
    time_ask_gpt = time.time()
    print('delay of GPT response: ',time_ask_gpt - time_after_speechrec)
    text_to_speech(answer,output_filename) 
    time_text_speech = time.time()
    time_answer = time_text_speech - time_ask_gpt
    print('delay of text to speech: ',time_answer)
    
def chat_response_with_key_words(input_filename,output_filename,current_state,history_messages):
    time_start = time.time()
    voice_file = input_filename
    #voice_file = 'voice.mp3'
    question,delay = speech_recognition_api(voice_file,model)
    time_after_speechrec = time.time()
    print('delay of speech recognition: ',time_after_speechrec - time_start)
    question = question.lower()
    print(question)
    if question.find(hotKeys[0]) != -1 and current_state == 'silence'  : # if the state is silence, and receive 'hello gpt', start talking
        text_to_speech(responses[hotKeys[0]],output_filename) # response 'what can i do for u'
        return 'chatting',[]
    elif question.find(hotKeys[1]) != -1 and current_state == 'chatting':# if the state is chatting, and receive 'thank u gpt', make it stop 
        text_to_speech(responses[hotKeys[1]],output_filename)
        return 'stop',[]
    elif current_state == 'chatting' and question == 'error':      # if the state is chatting but the user did not talk anything
        text_to_speech('i did not hear you talking, please talk to me',output_filename)
        return 'chatting', history_messages
    elif current_state == 'chatting': # if the state is chatting, keep tracking the historical messages
        system_intel = "My name is Sam.I am an elder person who is 80 years old.Please talk to me.please keep your answer as short as possible. Answer me as my 30 years old child"
        answer,history_messages = ask_GPT4_multi_times(system_intel,history_messages,question)
        time_ask_gpt = time.time()
        print('delay of GPT response: ',time_ask_gpt - time_after_speechrec)
        text_to_speech(answer,output_filename)
        time_text_speech = time.time()
        time_answer = time_text_speech - time_ask_gpt
        print('delay of text to speech: ',time_answer)
        return 'chatting', history_messages
    return 'silence',[]
if __name__ == '__main__':
    chat_response('voice.mp3','chatgptresult.mp3')
       
