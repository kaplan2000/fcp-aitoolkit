# O FCP AI-Toolkit 1.1.1 chegou: a 1.1, mais duas correções

Date: 2026-10-02
Status: Lançamento
Language: pt-BR
Canonical: https://www.fcp-aitoolkit.com/pt/blog/fcp-ai-toolkit-1-1-1/

A 1.1.1 já está na Mac App Store com Smart Cache, edição de legendas, Smart Search e cerca de 100 idiomas. O “.1” extra é por causa de dois bugs que corrigimos em cima da hora.

O FCP AI-Toolkit 1.1.1 está na Mac App Store desde 30 de setembro. Se você usa a versão 1.0, esta é a sua atualização. Abra a Mac App Store e atualize como sempre.


Esta versão trata de uma coisa só: voltar a uma edição sem recomeçar do zero. Você testa outro estilo, corta a abertura, corrige um nome, estende um clipe. As legendas acompanham você, em vez de começar do zero a cada vez.



## Espera, o que aconteceu com a 1.1?

Boa pergunta. Em 22 de setembro publicamos uma prévia chamada [Vem aí a versão 1.1](/pt/blog/fcp-ai-toolkit-1-1-preview/). A versão 1.1 estava pronta e revisada. Só esperava o vídeo de lançamento.


Então, em 25 de setembro, fizemos uma última rodada de testes em projetos reais do Final Cut Pro. Vários clipes, áudio desanexado, a bagunça típica de uma edição de verdade. Dois bugs apareceram. Corrigimos os dois no mesmo dia.


Poderíamos ter lançado a 1.1 e corrigido depois. Preferimos consertar a versão primeiro e dar a ela um novo número. Então a 1.1.1 é simplesmente a 1.1 mais duas correções. Os recursos são exatamente os que a prévia descrevia, e o “.1” extra representa os dois bugs que pegamos antes que você os conhecesse.


Enviamos a 1.1.1 à Apple em 27 de setembro, e ela entrou no ar em 30 de setembro. Ninguém perdeu uma versão: nunca existiu uma 1.1 pública. Se você está na 1.0, vai direto para a 1.1.1.


- 21 de junho de 2026A versão 1.0 é lançada22 de setembro de 2026A 1.1 é apresentada e espera o vídeo de lançamento25 de setembro de 2026O último teste acha dois bugs; ambos corrigidos no mesmo dia
- 27 de setembro de 2026A 1.1.1 vai para a análise da Apple30 de setembro de 2026A 1.1.1 está no ar na Mac App Store

## A primeira correção: legendas que ficavam umas sobre as outras

Quando você aciona Analyze, a extensão transcreve cada clipe de diálogo da sua linha do tempo separadamente e depois junta os resultados. Em alguns projetos, isso podia gerar a mesma fala duas vezes ou legendas sobrepostas. Encontramos três jeitos de isso acontecer:




- Um clipe aparado. Você corta o início de um clipe na linha do tempo, mas a fala da parte oculta, que foi cortada, ainda podia aparecer nas legendas.

- Dois clipes com a mesma fala. Pense no áudio da câmera mais um microfone separado, ambos marcados como diálogo. As mesmas palavras podiam aparecer duas vezes.

- O próprio modelo de fala. O Whisper às vezes retorna falas que se sobrepõem um pouco.

Isoladamente, isso já incomoda. Mas a 1.1.1 também traz um editor de legendas, e o editor faz algo sensato: recusa qualquer mudança de tempo que faça uma legenda se sobrepor à vizinha. Com duplicatas já sobrepostas, toda correção que você tentasse seria recusada. Você ficaria travado, com um editor que parecia trancado.


Veja o que acontece agora:




- As legendas de cada clipe são cortadas na parte que você realmente vê na linha do tempo, sem cortar palavras ao meio.

- A fala duplicada é unida em uma única legenda.

- Qualquer sobreposição restante é dividida de forma limpa.

- As legendas salvas antes da correção são reparadas automaticamente ao carregar.

E há um novo botão de remover em cada legenda. Se houver uma fala que você simplesmente não quer, apague-a. Ela continua apagada na próxima vez.



## A segunda correção: áudio que não estava onde pensávamos

Esta trata de áudio desanexado do vídeo ou que fica em um clipe conectado. Um caso comum é o som de um gravador separado, anexado ao seu clipe principal.


Nesses projetos, a extensão podia ler errado as posições na linha do tempo. Em um dos nossos projetos de teste, o áudio desanexado era mais longo que o vídeo. Só a duração do vídeo era transcrita, e as duas fontes ficavam 1,6 segundo distantes. As legendas saíam de sincronia.


Agora as posições dos clipes aninhados e conectados são calculadas corretamente. Um clipe conectado é medido no seu próprio enredo, em vez de ser cortado no comprimento do clipe ao qual está preso. A imagem de um clipe de vídeo deixa de ser confundida com uma fonte de áudio. E as funções de áudio, os clipes desativados e os canais de áudio desligados são respeitados.


As duas correções vieram do mesmo lugar: projetos reais. Ainda bem que testamos neles mais uma vez.



## Smart Cache: não recomece do zero

O Smart Cache lembra, no seu Mac, o que já foi transcrito.


Imagine só. Você legenda uma entrevista e fica satisfeito. Aí o cliente pede mais dez segundos no final. Você estende o clipe na linha do tempo e aciona Analyze de novo. Só a parte nova, ainda não transcrita, passa pelo Whisper. O resto já está lá.


