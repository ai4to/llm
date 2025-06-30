# Chain of Empathy for Large Language Models

Chain of Empathy is a prompt engineering method developed similar to Chain of Thought prompting, which has demonstrated significant imporvement in model's responses to users. The paper with the results can be found [here](https://arxiv.org/abs/2311.04915).

This technique has significant use cases in terms of our project. It is important that our LLM is considerate and empathetic to the needs of someone who suffering from breast cancer. This repo contains my experiments with CoE prompting.

## Repo Changelog

1. Experiment 1.ipynb : This contains my first experimentation with Chain of Empathy prompting. I tried to use HuggingFace transformers but this wasn't that successful.

2. Experiment 2.ipynb : I used OpenRouter to get a free API key for Deepseek-R1 and Qwen. Deepseek-R1 took into account the system prompt designed under the paper's guidelines, but has shown to struggle to follow CoT prompting, so I switched to Qwen. I can see some definitive changes on the CoE prompt vs the Non CoE prompt. More improvements on the prompt should enhance this distinction.