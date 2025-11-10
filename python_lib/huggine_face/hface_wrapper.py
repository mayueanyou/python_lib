import os,sys,torch
from transformers import AutoImageProcessor, AutoProcessor, AutoTokenizer, AutoModelForCausalLM, BitsAndBytesConfig, AutoConfig, pipeline,Gemma3nForConditionalGeneration
from accelerate import infer_auto_device_map, init_empty_weights
from abc import ABC, abstractmethod


class HFaceWrapper:
    def __init__(self,task,model_id,quantization=True):
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        self.task = task
        self.quantization = quantization
        #self.auto_load = auto_load
        self.model_id = model_id

        if self.task in ['text-generation','image-text-to-text']:
            self.pipeline_config = {
            "task": self.task,
            "model": self.model_id,
            "device_map": "auto",
            "max_new_tokens": 256
            }

        print(f'Model ID: {self.model_id}')
        self.generate_model()
    
    def generate_model(self):
        if self.model_id == "meta-llama/Meta-Llama-3.1-8B-Instruct":
            tokenizer = AutoTokenizer.from_pretrained(self.pipeline_config['model'])
            model = AutoModelForCausalLM.from_pretrained(
                self.pipeline_config['model'],
                quantization_config= BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16),
                device_map="auto"
            )
            self.pipeline_config["model"] = model
            self.pipeline_config["tokenizer"] = tokenizer
            self.pipe = pipeline(**self.pipeline_config)
        elif self.model_id == "google/gemma-3n-e4b-it":
            if self.quantization:
                quantization_config = BitsAndBytesConfig(
                                        load_in_4bit=True,
                                        bnb_4bit_quant_type="nf4",
                                        bnb_4bit_compute_dtype=torch.bfloat16)

                self.model = Gemma3nForConditionalGeneration.from_pretrained(self.model_id, device_map="auto", torch_dtype=torch.bfloat16,).eval()
                self.processor = AutoProcessor.from_pretrained(self.model_id)

                
            else:
                self.pipe = pipeline(**self.pipeline_config)
            
            
        elif self.model_id == "google/gemma-3-4b-it":
            model = AutoModelForCausalLM.from_pretrained(
                self.pipeline_config['model'],
                quantization_config= BitsAndBytesConfig(
                    load_in_4bit=True,
                    bnb_4bit_quant_type="nf4",
                    bnb_4bit_compute_dtype=torch.bfloat16),
                device_map="auto"
            )
            self.pipeline_config["model"] = model
            self.pipe = pipeline(**self.pipeline_config)
        else:
            if self.task == "image-text-to-text":
                self.pipe = pipeline(**self.pipeline_config)

    def inference(self,input_data):
        if self.model_id == "meta-llama/Meta-Llama-3.1-8B-Instruct":
            with torch.no_grad(): output = self.pipe(input_data)
        elif self.model_id == "google/gemma-3n-e4b-it":
            if not self.quantization:
                with torch.no_grad(): output = self.pipe(input_data)
            else:
                inputs = self.processor.apply_chat_template(
                        input_data,
                        add_generation_prompt=True,
                        tokenize=True,
                        return_dict=True,
                        return_tensors="pt",
                    ).to(self.model.device)
                input_len = inputs["input_ids"].shape[-1]
                with torch.inference_mode():
                    generation = self.model.generate(**inputs, max_new_tokens=100, do_sample=False)
                    generation = generation[0][input_len:]

                decoded = self.processor.decode(generation, skip_special_tokens=True)
                print(decoded)
        elif self.model_id == "google/gemma-3-4b-it":
            with torch.no_grad(): output = self.pipe(input_data)
        else:
            with torch.no_grad(): output = self.pipe(input_data)
        return output
    
    def llm_raw_inference(self):
        text = "Hello, how are you?"
        inputs = self.tokenizer(text, return_tensors="pt").to(self.device)

        with torch.no_grad():
            outputs = self.model(**inputs)

        # Access the raw tensor (e.g., logits)
        logits = outputs.logits
        print(logits.shape)
