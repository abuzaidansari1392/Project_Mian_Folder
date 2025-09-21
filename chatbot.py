from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
from datetime import datetime

import re

class Chatbot:
    def __init__(self):
        self.tokenizer = AutoTokenizer.from_pretrained("microsoft/DialoGPT-small")
        self.model = AutoModelForCausalLM.from_pretrained("microsoft/DialoGPT-small")
        self.chat_history_ids = None
        self.tokenizer.pad_token = self.tokenizer.eos_token
        
        # Simple FAQ responses
        self.faq_responses = {
            "hello": "Hello! How can I help you today?",
            "hi": "Hi there! What can I assist you with?",
            "help": "I'm here to help! You can ask me about our products, services, or anything else you need.",
            "thanks": "You're welcome! Is there anything else I can help with?",
            "whats time now": "Current time is: " + datetime.now().strftime("%H:%M:%S"),
            "bye": "Goodbye! Have a great day!",
            "order status": "To check your order status, please provide your order number or login to your account.",
            "refund": "For refund inquiries, please contact our support team at support@company.com.",
            "hours": "Our customer service is available Monday to Friday, 9 AM to 6 PM EST."
        }

    def preprocess_text(self, text):
        """Basic text preprocessing"""
        text = text.lower().strip()
        text = re.sub(r'[^\w\s]', '', text)
        return text

    def get_faq_response(self, user_input):
        """Check if input matches any FAQ"""
        processed_input = self.preprocess_text(user_input)
        for keyword, response in self.faq_responses.items():
            if keyword in processed_input:
                return response
        return None

    def get_response(self, user_input):
        """Get response from chatbot"""
        # First check if it's a simple FAQ
        faq_response = self.get_faq_response(user_input)
        if faq_response:
            return faq_response

        # Otherwise use the transformer model
        try:
            # Encode the new user input
            new_input_ids = self.tokenizer.encode(user_input + self.tokenizer.eos_token, return_tensors='pt')
            
            # Append to chat history
            if self.chat_history_ids is not None:
                bot_input_ids = torch.cat([self.chat_history_ids, new_input_ids], dim=-1)
            else:
                bot_input_ids = new_input_ids

            # Generate response
            self.chat_history_ids = self.model.generate(
                bot_input_ids,
                max_length=1000,
                pad_token_id=self.tokenizer.eos_token_id,
                temperature=0.7,
                do_sample=True
            )
            
            # Decode and return response
            response = self.tokenizer.decode(
                self.chat_history_ids[:, bot_input_ids.shape[-1]:][0],
                skip_special_tokens=True
            )
            
            return response if response else "I'm not sure how to respond to that. Can you try rephrasing?"
            
        except Exception as e:
            return f"I apologize, but I'm having trouble processing your request. Error: {str(e)}"