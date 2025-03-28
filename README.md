# Client-Sockets-Dns
Implementação de um cliente DNS utilizando a linguagem de programação Python com Sockets para personalizar o comando dig.

##

Este trabalho prático envolve o desenvolvimento de um cliente DNS personalizado utilizando a linguagem de programação Python que consulta registros A (IPv4) e AAAA (IPv6) de servidores DNS. Além disso, o Wireshark foi usado para capturar e analisar pacotes ao utilizar o comando dig para enviar alguma consulta DNS para alguns serviços DNS público pelo prompt de comando. O estudo detalhado desses pacotes DNS no Wireshark mostrou campos importantes para o entendimento e identificação de padrões das respostas retornadas para o desenvolvimento do programa.

##

<h3>Metodologia</h3>

O programa foi desenvolvido a partir dos padrões das respostas retornadas das consultas DNS com o suporte da ferramenta Wireshark ao utilizar o comando dig. Com essas informações, foi possível identificar os campos necessários para a decodificação da resposta retornada e também da construção da consulta.

##

<h3>Funcionamento do código:</h3>

- 1. O usuário define um domínio e o tipo de consulta (A ou AAAA).
- 2. O código constroi uma consulta DNS com as informações fornecidas.
- 3. A consulta é enviada para o servidor DNS especificado (porta 53/UDP).
- 4. O servidor responde com informações sobre o domínio consultado (ex.: endereços IP).
- 5. A resposta é analisada e exibida decodificada, incluindo:
- Nome do domínio.
  - Tipo de registro (A ou AAAA).
  - Endereço IP correspondente (IPv4 ou IPv6).
  - Classe, TTL, e outros metadados.
 

<h6>Resposta do programa para python dns.py --type A --name www.wikipedia.org --server 8.8.8.8</h6>

<img src="https://github.com/user-attachments/assets/cc49cc08-1147-4bae-af9f-3f716e92d0dc" justify-content="center" align="center"> </br>


