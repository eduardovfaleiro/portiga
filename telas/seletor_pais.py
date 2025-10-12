import os, json

from models.pais import Pais

class SeletorPais:
    __paises: dict[str, str] = {}
        
    PAISES_FILE_PATH = os.path.join(os.path.dirname(__file__), 'countries.json')
    
    try:
        with open('countries.json', 'r', encoding='utf-8') as f:
            paises_dict = json.load(f)
            __paises = {item.get('code'): item.get('name') for item in paises_dict}
    except FileNotFoundError:
        print("ERRO: O arquivo countries.json não foi encontrado. A lista de países está vazia.")
    except json.JSONDecodeError:
        print("ERRO: Falha ao decodificar o JSON do arquivo countries.json.")

    def retorna_pais(self, codigo_pais: str) -> Pais | None:
        pais_nome = self.__paises.get(codigo_pais)

        if pais_nome is not None:
            return Pais(codigo=codigo_pais, nome=pais_nome)
        else:
            return None