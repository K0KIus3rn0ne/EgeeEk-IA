import torch
from transformers import GPT2LMHeadModel, GPT2Tokenizer

class GPT2Chat:
    def __init__(self):
        self.model_name = 'gpt2'
        self.model = GPT2LMHeadModel.from_pretrained(self.model_name)
        self.tokenizer = GPT2Tokenizer.from_pretrained(self.model_name)
        self.conversation_history = ""  # História mínima da conversa, para melhorar a coerência

    def get_response(self, user_input, conversation_context, topic=None):
        # Inclui a conversa anterior no input para manter o contexto (histórico curto)
        full_input = f"{self.conversation_history} \nUsuário: {user_input}" if conversation_context else user_input
        input_ids = self.tokenizer.encode(full_input, return_tensors='pt')

        # Ajusta os parâmetros para melhorar a qualidade da geração
        output = self.model.generate(
            input_ids, 
            max_length=150,  # Limita o comprimento máximo da resposta
            temperature=0.7,  # Controla a criatividade
            top_k=50,  # Garante coerência, limitando as opções
            top_p=0.9,  # Probabilidade cumulativa para maior fluência
            no_repeat_ngram_size=2  # Evita repetições
        )

        # Decodifica a resposta e atualiza o histórico da conversa
        response = self.tokenizer.decode(output[0], skip_special_tokens=True)
        self.update_conversation_history(user_input, response)
        return response

    def update_conversation_history(self, user_input, response):
        # Atualiza o histórico da conversa (curto) para manter o contexto sem sobrecarregar
        self.conversation_history += f"Usuário: {user_input}\nIA: {response}\n"
        # Limita o histórico a 300 caracteres para evitar entradas muito longas
        if len(self.conversation_history) > 300:
            self.conversation_history = self.conversation_history[-300:]

# Exemplo de uso
def main():
    chatbot = GPT2Chat()

    conversation_context = ""  # Contexto da conversa pode ser vazio
    topic = None  # Pode ignorar o tópico se não quiser usar
    while True:
        user_input = input("Você: ")
        if user_input.lower() in ['sair', 'exit']:
            print("Encerrando a conversa...")
            break

        response = chatbot.get_response(user_input, conversation_context, topic)
        print(f"IA: {response}")

if __name__ == "__main__":
    main()
