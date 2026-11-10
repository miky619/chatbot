import requests
import json

def call_ollama_model(prompt, model, stream=False):
    url = "http://localhost:11434/api/generate"

    params = {
        "prompt":prompt,
        "model": model,
        "stream": stream
    }
    paylod = json.dumps(params)

    response = requests.post(url, data=paylod,
                             headers={"Content-Type":"application/json"})
    if response.status_code != 200:
        return "ERORR"
    else:
        response = response.json()["response"]
        return response

def stream_ollama_model(prompt, model):
    url = "http://localhost:11434/api/generate"

    params = {
        "prompt": prompt,
        "model": model,
        "stream": True
    }
    paylod = json.dumps(params)

    response = requests.post(url, data=paylod,
                             headers={"Content-Type": "application/json"},
                             stream=True)
    if response.status_code != 200:
        yield "ERORR"
        return

    
    for line in response.iter_lines():
        if line:
            data = json.loads(line)
            yield data.get("response", "")


# ===============================
if __name__ == "__main__":
    model = "gemma3:1b"
    prompt = input("Enter your Question:")
    response = call_ollama_model(prompt, model)
    print(f"Response: {response}")

