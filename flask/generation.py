import openai

#openai.api_key = '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'
openai.api_key = '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' #my key
#whisper_output = 'hey, so what I want is to get an image of an astronaut flying on a unicorn with blue flames in space'
#whisper_output = "I've got a basic idea for the image, What we need is to make a human from future, probably from year 2500 posing a selfie"
#whisper_output = "So basically what I want is, to generate an image where an astronaut is resting in space resort "
#whisper_output = "so the image that I'm looking for is an image of a cat wearing a tuxedo"  
#whisper_output = "I'm looking for an image which was photo of the year of a tuxido cat 35mm with dramatic lights captured from canon f2.5 and magnificent cover"
#whisper_output = 'Generate an image of a nurse'
#image_description = 'A cat wearing a tuxedo'
def find_keywords(sentence):
    response = openai.Completion.create(
      model="text-davinci-002",
#    prompt=f"extract key words from the given sentence\nsentence:This is a modern fiction story\nkeywords: Modern fiction\nsentence:This story is written for children\nkeywords: children\nsentence:The story is set in a park in a neighborhood\nkeywords: park \nsentence: The story is about friendship, teamwork, and courage.\nkeywords: friendship, teamwork, courage\nsentence: The story is set in Nathan's house and the temple in Albania\nkeywords: temple of Albania\nsentence: any\nkeywords: any\nsentence: {sentence}\nkeywords: ",
#    prompt = f'Extract key words from the given sentence. Create a summarized sentence fragment with original meaning using keywords\nsentence {sentence}\n summarized sentence:',
    prompt = f'Summarize the given sentence.\nsentence: {sentence}\nsummarized sentence:',
      temperature=0,
      max_tokens=30,
      frequency_penalty=0,
      presence_penalty=0,
    )
    for i in response.choices:
        print(i.text)
    text = response.choices[0].text
    return text
def extract_important(sentence):
    response = openai.Completion.create(
      model="text-davinci-002",
    prompt = f'extract the image description from sentence \n sentence:{sentence}\nimage description:',
      temperature=0,
      max_tokens=50,
      frequency_penalty=0,
      presence_penalty=0,
    )
    for i in response.choices:
        print(i.text)
    text = response.choices[0].text
    return text


def generate_camera_description(sentence):
    response = openai.Completion.create(
      model="text-davinci-002",
      prompt = 'given the image description, generate the following\n1 camera name\n2 Lens\n3 type of shot\n4 iso settings\n5 light\nimage quality\nsentence:{}\nsettings',
#    prompt = f'given the image description, generate iso settings in numeric formfor the perfect image\n sentence: Generate an image of a nurse\n iso settings: ISO 100, aperture 5.6, shutter speed 1/125 sec.\nsentence:{sentence}\iso settings:',
      temperature=0.7,
      max_tokens=50,
      frequency_penalty=0,
      presence_penalty=0,
      n=1,
    )
    for i in response.choices:
        print(i.text)
    text = response.choices[0].text
    return text

def get_dalle_prompt(whisper_output):
  image_description = extract_important(whisper_output)
  index = 0
  while True:
    camera_options = generate_camera_description(image_description)
    for i in range(len(camera_options)):
      if camera_options[i][0]=='1':
        index=i
        break
    camera_options = camera_options[index:]

    camera_options = camera_options.lstrip()
    camera_options = camera_options.split('\n')
    output = image_description
    flag = True
    for i in camera_options:
      line = i.split('.',1)
      if len(line)!=2:
        line = i.split(':',1)
        if len(line)!=2:
          flag = False
          break
      output+=f',{line[-1]}'
    if flag:
      break
  print(output)
  return output

def generate_dalle_image(description):
  img_response=openai.Image.create(prompt = description,n=1,size="512x512")
  print(img_response)
  return img_response['data'][0]['url']

def transcribe_audio(base_model,audio_path):
  result = base_model.transcribe(audio_path)
  print(result['text'])
  return result['text']
