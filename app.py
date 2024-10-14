from flask import Flask, request, send_file, jsonify
import subprocess
import os
import glob


app = Flask(__name__)

def baixar_musica(url):
    try:
        # Executa o comando para baixar a música
        subprocess.run(['yt-dlp', '-x', '--audio-format', 'mp3', url], check=True)
        print("Download concluído!")
    except subprocess.CalledProcessError as e:
        return None, f"Erro ao baixar: {e}"

    # Encontra o arquivo MP3 baixado
    arquivos = glob.glob('*.mp3')
    if arquivos:
        return arquivos[0], None  # Retorna o nome do primeiro arquivo encontrado
    else:
        return None, "Nenhum arquivo MP3 encontrado."

@app.route('/download', methods=['POST'])
def baixar():
    data = request.json
    url = data.get('url')

    if not url:
        return jsonify({"error": "URL não fornecida"}), 400

    arquivo, erro = baixar_musica(url)

    filename = arquivo.split(".mp3")[0]

    if erro:
        return jsonify({"error": erro}), 500

    # Retorna a URL do arquivo para download
    return jsonify({"filename": filename})

@app.route('/download/<filename>', methods=['GET'])
def download_file(filename):
    return send_file(filename, as_attachment=True)

@app.route('/download/<filename>', methods=['DELETE'])
def delete_file(filename):
    try:
        os.remove(filename)
        return jsonify({"message": f"Arquivo '{filename}' deletado com sucesso!"}), 200
    except FileNotFoundError:
        return jsonify({"error": "Arquivo não encontrado!"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)

