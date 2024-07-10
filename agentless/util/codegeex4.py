
import json
import gzip
import fire
import time
import requests
import loguru
from tqdm.auto import tqdm
import os

logger = loguru.logger

headers = {
    'Content-Type': 'application/json'
}

def generate(
        prompt, 
        url,
        do_sample=False,
        temperature=0.3,
        top_p=0.95,
        max_tokens=256,
        truncate=12800,
        stream=False,
        stop=["<|endoftext|>", "<|user|>", "<|observation|>", "<|assistant|>"],
        retries=3,
        delay=2,
        **kwargs
):
    data = {
        "prompt": prompt,
        "temperature": temperature,
        "top_p": top_p,
        "do_sample": do_sample,
        "max_tokens": max_tokens,
        "truncate": truncate,
        "stream": stream,
        "stop": stop,
    }
    attempts = 0
    while attempts < retries:
        try:
            response = requests.post(url, headers=headers, json=data, verify=False)
            response = response.json()
            return response['choices'][0]['text']
        except Exception as e:
            attempts += 1
            print(e)
            logger.error(f"Attempt {attempts}/{retries} failed with error: {e}. Retrying in {delay} seconds...")
            time.sleep(delay)
    raise Exception(f"All {retries} attempts failed for prompt: {prompt}")



def generate_with_openai():
    import openai
    from zhipuai import ZhipuAI

    # client = openai.OpenAI(api_key=os.environ.get("ZHIPU_API_KEY"))
    client = ZhipuAI(api_key=os.environ.get("ZHIPU_API_KEY"))
    batch_size = 3
    max_tokens = 256
    temperature = 0.3

    config = {
            "model": "codegeex-4",
            "max_tokens": max_tokens,
            "temperature": temperature,
             "messages":[
        {"role": "user", "content": "作为一名营销专家，请为我的产品创作一个吸引人的slogan"},
        {"role": "assistant", "content": "当然，为了创作一个吸引人的slogan，请告诉我一些关于您产品的信息"},
        {"role": "user", "content": "智谱AI开放平台"},
        {"role": "assistant", "content": "智启未来，谱绘无限一智谱AI，让创新触手可及!"},
        {"role": "user", "content": "创造一个更精准、吸引人的slogan"}
    ]
            }

    response = client.chat.completions.create(**config)
    print(response.choices[0].message.content)
    print(response.usage.prompt_tokens)
    print(response.usage.completion_tokens)





def main():
    system_prompt = "You are an intelligent programming assistant named CodeGeeX. You will answer any questions users have about programming, coding, and computers, and provide code that is formatted correctly. "
    query = "What can you do?"
    # Sample prompt 
    # prompt = f"<|assistant|>\n{system_prompt}\n<|user|>\n{query}\n"
    
    # taking prompt from file
    # with open("codegeex_inspect/prompt.txt", "r") as f:
    #     # load from f
    #     prompt = f.read()


    # url = "http://172.18.64.110:9090/v1/completions"
    # try:
    #     code = generate(prompt, url)
    #     logger.info(code)

    # except Exception as e:
    #     logger.error(e)

    generate_with_openai()


if __name__ == "__main__":
    main()