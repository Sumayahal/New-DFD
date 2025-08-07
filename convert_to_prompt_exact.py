import json

def convert_to_prompt(input_path, output_path):
    with open(input_path, 'r', encoding='utf-8') as f:
        raw_data = json.load(f)

    with open(output_path, 'w', encoding='utf-8') as f:
        for example in raw_data:
            entry = {
                "messages": [
                    {"role": "user", "content": example["input"]},
                    {"role": "assistant", "content": example["output"]}
                ]
            }
            f.write(json.dumps(entry, ensure_ascii=False) + "\n")

if __name__ == "__main__":
    convert_to_prompt("raw_examples_final.json", "reconstructed_fine_tune_ready.jsonl")