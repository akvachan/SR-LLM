logging.set_verbosity(logging.CRITICAL)
pipe = pipeline(task="text-generation", model=model, tokenizer=tokenizer, max_length=1000)

def build_prompt(system_message, feedback):
  prompt = "<s>" + "[INST]" + system_message + "/n" + feedback + "[/INST]"
  return prompt

system_message = ""
question = ""
prompt = build_prompt(system_message, question)
result = pipe(prompt)

print(result[0]['generated_text'])

from peft import PeftModel, PeftConfig
from transformers import AutoModelForCausalLM

config = PeftConfig.from_pretrained("arseniikvachan/FrozenLake-Mistral")
base_model = AutoModelForCausalLM.from_pretrained("mistralai/Mistral-7B-Instruct-v0.2")
model = PeftModel.from_pretrained(base_model, "arseniikvachan/FrozenLake-Mistral")

df_test=pd.read_csv(test_path)

questionCounter=0
correct=0
promptEnding = "[/INST]"

# this must be >= 2
fail_limit=10

# chain of thought activator, model might run out of output tokens
USE_COT=True

#this comes before the question
testGuide='Answer the following question, at the end of your response write the answer like this: Answer:a or Answer:b or Answer:c or Answer:d \n'

for index, row in df_test.iterrows():
    print("#############################")
    questionCounter = questionCounter + 1

    #chain of thought activator
    if USE_COT:
        chainOfThoughtActivator='\nfirst think step by step\n'
    else:
        chainOfThoughtActivator='\n'

    #build the prompt
    question=testGuide + row['Question'] + '\na)' + row['a'] + '\nb)' + row['b'] + '\nc)' + row['c'] + '\nd)' + row['d'] + chainOfThoughtActivator
    print(question)

    #true answer
    truth=row['Answer']

    #use a loop, if llm stopped before reaching the answer. ask again
    index=-1
    failCounter=0
    while(index==-1):

        #build the prompt
        prompt = build_prompt(question)

        #generate answer
        result = pipe(prompt)
        llmAnswer = result[0]['generated_text']

        #remove our prompt from it
        index = llmAnswer.find(promptEnding)
        llmAnswer = llmAnswer[len(promptEnding)+index:]

        print("LLM Answer:")
        print(llmAnswer)

        #remove spaces
        llmAnswer=llmAnswer.replace(' ','')

        #find the option in response
        index = llmAnswer.find('Answer:')

        #edge case - llm stoped at the worst time
        if(index+len('Answer:')==len(llmAnswer)):
            index=-1

        #update question for the next try. remove chain of thought
        question=testGuide + row['Question'] + '\na)' + row['a'] + '\nb)' + row['b'] + '\nc)' + row['c'] + '\nd)' + row['d']

        #Don't get stock on a question
        failCounter=failCounter+1
        if failCounter==fail_limit:
            break

    if failCounter==fail_limit:
        continue

    #find and match the option
    next_char = llmAnswer[index+len('Answer:'):][0]
    if next_char in truth:
        correct=correct+1
        print('correct')
    else:
        print('wrong')

    #update accuracy
    accuracy=correct/questionCounter
    print(f"Progress: {questionCounter/len(df_test)}")
    print(f"Accuracy: {accuracy}")


