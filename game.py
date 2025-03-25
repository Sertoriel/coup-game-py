# game.py
import random

# Representa uma carta de influência
class Card:
    def __init__(self, name):
        self.name = name
        self.revealed = False

    def __repr__(self):
        status = " (revelada)" if self.revealed else ""
        return f"{self.name}{status}"

# Representa um jogador
class Player:
    def __init__(self, name):
        self.name = name
        self.coins = 2
        self.cards = []
        self.alive = True

    def lose_influence(self, card_index):
        if 0 <= card_index < len(self.cards):
            self.cards[card_index].revealed = True
            if all(card.revealed for card in self.cards):
                self.alive = False
        else:
            raise Exception("Carta inválida.")

    def __repr__(self):
        return f"{self.name} | Moedas: {self.coins} | Cartas: {self.cards}"

# Classe principal do jogo
class Game:
    def __init__(self, player_names):
        self.characters = ["Duque", "Assassino", "Capitão", "Embaixador", "Condessa"]
        self.deck = [Card(name) for name in self.characters for _ in range(5)]
        random.shuffle(self.deck)
        self.players = [Player(name) for name in player_names]
        for player in self.players:
            player.cards.append(self.deck.pop())
            player.cards.append(self.deck.pop())
        self.current_turn = 0
        self.pending_action = None  # Ação pendente para bloqueio/desafio
        self.pending_reveal = None  # Estado pendente para revelar carta após desafio
        self.pending_exchange = None  # Estado pendente para troca do embaixador

    def get_current_player(self):
        return self.players[self.current_turn]

    def next_turn(self):
        alive_players = [p for p in self.players if p.alive]
        if len(alive_players) <= 1:
            return
        while True:
            self.current_turn = (self.current_turn + 1) % len(self.players)
            if self.players[self.current_turn].alive:
                break

    def action_renda(self, player):
        player.coins += 1
        return f"{player.name} ganhou 1 moeda."

    def action_ajuda_externa(self, player):
        player.coins += 2
        return f"{player.name} ganhou 2 moedas (pode ser bloqueada pelo Duque)."

    def action_golpe_estado(self, player, target: Player, card_index: int):
        if player.coins < 7:
            raise Exception("Moedas insuficientes para golpe de estado.")
        player.coins -= 7
        target.lose_influence(card_index)
        return f"{player.name} aplicou golpe de estado em {target.name}."

    def action_duque(self, player):
        player.coins += 3
        return f"{player.name} usou Duque e ganhou 3 moedas."

    def action_assassino(self, player, target: Player, card_index: int):
        if player.coins < 3:
            raise Exception("Moedas insuficientes para Assassinato.")
        player.coins -= 3
        target.lose_influence(card_index)
        return f"{player.name} usou Assassino em {target.name}."

    def action_capitao(self, player, target: Player):
        amount = min(2, target.coins)
        target.coins -= amount
        player.coins += amount
        return f"{player.name} roubou {amount} moedas de {target.name}."

    def action_embaixador(self, player):
        # Em vez de trocar imediatamente, criamos uma troca pendente.
        # O pool será composto pelas cartas atuais do jogador + 2 cartas extras.
        extra_cards = []
        for _ in range(2):
            if len(self.deck) > 0:
                extra_cards.append(self.deck.pop())
        pool = player.cards + extra_cards
        self.pending_exchange = {
            "player": player,
            "pool": pool,
            "keep": len(player.cards)  # Quantidade de cartas que ele já possuía
        }
        return f"Ação pendente: {player.name}, escolha exatamente {len(player.cards)} carta(s) para manter."

    def action_condessa(self, player):
        return f"{player.name} usou a Condessa para bloquear um assassinato."

    def is_game_over(self):
        alive = [p for p in self.players if p.alive]
        return len(alive) <= 1

    def get_winner(self):
        alive = [p for p in self.players if p.alive]
        return alive[0] if len(alive) == 1 else None

    # MÉTODOS PARA BLOQUEIO, DESAFIO E REVELAÇÃO (já implementados anteriormente)

    def init_pending_action(self, action, acting_player, target=None, card_index=None):
        self.pending_action = {
            "action": action,
            "acting_player": acting_player,
            "target": target,
            "card_index": card_index,
            "reaction": None,
            "reacting_player": None
        }
        self.pending_reveal = None  # Garante que não haja estado pendente anterior

    def player_has_card(self, player, card_name):
        for card in player.cards:
            if card.name == card_name and not card.revealed:
                return True
        return False

    def resolve_pending_action(self, reaction_type, reacting_player, card_used=None):
        pa = self.pending_action
        action = pa["action"]
        acting_player = pa["acting_player"]
        target = pa["target"]
        card_index = pa["card_index"]

        # Define a carta necessária para a ação (para verificação de desafio)
        required_card = None
        if action == "duque":
            required_card = "Duque"
        elif action == "assassino":
            required_card = "Assassino"
        elif action == "capitao":
            required_card = "Capitão"
        elif action == "embaixador":
            required_card = "Embaixador"
        elif action == "ajuda_externa":
            required_card = "Duque"  # para bloquear Ajuda Externa

        if reaction_type == "pass":
            # Sem reação: executa a ação normalmente
            if action == "duque":
                return self.action_duque(acting_player)
            elif action == "assassino":
                return self.action_assassino(acting_player, target, card_index)
            elif action == "capitao":
                return self.action_capitao(acting_player, target)
            elif action == "embaixador":
                # Ao usar o embaixador, redireciona para a troca pendente.
                return self.action_embaixador(acting_player)
            elif action == "ajuda_externa":
                return self.action_ajuda_externa(acting_player)
            else:
                return "Ação não reconhecida."
        elif reaction_type == "challenge":
            if required_card and self.player_has_card(acting_player, required_card):
                self.pending_reveal = {
                    "player": reacting_player,
                    "message": f"Desafio falhou! {acting_player.name} possuía {required_card}. {reacting_player.name}, escolha uma carta para revelar."
                }
                return f"Desafio pendente: {reacting_player.name} deve revelar uma carta."
            else:
                self.pending_reveal = {
                    "player": acting_player,
                    "message": f"Desafio bem-sucedido! {acting_player.name} não possuía {required_card}. Escolha uma carta para revelar."
                }
                return f"Desafio pendente: {acting_player.name} deve revelar uma carta."
        elif reaction_type == "block":
            if not card_used:
                return "Nenhuma carta foi informada para bloqueio."
            if self.player_has_card(reacting_player, card_used):
                return f"Ação bloqueada por {reacting_player.name} usando {card_used}."
            else:
                reacting_player.lose_influence(0)
                return f"Bloqueio falhou! {reacting_player.name} não possuía {card_used}. Bloqueio inválido."
        else:
            return "Reação inválida."

    def resolve_pending_reveal(self, card_index):
        if self.pending_reveal is None:
            raise Exception("Não há ação pendente de revelação.")
        losing_player = self.pending_reveal["player"]
        losing_player.lose_influence(int(card_index))
        msg = f"{losing_player.name} revelou uma carta e perdeu influência."
        self.pending_reveal = None
        self.pending_action = None  # Limpa a ação pendente após resolução
        return msg

    def resolve_pending_exchange(self, selected_indices):
        if self.pending_exchange is None:
            raise Exception("Não há troca pendente.")
        exchange = self.pending_exchange
        player = exchange["player"]
        pool = exchange["pool"]
        keep = exchange["keep"]
        if len(selected_indices) != keep:
            raise Exception(f"Você deve selecionar exatamente {keep} carta(s).")
        try:
            selected_indices = list(map(int, selected_indices))
        except ValueError:
            raise Exception("Índices inválidos.")
        if any(idx < 0 or idx >= len(pool) for idx in selected_indices):
            raise Exception("Índice fora do intervalo do pool de cartas.")
        # Define a nova mão do jogador com as cartas escolhidas
        new_hand = [pool[idx] for idx in selected_indices]
        # As cartas não escolhidas retornam para o deck
        remaining_cards = [card for i, card in enumerate(pool) if i not in selected_indices]
        self.deck.extend(remaining_cards)
        random.shuffle(self.deck)
        player.cards = new_hand
        self.pending_exchange = None
        return f"{player.name} trocou suas cartas com sucesso."
