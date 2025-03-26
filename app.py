from flask import Flask, render_template, request, redirect, url_for, flash
from game import Game, Player
import traceback

app = Flask(__name__)
app.secret_key = 'chave-secreta'

game = None

@app.route("/add_players", methods=["GET", "POST"])
def add_players():
    global game
    if request.method == "POST":
        players_str = request.form.get("players")
        if not players_str:
            flash("Insira pelo menos um nome de jogador.", "danger")
            return redirect(url_for("add_players"))
        player_names = [name.strip() for name in players_str.split(",") if name.strip()]
        if len(player_names) < 4 or len(player_names) > 6:
            flash("Número de jogadores deve ser entre 4 e 6.", "danger")
            return redirect(url_for("add_players"))
        game = Game(player_names)
        flash("Jogo iniciado com sucesso!", "success")
        return redirect(url_for("index"))
    return render_template("add_players.html")

@app.route("/", methods=["GET", "POST"])
def index():
    global game
    if game is None:
        flash("Cadastre os jogadores para iniciar o jogo.", "info")
        return redirect(url_for("add_players"))
    if request.method == "POST":
        try:
            action = request.form.get("action")
            current_player = game.get_current_player()
            target_index = request.form.get("target")
            card_index = request.form.get("card_index")
            result = ""
            if action == "assassino" and current_player.coins < 3:
                flash("Você não tem moedas suficientes para executar Assassino.", "danger")
                return redirect(url_for("index"))
            if action == "golpe_estado" and current_player.coins < 7:
                flash("Você não tem moedas suficientes para executar Golpe de Estado.", "danger")
                return redirect(url_for("index"))
            
            challengeable_actions = ["ajuda_externa", "duque", "assassino", "capitao", "embaixador"]
            if action in challengeable_actions:
                target = game.players[int(target_index)] if target_index and target_index.strip() != "" else None
                game.init_pending_action(action, current_player, target, int(card_index) if card_index and card_index.strip() != "" else None)
                return redirect(url_for("reaction"))
            else:
                if action == "renda":
                    result = game.action_renda(current_player)
                elif action == "golpe_estado":
                    if target_index is None or card_index is None:
                        raise Exception("Selecione um alvo e a carta a ser perdida.")
                    target = game.players[int(target_index)]
                    result = game.action_golpe_estado(current_player, target, int(card_index))
                elif action == "condessa":
                    result = game.action_condessa(current_player)
                else:
                    raise Exception("Ação inválida.")

                flash(result, "success")
                if game.is_game_over():
                    winner = game.get_winner()
                    flash(f"Fim do jogo! Vencedor: {winner.name}", "info")
                else:
                    game.next_turn()
        except Exception as e:
            flash(str(e), "danger")
            traceback.print_exc()
        return redirect(url_for("index"))
    return render_template("index.html", game=game)

@app.route("/reaction", methods=["GET", "POST"])
def reaction():
    global game
    if game.pending_action is None:
        flash("Não há ação pendente.", "danger")
        return redirect(url_for("index"))
    action = game.pending_action["action"]
    required_card = None
    if action == "duque" or action == "ajuda_externa":
        required_card = "Duque"
    elif action == "assassino":
        required_card = "Condessa"
    elif action == "capitao":
        required_card = "Capitão ou Embaixador"
    elif action == "embaixador":
        required_card = "Embaixador"
    
    if request.method == "POST":
        reaction_type = request.form.get("reaction")
        reacting_player_index = request.form.get("reacting_player")
        reacting_player = game.players[int(reacting_player_index)] if reacting_player_index else None
        card_used = request.form.get("card_used")
        result = game.resolve_pending_action(reaction_type, reacting_player, card_used)
        flash(result, "success")
        if game.pending_reveal is not None:
            return redirect(url_for("reveal"))
        if game.pending_exchange is not None:
            return redirect(url_for("exchange"))
        if not game.is_game_over():
            game.next_turn()
        return redirect(url_for("index"))
    return render_template("reaction.html", pending=game.pending_action, players=game.players, required_card=required_card)

@app.route("/reveal", methods=["GET", "POST"])
def reveal():
    global game
    if game.pending_reveal is None:
        flash("Nenhuma carta precisa ser revelada.", "info")
        return redirect(url_for("index"))
    pending = game.pending_reveal
    player = pending["player"]
    available_cards = [(i, card) for i, card in enumerate(player.cards) if not card.revealed]
    if request.method == "POST":
        card_index = request.form.get("card_index")
        if card_index is None:
            flash("Selecione uma carta para revelar.", "danger")
            return redirect(url_for("reveal"))
        result = game.resolve_pending_reveal(card_index)
        flash(result, "success")
        if not game.is_game_over():
            game.next_turn()
        return redirect(url_for("index"))
    return render_template("reveal.html", player=player, available_cards=available_cards, message=pending["message"])

@app.route("/exchange", methods=["GET", "POST"])
def exchange():
    global game
    if game.pending_exchange is None:
        flash("Nenhuma troca pendente.", "info")
        return redirect(url_for("index"))
    exchange_data = game.pending_exchange
    pool = exchange_data["pool"]
    keep = exchange_data["keep"]
    player = exchange_data["player"]
    if request.method == "POST":
        selected = request.form.getlist("selected")
        try:
            result = game.resolve_pending_exchange(selected)
            flash(result, "success")
            if not game.is_game_over():
                game.next_turn()
            return redirect(url_for("index"))
        except Exception as e:
            flash(str(e), "danger")
            return redirect(url_for("exchange"))
    return render_template("exchange.html", pool=pool, keep=keep, player=player)

if __name__ == "__main__":
    app.run(debug=True, port=5001)
