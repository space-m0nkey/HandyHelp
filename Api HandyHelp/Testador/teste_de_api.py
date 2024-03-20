import requests
base_url = 'http://127.0.0.1:5000'
def print_response(response):
    print('Status code:', response.status_code)
    print('Response:', response.json())
    print()
def test_visualizar_anuncio(id_anuncio):
    url = f'{base_url}/anuncio/{id_anuncio}'
    response = requests.get(url)
    print(f'Visualizar Anúncio {id_anuncio}:')
    print_response(response)
def test_visualizar_avaliacoes(id_anuncio):
    url = f'{base_url}/avaliacoes/{id_anuncio}'
    response = requests.get(url)
    print(f'Visualizar Avaliações do Anúncio {id_anuncio}:')
    if response.status_code == 200:
        avaliacoes = response.json().get('avaliacoes', [])
        if avaliacoes:
            media_avaliacoes = sum(avaliacoes) / len(avaliacoes)
            print('Avaliações:', avaliacoes)
            print('Média de Avaliações:', media_avaliacoes)
        else:
            print('Não há avaliações para este anúncio.')
    else:
        print_response(response)
def test_visualizar_todos_anuncios():
    url = f'{base_url}/'
    response = requests.get(url)
    print('Visualizar Todos os Anúncios:')
    print_response(response)
def test_avaliar(id_anuncio, estrelas):
    url = f'{base_url}/avaliar'
    data = {'id_anuncio': id_anuncio, 'estrelas': estrelas}
    response = requests.post(url, json=data)
    print(f'Avaliar Anúncio {id_anuncio} com {estrelas} estrelas:')
    print_response(response)
def test_criar_anuncio(titulo, descricao, local, preco):
    url = f'{base_url}/criar_anuncio'
    data = {'titulo': titulo, 'descricao': descricao, 'local': local, 'preco': preco}
    response = requests.post(url, json=data)
    print(f'Criar Anúncio:')
    print_response(response)
def show_menu():
    print("Escolha uma opção:")
    print("1. Visualizar um anúncio específico")
    print("2. Visualizar as avaliações de um anúncio específico")
    print("3. Visualizar todos os anúncios")
    print("4. Avaliar um anúncio")
    print("5. Criar um novo anúncio")
    print("6. Sair")
def main():
    while True:
        show_menu()
        opcao = input("Digite o número da opção desejada: ")
        if opcao == '1':
            id_anuncio = input("Digite o ID do anúncio: ")
            test_visualizar_anuncio(int(id_anuncio))
        elif opcao == '2':
            id_anuncio = input("Digite o ID do anúncio: ")
            test_visualizar_avaliacoes(int(id_anuncio))
        elif opcao == '3':
            test_visualizar_todos_anuncios()
        elif opcao == '4':
            id_anuncio = input("Digite o ID do anúncio: ")
            estrelas = input("Digite o número de estrelas para a avaliação: ")
            test_avaliar(int(id_anuncio), int(estrelas))
        elif opcao == '5':
            titulo = input("Digite o título do anúncio: ")
            descricao = input("Digite a descrição do anúncio: ")
            local = input("Digite o local do anúncio: ")
            preco = input("Digite o preço do anúncio: ")
            test_criar_anuncio(titulo, descricao, local, float(preco))
        elif opcao == '6':
            print("Saindo do aplicativo...")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
if __name__ == '__main__':
    main()
