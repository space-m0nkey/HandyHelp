from flask import Flask, jsonify, request
import os
import json 
app = Flask(__name__)
ANUNCIOS_FILE = 'anuncios.json'
AVALIACOES_FILE = 'avaliacoes.json'
def carregar_dados(nome_arquivo):
    try:
        with open(nome_arquivo, 'r') as arquivo:
            return json.load(arquivo)
    except (FileNotFoundError, json.decoder.JSONDecodeError):
        return None
def salvar_dados(dados, nome_arquivo):
    with open(nome_arquivo, 'w') as arquivo:
        json.dump(dados, arquivo, indent=4)
if not os.path.exists(ANUNCIOS_FILE) or os.path.getsize(ANUNCIOS_FILE) == 0:
    with open(ANUNCIOS_FILE, 'w') as arquivo:
        json.dump([], arquivo)
if not os.path.exists(AVALIACOES_FILE) or os.path.getsize(AVALIACOES_FILE) == 0:
    with open(AVALIACOES_FILE, 'w') as arquivo:
        json.dump({}, arquivo)
anuncios = carregar_dados(ANUNCIOS_FILE) or []
avaliacoes = carregar_dados(AVALIACOES_FILE) or {}
@app.route('/anuncio/<int:id_anuncio>')
def visualizar_anuncio(id_anuncio):
    anuncio = next((a for a in anuncios if a['id'] == id_anuncio), None)
    if anuncio:
        return jsonify(anuncio)
    else:
        return jsonify({"error": "Anúncio não encontrado"}), 404
@app.route('/avaliacoes/<int:id_anuncio>')
def visualizar_avaliacoes(id_anuncio):
    if id_anuncio in avaliacoes:
        return jsonify({"avaliacoes": avaliacoes[id_anuncio]})
    else:
        return jsonify({"error": "Avaliações não encontradas para o anúncio especificado"}), 404
@app.route('/')
def index():
    return jsonify(anuncios)
@app.route('/avaliar', methods=['POST'])
def avaliacao():
    data = request.json
    if 'id_anuncio' in data and 'estrelas' in data:
        id_anuncio = data['id_anuncio']
        estrelas = data['estrelas']
        if id_anuncio in avaliacoes:
            avaliacoes[id_anuncio].append(estrelas)
        else:
            avaliacoes[id_anuncio] = [estrelas]
        media = sum(avaliacoes[id_anuncio]) / len(avaliacoes[id_anuncio])
        salvar_dados(avaliacoes, AVALIACOES_FILE)
        return jsonify({"message": "Avaliação recebida", "media_avaliacoes": media}), 201
    else:
        return jsonify({"error": "Dados inválidos"}), 400
@app.route('/criar_anuncio', methods=['POST'])
def criar_anuncio():
    data = request.json
    if 'titulo' in data and 'descricao' in data and 'local' in data and 'preco' in data:
        anuncio = {"id": len(anuncios) + 1, "titulo": data['titulo'], "descricao": data['descricao'], "local": data['local'], "preco": data['preco']}
        anuncios.append(anuncio)
        salvar_dados(anuncios, ANUNCIOS_FILE)
        return jsonify({"message": "Anúncio criado com sucesso", "anuncio": anuncio}), 201
    else:
        return jsonify({"error": "Dados inválidos"}), 400
if __name__ == '__main__':
    print("""

    //    / /                                                    //    / /
   //___ / /      ___         __        ___   /                 //___ / /      ___       //      ___
  / ___   /     //___) )   //   ) )   //   ) /    //   / /     / ___   /     //___) )   //     //   ) )
 //    / /     //         //   / /   //   / /    ((___/ /     //    / /     //         //     //___/ /
//    / /     ((____     //   / /   ((___/ /         / /     //    / /     ((____     //     //

""")
    app.run(debug=True)
