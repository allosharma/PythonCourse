from google import genai
from google.genai import types

client = genai.Client()

with open("system_instruction.txt", "r") as file:
    system_instruction_from_file = file.read()

# Define the generation configuration with default controls
config = types.GenerateContentConfig(
    # System Instruction (sets the 'persona' or ground rules)
    system_instruction= system_instruction_from_file,
    
    # Sampling Parameters
    temperature=1.0,            # Range: 0.0 - 2.0 (1.0 is default for balanced creativity)
    top_p=0.95,                 # Nucleus sampling threshold
    top_k=40,                   # Top-k sampling (limits the pool of next-token candidates)
    
    # Output Limits
    max_output_tokens=4096,     # Limits the length of the generated response
    
    # Stop Criteria
    stop_sequences=["STOP"],    # Model will stop generating if it produces this string
    
    # Optional: Safety Settings
    safety_settings=[
        types.SafetySetting(
            category="HARM_CATEGORY_HARASSMENT",
            threshold="BLOCK_MEDIUM_AND_ABOVE"
        )
    ]
)

# Execute the request
response = client.models.generate_content(
    model="gemma-4-31b-it",
    contents="You are given an opportunity to set paper for IIT JEE paper for physics, chemistry and mathematics. \
    You have to set 25 questions from each subject. Each question should be of 4 marks and should be of easy, moderate and hard difficulty level.\
        You have to set the question in such a way that it covers the entire syllabus of JEE.\
            You have to set the question in such a way that it is not repeated in the past 10 years papers.\
                You response hsould have the question with 4 options and then followed by the ansswer and that followed by explanation.\
                    Your resopnse must be in json format\
                        For this response only give our question for physics.\
                            **Option A:** I provide the **Full Physics Paper** (25 Questions) first, then Chemistry, then Maths.",
    config=config
)

print(response.text)