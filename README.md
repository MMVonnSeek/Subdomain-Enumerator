# SubEnum — Hybrid Subdomain Enumeration Framework  
### *Advanced Reconnaissance Engine for Offensive Security & Cyber Threat Analysis*

---
<img src="https://img.shields.io/badge/Autor-Max Muller-darkred?style=for-the-badge&logo=" alt="MMVonnSeek">

![Python](https://img.shields.io/badge/Python-3.10%2B-black?style=for-the-badge&logo=python)
![Security Research](https://img.shields.io/badge/Security%20Research-Ready-darkred?style=for-the-badge&logo=target)
![Offensive Security](https://img.shields.io/badge/Offensive%20Security-Ready-black?style=for-the-badge&logo=skynet)
![AsyncIO](https://img.shields.io/badge/AsyncIO-High%20Performance-darkred?style=for-the-badge&logo=fastapi)
[![Sponsor](https://img.shields.io/badge/Apoie_este_projeto-Sponsor-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/MMVonnSeek)

---

## Visão Geral

SubEnum é uma ferramenta híbrida de enumeração de subdomínios desenvolvida para ambientes de:

- Offensive Security  
- Bug Bounty  
- Threat Intelligence  
- Engenharia de Ataque  

**O framework combina:**

- Enumeração ativa  
- Enumeração passiva  
- DNS tradicional  
- DNS-over-HTTPS (DoH)  
- Wordlists extensíveis  
- APIs de Recon profissionais  

Com arquitetura limpa, modular e preparada para pipelines profissionais.

 <img src="/docs/imagens/dashboard.png" alt="Dashboard" width="800"/>
 
---

## Principais Recursos

### 1. Enumeração Híbrida (Ativa + Passiva)

| Fonte | Tipo | Requer API Key | Status |
|-------|------|----------------|--------|
| Wordlist bruteforce | Ativo | Não | ✔ |
| DNS resolver | Ativo | Não | ✔ |
| DNS-over-HTTPS (Cloudflare) | Ativo | Não | ✔ |
| crt.sh | Passivo | Não | ✔ |
| SecurityTrails | Passivo | Sim | ✔ |
| Shodan | Passivo | Sim | ✔ |

---

### 2. Execução Paralela de Alta Performance  

- AsyncIO  
- ThreadPool Executor  
- Resolução massiva (milhares por segundo)  
- Detecção automática de wildcard DNS  

---

### 3. Dashboard HTML Automático  

Gerado após a execução contendo:

- Mapa de subdomínios  
- Fontes: ativo / passivo / wildcard  
- Estatísticas  
- Profundidade da árvore DNS  

---

### 4. Logging Estruturado + Telemetria  

Formato JSON-Lines:

{"time": "2025-11-20 17:38:37", "level": "INFO", "name": "subenum.core", "msg": "Starting hybrid enumeration for example.com"}
Compatível com:

- Splunk
- ELK Stack
- Datadog
- Loki / Grafana

---

### 5. Wordlists Modulares

default.txt → rápida
generate_mega_wordlist.py → gera mega_wordlist.txt (milhões de entradas)

---

### Instalação
**1. Faça um Fork do Repositório:** 
Antes de tudo, crie sua própria cópia deste projeto:

- Clique no botão Fork no canto superior direito do GitHub.

- Isso criará uma versão do repositório na sua conta.

**2. Clone o Seu Repositório Forkado:**

```
git clone https://github.com/MMVonnSeek/Subdomain-Enumerator.git

cd SubEnum
```

---
**3. Criar ambiente virtual e instalar dependências**

```
python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
```

---
**4. (Opcional) Instalar como pacote**

```
pip install -e .
```

---

### Como Usar
**1. Modo básico**

```
python -m subenum.cli --domain exemplo.com --wordlist wordlists/default.txt
```

---
**2. Modo Profundo (Mega Wordlist)**
Gerar a wordlist massiva:
```
python wordlists/generate_mega_wordlist.py
```

Executar enumeração profunda:
```
python -m subenum.cli \
  --domain target.com \
  --wordlist wordlists/mega_wordlist.txt \
  --dashboard dashboard.html
```

---
**3. Execução com Dashboard (scan padrão)**
```
python -m subenum.cli --domain target.com --wordlist wordlists/default.txt --dashboard dashboard.html
```

---
**4. Modo Passivo**

**crt.sh**
```
python -m subenum.cli --domain target.com --passive crtsh
```
---
**SecurityTrails**
```
export SECURITYTRAILS_KEY="SUA_API_KEY"

python -m subenum.cli --domain target.com --passive securitytrails
```
---
**Shodan**
```
export SHODAN_KEY="SUA_API_KEY"

python -m subenum.cli --domain target.com --passive shodan
```

<img src="/docs/imagens/cli_scan.png" alt="cliscan" width="800"/>

 ---
 
### Detecção de Wildcard DNS
**Exemplo de aviso:**

Wildcard DNS detected; results will be marked but still returned.
Resultado marcado:
{"subdomain": "test.example.com", "wildcard": true}

<img src="/docs/imagens/wildcard_detection.png" alt="Wildcard" width="800"/>

---

### Testes Automatizados
```
pytest -v
```
---

#### Benchmark

python -m subenum.cli \
  --domain target.com \
  --wordlist wordlists/ultimate_50k.txt \
  --benchmark \
  --threads 200
---
**Saída típica:**

[Benchmark] 50.000 resoluções em 8.2s (6.097 qps)

---

## Exemplo de Resultados

Após a enumeração de um domínio, o SubEnum produz um arquivo JSON estruturado com os subdomínios identificados, endereços IP associados, fontes de descoberta e outras informações relevantes:

<img src="/docs/imagens/results_json.png" alt="json" width="800"/>

---

## Contribuição

Se você gostou do projeto, não esqueça de:

-   ⭐ Deixar uma estrela no Repositório
    
-    Reportar bugs encontrados
    
-    Sugerir novas funcionalidades
    
-    Fazer um fork e contribuir
    

----------

## Licença

Este projeto é distribuído sob a Licença MIT, permitindo uso, modificação e distribuição livre, inclusive para fins comerciais, desde que os devidos créditos sejam mantidos.

Consulte o arquivo LICENSE para mais informações.
    

----------

<div align="center"> <sub> Feito por <strong>Prof. Max Muller - MMVonnSeek</strong> para a comunidade de segurança </sub>

  
  

[![Stars](https://img.shields.io/github/stars/MMVonnSeek/Subdomain-Enumerator?style=social)](https://github.com/MMVonnSeek/Subdomain-Enumerator/stargazers)
[![Forks](https://img.shields.io/github/forks/MMVonnSeek/Subdomain-Enumerator?style=social)](https://github.com/MMVonnSeek/Subdomain-Enumerator/network/members)
[![Follow](https://img.shields.io/github/followers/MMVonnSeek?style=social)](https://github.com/MMVonnSeek)

[![Sponsor](https://img.shields.io/badge/Apoie_este_projeto-Sponsor-ea4aaa?style=for-the-badge&logo=github-sponsors)](https://github.com/sponsors/MMVonnSeek)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-Max_Muller-0A66C2?style=for-the-badge&logo=linkedin&logoColor=white)](https://www.linkedin.com/in/max-muller-685705248/)

<br>

  [Voltar ao topo](#-Subdomain-Enumerator)

</div>
