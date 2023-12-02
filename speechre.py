import whisper
import speech_recognition as sr 
import time

IBM_KEY='XXXX-XXXX'
def whisper_recognition(audio_path):
    timeStart = time.time() 
    model = whisper.load_model("small") # whisper model choice
    model.FP16 = True
    result = model.transcribe(audio_path)
    #print("whisper results: ", result["text"])
    text = result["text"]
    delay = time.time() - timeStart
    return text,delay

def speech_recognition_api(inFile,model): # fuse all models into one method
    """
    IMPORT: string
    EXPORT: string
    PURPOSE: listen to the resident using an online module. Except the responses
    will be handled by saving to file. Hence, audio files are saved
    and read in from file
    """
    timeStart = time.time()
    r = sr.Recognizer() #build Recognizer
    contents = sr.AudioFile(inFile)
    text = 'ERROR'
    with contents as source:
        audio = r.record(source)
        try:
            if model == 'google':
                text = r.recognize_google(audio)
                delay = time.time()-timeStart
            elif model == 'bing':
                text = r.recognze_bing(audio)
                delay = time.time()-timeStart
            elif model == 'ibm':
                text = r.recognze_ibm(audio,IBM_KEY)
                delay = time.time()-timeStart
            elif model == 'whisper':
                text,delay = whisper_recognition(inFile)
        except sr.UnknownValueError as err:
            text = 'ERROR'
            delay = -1
            print("couldn't hear what you were saying")
    
    return text,delay

#voice_list = ['./'+ str(i)+'.mp3' for i in range(1,4)]
if __name__ == '__main__':
    import csv
    import os

    folder_path = './voice_dataset'
    file_list = os.listdir(folder_path)
    file_list.sort()
    voice_list = [folder_path + '/'+file_list[i] for i in range(100)]
    output_data = []
    for voice in voice_list: # record the delay and performance, for evaluation
        print(voice)
        text,delay = speech_recognition_api(voice, 'google')
        print('google',';',voice,';', text, ';', delay)
        output_data.append(['google',voice,text,delay])
        text1,delay1 = whisper_recognition(voice)
        print('whisper',';',voice,';', text1, ';', delay1)
        output_data.append(['whisper',voice,text1,delay1])

    # open the file
    with open('data.csv', 'w', newline='') as file:
        # create csv object
        writer = csv.writer(file)
        # header
        writer.writerow(['model', 'filename', 'translated_text','delay'])
        # data
        writer.writerows(output_data)