Rode o mesmo clipe de novo, com o mesmo idioma e o mesmo modelo, e as legendas voltam na hora. Isso ajuda enquanto a edição ainda muda: teste outro estilo, rode de novo, corte, estenda, sem recomeçar a legendagem do zero.


O Smart Cache vem ativado por padrão. Há um interruptor na extensão se você quiser desativá-lo. A primeira execução de um clipe continua levando o tempo que levar, e isso depende do seu Mac, do seu clipe e do modelo. O Smart Cache ajuda na segunda execução, não na primeira.



## Corrija uma legenda antes que ela chegue à linha do tempo

Até um bom modelo de fala pode escrever o nome do seu convidado do jeito dele. Agora você pode corrigir um nome, uma pontuação ou uma frase inteira direto na extensão, antes que os títulos cheguem à linha do tempo.


Você também pode mudar o tempo de início e de fim de cada legenda. O editor confere os tempos conforme você edita. Ele recusa um intervalo inválido e uma legenda que se sobreponha à vizinha, para que uma pequena mudança não quebre a sequência sem você perceber.


Suas edições ficam salvas no seu Mac. Elas voltam quando você abre a extensão de novo ou analisa a mesma mídia outra vez. E, novidade da 1.1.1, você pode remover uma legenda que não quer.



## Smart Search: onde foi que eu disse isso?

Você lembra de ter falado algo sobre uma lente, mas não em qual vídeo. O Smart Search vasculha todas as legendas que você gerou, em todos os seus clipes. Cada resultado mostra o texto correspondente, o nome do arquivo e o timecode.


A busca também enxerga suas correções. Se você corrigiu um nome, é o nome corrigido que você encontra.


Um limite honesto: clicar em um resultado não leva ao clipe no Final Cut Pro. Você recebe o nome do arquivo e o timecode, e vai até lá por conta própria.



## Cerca de 100 idiomas e Auto Detect

A versão 1.0 tinha um seletor com 20 idiomas. Agora o menu de idiomas lista todos os cerca de 100 idiomas do catálogo de modelos Whisper. No topo há uma nova opção, Auto Detect. Se você não sabe qual idioma está em um clipe, ou mistura idiomas entre clipes, deixe que ele decida. O Auto Detect também roda no seu Mac, depois do download do modelo.


Leia esta parte com atenção. Esse número é a cobertura de idiomas do modelo. Não testamos a qualidade das legendas separadamente em cada idioma. A precisão das legendas depende do idioma, da gravação, de quem fala e do modelo. Por isso, revisar as legendas continua fazendo parte do trabalho, em qualquer idioma. Com o novo editor, isso também fica mais rápido.



## Janelas menores

A extensão agora cabe em janelas menores do Final Cut Pro, por exemplo na tela de um notebook. A área para soltar o projeto, a busca e as opções de modelos continuam acessíveis.



## O que continua igual



- A transcrição ainda roda no seu Mac. Usamos o WhisperKit, que é baseado no Whisper da OpenAI. Seu material não é enviado a um serviço de transcrição na nuvem. O modelo de fala é baixado uma vez, e isso exige internet. Compras na App Store e verificações de assinatura também usam a internet.

- Os mesmos cinco modelos. Basic, Highlighted, Highlighted with Background, Pop e Beast Pop. Fonte, cor e posição continuam ajustáveis.

- O mesmo resultado organizado. Seus títulos voltam agrupados em um clipe composto em um enredo secundário.

- O mesmo modelo de preços. O app é gratuito para baixar e os modelos são gratuitos. As legendas automáticas por IA exigem uma assinatura mensal ativa. Para ver os preços atuais, consulte a [página na Mac App Store](https://apps.apple.com/app/id6775619373).


## O que não está nesta atualização

Para você não ficar na dúvida: a 1.1.1 não tem exportação de SRT nem de outros arquivos de legenda, não tem conversão de texto em fala e não tem envio automático para o YouTube. A busca encontra palavras, não imagens nem ideias, então não há busca visual ou semântica. E, como dito acima, um resultado de busca não leva ao clipe.


Já estamos trabalhando na próxima atualização. Não vamos prometer nada sobre ela aqui. Preferimos avisar quando estiver pronta.



## Baixe, assista e conte o que achou

Para atualizar, abra a [Mac App Store](https://apps.apple.com/app/id6775619373) e instale o FCP AI-Toolkit 1.1.1. A página na App Store agora está disponível em 10 idiomas e tem um vídeo de prévia curto.


Para vê-lo em ação, assista ao [vídeo de lançamento no YouTube](https://www.youtube.com/watch?v=ZvGX2RwCvH8). Nossos primeiros vídeos, um de lançamento e os Shorts, estão no [YouTube](https://www.youtube.com/@FCPAIToolkit) e no [Instagram](https://www.instagram.com/fcpaitoolkit/) como Reels. Também estamos no [TikTok](https://www.tiktok.com/@fcpaitoolkit). Se quiser saber como chegamos até aqui, a [publicação da 1.0](/pt/blog/fcp-ai-toolkit-1-0/) e a [prévia da 1.1](/pt/blog/fcp-ai-toolkit-1-1-preview/) continuam no ar.


Se algo não funcionar no seu projeto, ou se você tiver uma ideia, escreva para help@fcp-aitoolkit.com. Um projeto real com um problema real é o melhor teste que podemos ter. Foi assim que encontramos esses dois bugs.


Obrigado por usar o FCP AI-Toolkit.
