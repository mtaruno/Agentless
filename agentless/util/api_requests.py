import signal
import time
from typing import Dict, Union

import openai
import tiktoken
from agentless.util.codegeex4 import generate
from zhipuai import ZhipuAI
import os
import config

cfg = config.Config(os.path.join(os.getcwd(), "keys.cfg"))
client = openai.OpenAI(api_key=cfg['OPENAI_API_KEY'])
zhipu_client = ZhipuAI(api_key=cfg["ZHIPU_API_KEY"])

def num_tokens_from_messages(message, model="gpt-3.5-turbo-0301"):
    """Returns the number of tokens used by a list of messages."""
    try:
        encoding = tiktoken.encoding_for_model(model)
    except KeyError:
        encoding = tiktoken.get_encoding("cl100k_base")
    if isinstance(message, list):
        # use last message.
        num_tokens = len(encoding.encode(message[0]["content"]))
    else:
        num_tokens = len(encoding.encode(message))
    return num_tokens

       
# def create_codegeex_config(
#     message: Union[str, list],
#     max_tokens: int,
#     temperature: float = 1,
#     system_message: str = "You are a helpful assistant.",
# ) -> Dict:
#     if isinstance(message, list):
#         config = {
#             "max_tokens": max_tokens,
#             "temperature": temperature,
#             "prompt": f"<|assistant|>\n{system_message}\n<|user|>\n{message}\n<|assistant|>\n",
#             "url": "http://172.18.64.110:9090/v1/completions"
#         }
#     else:
#         config = {
#             "max_tokens": max_tokens,
#             "temperature": temperature,
#             "prompt": f"<|assistant|>\n{system_message}\n<|user|>\n{message}\n<|assistant|>\n",
#             "url" : "http://172.18.64.110:9090/v1/completions"
#         }
#     return config 


# def request_codegeex_engine(config):
#     ret = None
#     while ret is None:
#         try:
#             signal.signal(signal.SIGALRM, handler)
#             signal.alarm(100)
#             ret = generate(**config)
#             signal.alarm(0)
#         except openai._exceptions.BadRequestError as e:
#             print(e)
#             signal.alarm(0)
#         except openai._exceptions.RateLimitError as e:
#             print("Rate limit exceeded. Waiting...")
#             print(e)
#             signal.alarm(0)
#             time.sleep(5)
#         except openai._exceptions.APIConnectionError as e:
#             print("API connection error. Waiting...")
#             signal.alarm(0)
#             time.sleep(5)
#         except Exception as e:
#             print("Unknown error. Waiting...")
#             print(e)
#             signal.alarm(0)
#             time.sleep(1)
#     return ret
    

def create_chatgpt_config(
    message: Union[str, list],
    max_tokens: int,
    temperature: float = 1,
    batch_size: int = 1,
    system_message: str = "You are a helpful assistant.",
    model: str = "gpt-3.5-turbo",
) -> Dict:
    if isinstance(message, list):
        config = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "n": batch_size,
            "messages": [{"role": "system", "content": system_message}] + message,
        }
    else:
        config = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "n": batch_size,
            "messages": [
                {"role": "system", "content": system_message},
                {"role": "user", "content": message},
            ],
        }
    return config


def handler(signum, frame):
    # swallow signum and frame
    raise Exception("end of time")


def request_chatgpt_engine(config):
    ret = None
    while ret is None:
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(100)
            ret = client.chat.completions.create(**config)
            signal.alarm(0)
        except openai._exceptions.BadRequestError as e:
            print(e)
            signal.alarm(0)
        except openai._exceptions.RateLimitError as e:
            print("Rate limit exceeded. Waiting...")
            print(e)
            signal.alarm(0)
            time.sleep(5)
        except openai._exceptions.APIConnectionError as e:
            print("API connection error. Waiting...")
            signal.alarm(0)
            time.sleep(5)
        except Exception as e:
            print("Unknown error. Waiting...")
            print(e)
            signal.alarm(0)
            time.sleep(1)
    return ret




def create_codegeex_config(
    message: Union[str, list],
    max_tokens: int,
    temperature: float = 1,
    batch_size: int = 1,
    system_message: str = "You are an intelligent programming assistant named CodeGeeX. You will answer any questions users have about programming, coding, and computers, and provide code that is formatted correctly.",
    model: str = "codegeex-4",
) -> Dict:
    if isinstance(message, list):
        config = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [{"role": "system", "content": system_message}] + message,
        }
    else:
        config = {
            "model": model,
            "max_tokens": max_tokens,
            "temperature": temperature,
            "messages": [
                {"role": "user", "content": message},
            ],
        }
    return config
def request_codegeex_engine(config):
    ret = None
    while ret is None:
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(100)
            ret = zhipu_client.chat.completions.create(**config)
            signal.alarm(0)
        except openai._exceptions.BadRequestError as e:
            print(e)
            signal.alarm(0)
        except openai._exceptions.RateLimitError as e:
            print("Rate limit exceeded. Waiting...")
            print(e)
            signal.alarm(0)
            time.sleep(5)
        except openai._exceptions.APIConnectionError as e:
            print("API connection error. Waiting...")
            signal.alarm(0)
            time.sleep(5)
        except Exception as e:
            print("Unknown error. Waiting...")
            print(e)
            signal.alarm(0)
            time.sleep(1)
    return ret


def create_anthropic_config(
    message: str,
    prefill_message: str,
    max_tokens: int,
    temperature: float = 1,
    batch_size: int = 1,
    system_message: str = "You are a helpful assistant.",
    model: str = "claude-2.1",
) -> Dict:
    if isinstance(message, list):
        config = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "system": system_message,
            "messages": message,
        }
    else:
        config = {
            "model": model,
            "temperature": temperature,
            "max_tokens": max_tokens,
            "system": system_message,
            "messages": [
                {"role": "user", "content": message},
                {"role": "assistant", "content": prefill_message},
            ],
        }
    return config


def request_anthropic_engine(client, config):
    ret = None
    while ret is None:
        try:
            signal.signal(signal.SIGALRM, handler)
            signal.alarm(100)
            ret = client.messages.create(**config)
            signal.alarm(0)
        except Exception as e:
            print("Unknown error. Waiting...")
            print(e)
            signal.alarm(0)
            time.sleep(10)
    return ret
