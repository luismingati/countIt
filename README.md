# CountIT
O CountIT é baseado em um sistema de Ponto de Venda (PDV) é muito utilizado atualmente para ajudar na questão de fluxo de caixa de pequenas e grandes empresas.Junto ao PDV, também conta um gerenciamento do estoque, na abertura e fechamento de caixa e para controlar trocas e devoluções de forma mais simplificada e autônoma.
Essa ferramenta é essencial em vários negócios, porém, notamos que as vezes pode se tornar muito confusa pois muitas delas contém bastante funcionalidades irrelevantes que acabam só atrapalhando o usuário e são jogadas de forma desorganizada na tela, ofuscando assim algumas funcionalidades legais que poderiam estar sendo usadas mas estão sendo ofuscadas diante tantas informações.


# Proposta
A proposta do CountIT é simplificar esse sistema e colocar apenas ferramentas essenciais, com um layout minimalista e de simples entendimento. 

# Equipe

Esse projeto está sendo desenvolvido por 6 Alunos que estão cursando Ciências da Computação no Segundo Período na Cesar School.
São eles:

Pedro Henrique Andriotti Bastos - phab@cesar.school

Valter Costa Guerra Neto - vcgn@cesar.school

Kauan Victório Novello de Souza - kvns@cesar.school 

Ester Carvalho - eacm@cesar.school

Luis Otavio Campos Mingati - locm@cesar.school

Giovana Dantas Barreto Mariano - gdbm@cesar.school

# Ferramentas
Jira: https://easypdv.atlassian.net/jira/software/projects/EP/boards/1/backlog

Figma: https://www.figma.com/file/L4wsHpCyzswN1dpXPZfnpe/Prancha-Principal?node-id=0-1&t=wlwz17dQFPAbZac2-0

Protótipo Navegável Figma: https://www.figma.com/proto/L4wsHpCyzswN1dpXPZfnpe/Prancha-Principal?node-id=5-20&scaling=scale-down&page-id=0%3A1&starting-point-node-id=5%3A20

Diagrama de Atividades: https://drive.google.com/drive/folders/1G1dfJXF6Zx9hdQCyEuQXo-l9lDxswwAo?usp=share_link

Deploy: http://countit-7-env.eba-unrhmndk.us-east-1.elasticbeanstalk.com/

Manual do Usuário: https://drive.google.com/file/d/1AYKIETjZFx-hRj5OjETkEbk6ywj8JfDP/view?usp=sharing

# Experiência de Programação em Pares:
-Segunda Entrega: https://drive.google.com/file/d/1uro-NzbUQauQ-HGOdpUsdcTfkHmJ3ucW/view?usp=share_link 

-Terceira Entrega: https://drive.google.com/file/d/1gK48NTZBCWcVOqgeeZoJVA7hH2_wfqjn/view?usp=sharing

# Testes automatizados
Relizamos os testes automatizados utilizando a ferramenta Selenium, esta aba serve como um passo a passo para realizar os testes na nossa aplicação.

1- Acesse a pasta countIt, e na linha de comando:

```
pip install requirements.txt
```

2- garanta ter o webdriver do selenium instalado na raiz do projeto.

3- Os testes foram feitos através da validações das histórias que estão no Jira, foram dividos por funções, onde cada validação de cada história é executada de maneira independente.
   Para rodar, basta digitar na linha de comando:

```
1- python manage.py test app.tests.plataformTests.Ep27Tests_vd1
2- python manage.py test app.tests.plataformTests.Ep27Tests_vd2
3- python manage.py test app.tests.plataformTests.Ep5Tests
4- python manage.py test app.tests.plataformTests.Ep3Tests_vd1
5- python manage.py test app.tests.plataformTests.Ep3Tests_vd2
6- python manage.py test app.tests.plataformTests.Ep3Tests_vd3
```

Cada código é digitado um por vez na linha de comando.
   

