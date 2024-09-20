class Memory:
  def __init__(self):
      self.history = []

  def add_message(self, speaker, message):
      self.history.append((speaker, message))

  def get_full_context(self):
      # Retorna uma string com todo o contexto da conversa
      return "\n".join([f"{speaker}: {msg}" for speaker, msg in self.history[-5:]])  # Últimas 5 mensagens para contexto