"""
Servidor HTTP local (rede Wi-Fi da casa, não é exposto pra internet).
Recebe comandos vindos do app Android e repassa pro escravo.py — a
mesma lógica que o campo de texto da aba Início já usa.

Roda dentro de uma QThread pra não travar a interface enquanto está
escutando. Usa werkzeug.serving.make_server (em vez de app.run direto)
porque isso dá um jeito limpo de LIGAR e DESLIGAR o servidor sob
demanda — o app.run() padrão do Flask não tem um "parar" de fora.
"""

from __future__ import annotations

import secrets
import socket

from flask import Flask, jsonify, request
from PySide6.QtCore import QThread
from werkzeug.serving import make_server

import escravo
from ui import system_info

PORTA_PADRAO = 5678


def obter_ip_local() -> str:
    """Descobre o IP da máquina na rede local (não o 127.0.0.1), pra
    mostrar pro usuário digitar no celular. Não manda nem recebe nada
    de verdade pro 8.8.8.8 — só usa a tentativa de conexão UDP pra
    perguntar ao sistema operacional qual interface de rede seria
    usada, que é um jeito confiável de achar o IP local mesmo com
    várias placas de rede."""
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        s.connect(("8.8.8.8", 80))
        return s.getsockname()[0]
    except Exception:
        return "127.0.0.1"
    finally:
        s.close()


def gerar_token() -> str:
    return secrets.token_hex(4)  # 8 caracteres, fácil de digitar no celular


class ServidorRemoto(QThread):
    """Uma instância = um servidor rodando. Chame start() pra ligar e
    parar() pra desligar (espera terminar com wait())."""

    def __init__(self, token: str, porta: int = PORTA_PADRAO, parent=None):
        super().__init__(parent)
        self.token = token
        self.porta = porta
        self._app = self._criar_app()
        self._server = make_server("0.0.0.0", self.porta, self._app, threaded=True)

    def _checar_token(self):
        # todas as rotas exigem o token, inclusive /ping — se não exigisse
        # aqui, a tela de "Conectar" do celular sempre daria "sucesso"
        # mesmo com a chave errada, e o erro só apareceria depois, ao
        # tentar executar um comando de verdade.
        if request.headers.get("X-Token", "") != self.token:
            return jsonify({"erro": "token inválido"}), 401
        return None

    def _criar_app(self) -> Flask:
        app = Flask(__name__)
        app.before_request(self._checar_token)

        @app.route("/ping", methods=["GET"])
        def ping():
            return jsonify({"status": "ok", "app": "Assistente Virtual Ikuromimy"})

        @app.route("/comando", methods=["POST"])
        def comando():
            dados = request.get_json(silent=True) or {}
            texto = (dados.get("texto") or "").strip()
            if not texto:
                return jsonify({"erro": "comando vazio"}), 400
            try:
                escravo.processar_comando(texto)
                return jsonify({"ok": True})
            except Exception as erro:
                return jsonify({"erro": str(erro)}), 500

        @app.route("/midia/<acao>", methods=["POST"])
        def midia(acao):
            acoes = {
                "play_pause": escravo.media_play_pause,
                "proxima": escravo.media_next,
                "anterior": escravo.media_prev,
            }
            funcao = acoes.get(acao)
            if not funcao:
                return jsonify({"erro": "ação desconhecida"}), 400
            funcao()
            return jsonify({"ok": True})

        @app.route("/sistema", methods=["GET"])
        def sistema():
            return jsonify(system_info.obter_resumo_sistema())

        return app

    def run(self) -> None:
        self._server.serve_forever()

    def parar(self) -> None:
        self._server.shutdown()
