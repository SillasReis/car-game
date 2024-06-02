# Car Game

## Instalar

_(É necessário ter o poetry previamente instalado na máquina. Para mas informações, acesse [python-poetry.org](https://python-poetry.org/))_

Para instalar as dependências do projeto, execute o seguinte comando:

```shell
poetry install
```

## Executar

Para executar o projeto, execute o comando:

```shell
poetry run python car_game
```

## Criação de Pistas
 Para criar pistas, crie uma imagem com tamanho 1080x720 pixels e deixe o desenho do traçado da pista transparente. O background será sempre preto, então a cor da pista deve ser diferente.

Após criar a imagem no formato PNG, ela deve ser salva na pasta [car_game/imgs](./car_game/imgs/) com o prefixo
`track-`.

Exemplos de pistas podem ser encontrados na pasta destino. Um modelo de pista feito no GIMP está presente em [track-generator.xcf](track-generator.xcf)

## Ferramentas Utilizadas

* [Neat Python](https://neat-python.readthedocs.io/en/latest/)
* [PyGame](https://www.pygame.org/news)
* [Python Prompt Toolkit](https://python-prompt-toolkit.readthedocs.io/en/master/index.html)