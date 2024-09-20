from feedback import FeedbackSystem
from gpt2_model import GPT2Chat
from conversation_memory import Memory
from flow_control import maintain_flow, clarify_question

def print_goo():
    goo = """
   _____           ______       
  / ____|         |  ____|      
 | |  __  ___  ___| |__   _  __ 
 | | |_ |/ _ \/ _ \  __| | |/ / 
 | |__| |  __/  __/ |____|   <   
  \_____|\___|\___|______|_|\_\  IA
    """
    print(goo)

print_goo()

def main():
    chat = GPT2Chat()
    memory = Memory()
    feedback_system = FeedbackSystem()
    topic = None

    while True:
        user_input = input("Você: ")

        # Mantém o fluxo da conversa
        topic = maintain_flow(user_input, topic)

        # Clarifica se necessário
        if clarify_question(user_input):
            clarification = input("IA: Pode esclarecer melhor? ")
            user_input += " " + clarification

        # Recupera a média de feedback anterior (se existir)
        previous_feedback = feedback_system.get_feedback(user_input)
        if previous_feedback < 0:
            print("IA: Parece que eu errei antes, vamos tentar novamente.")

        # Gera a resposta com o GPT-2
        memory.add_message("user", user_input)
        response = chat.get_response(user_input, memory.get_full_context(), topic)
        memory.add_message("IA", response)

        print(f"IA: {response}")

        # Solicita feedback do usuário
        feedback = input("Feedback (+1 para bom, -1 para ruim): ")
        feedback = int(feedback) if feedback in ["+1", "-1"] else 0

        # Armazena o feedback no banco de dados
        feedback_system.store_feedback(user_input, response, feedback)

if __name__ == "__main__":
    main()
