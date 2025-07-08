# Relógio Digital Profissional (Python & Tkinter)

Um relógio digital moderno e responsivo, construído em Python com a biblioteca Tkinter, inspirado em designs futuristas e minimalistas. Este projeto demonstra habilidades em criação de interfaces gráficas, manipulação de tempo e adaptação de design UI/UX.

![Sem nome (600 x 600 px) (1)](https://github.com/user-attachments/assets/dd15dd22-f3b4-4887-80a7-37fb5f319722)

## Funcionalidades

* **Exibição Precisa:** Mostra a hora (HH:MM:SS), AM/PM e a data completa (Dia da Semana, Dia, Mês, Ano).
* **Design Profissional:** Interface elegante com fundo gradiente, "vidro" translúcido (simulado) e cores vibrantes.
* **Responsivo:** O tamanho da fonte e o layout se adaptam automaticamente ao redimensionamento da janela, garantindo uma boa experiência visual em diferentes tamanhos.
* **Fonte Digital:** Utiliza a fonte 'Orbitron' para um visual autêntico de relógio digital.
* **Dois Pontos Fixos:** Os separadores de hora e minuto são estáticos, sem animação de piscar.

## Como Executar

Siga os passos abaixo para ter o Relógio Digital funcionando em sua máquina.

### Pré-requisitos

Certifique-se de ter o Python instalado (versão 3.6 ou superior). O Tkinter geralmente já vem incluído com a instalação padrão do Python.

**Recomendado:** Para a melhor experiência visual, instale a fonte **Orbitron** em seu sistema operacional:
1.  Visite [Google Fonts - Orbitron](https://fonts.google.com/specimen/Orbitron) ou um site similar para baixar a família de fontes.
2.  **No Windows:** Clique com o botão direito nos arquivos `.ttf` (TrueType Font) baixados e selecione "Instalar".
3.  **No macOS:** Dê dois cliques nos arquivos da fonte e clique em "Instalar Fonte".
4.  **No Linux:** Copie os arquivos `.ttf` para `~/.local/share/fonts/` e execute `fc-cache -f -v` no terminal para atualizar o cache das fontes.

### Instalação

1.  Clone este repositório (ou baixe os arquivos diretamente):
    ```bash
    git clone [https://github.com/Joaofernandes-DEV/RelogioDigitalPython.git](https://github.com/Joaofernandes-DEV/RelogioDigitalPython.git)
    cd RelogioDigitalPython
    ```

2.  Navegue até a pasta `src`:
    ```bash
    cd src
    ```

### Execução

1.  Execute o script Python:
    ```bash
    python RelogioDigital.py
    ```

O relógio digital será aberto em uma nova janela. Tente redimensionar a janela para ver o efeito responsivo!

## Tecnologias Utilizadas

* **Python 3.x**
* **Tkinter:** Biblioteca padrão do Python para criação de interfaces gráficas (GUIs).
* **`datetime`:** Módulo Python para manipulação de datas e horas.
* **Fonte Orbitron:** Para o estilo visual do relógio.

## Como o Projeto foi Construído

O relógio é construído usando uma abordagem de programação orientada a objetos com a classe `ProfessionalDigitalClock`.

* **Fundo Gradiente:** Um `tk.Canvas` é usado para desenhar um gradiente de cor dinâmico que se ajusta ao tamanho da janela.
* **"Clock Face" (Elemento Central):** Um `tk.Frame` com bordas estilizadas e fundo translúcido (simulado por uma cor sólida) atua como o display do relógio, centralizado no Canvas.
* **Responsividade:** A função `_on_window_resize` é vinculada ao evento de redimensionamento da janela. Ela recalcula os tamanhos das fontes e a posição dos elementos com base nas dimensões atuais da janela, garantindo que o relógio se adapte suavemente.
* **Atualização do Tempo:** A função `_update_clock` é chamada a cada segundo usando `master.after(1000, ...)`, mantendo a hora e a data sempre atualizadas.
* **Formatação:** O módulo `datetime` é usado para formatar a hora (HH:MM:SS AM/PM) e a data (dia da semana, dia, mês, ano) em português.

---

##  Desenvolvimento

Este projeto foi desenvolvido por:

| [<img src="https://avatars.githubusercontent.com/u/170758704?s=400&u=da7a33d81f3feeb953e687442cba5d042527f94d&v=4" width=115><br><sub>João Vitor Fernandes</sub>](https://github.com/Joaofernandes-DEV) |
|:----------------------------------------------------------------------------------------------------------------------------------------------------------:|

## 📝 Licença

Este projeto está licenciado sob a licença MIT - veja o arquivo [LICENSE](LICENSE) para detalhes.
