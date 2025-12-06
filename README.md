# SubEnum — Hybrid Subdomain Enumeration Framework  
### *Advanced Reconnaissance Engine for Offensive Security & Cyber Threat Analysis*

---
![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=for-the-badge&logo=python)
![Security Research](https://img.shields.io/badge/Security%20Research-Max%20Müller-darkred?style=for-the-badge&logo=target)
![Offensive Security](https://img.shields.io/badge/Offensive%20Security-Ready-black?style=for-the-badge&logo=skynet)
![AsyncIO](https://img.shields.io/badge/AsyncIO-High%20Performance-green?style=for-the-badge&logo=fastapi)

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

- default.txt → rápida
- ultimate_50k.txt → intermediária
- ultra_500k.txt → profunda
- generate_mega_wordlist.py → +5 milhões de entradas

---

### Instalação
**1. Faça um Fork do Repositório:** 
Antes de tudo, crie sua própria cópia deste projeto:

- Clique no botão Fork no canto superior direito do GitHub.

- Isso criará uma versão do repositório na sua conta.

**2. Clone o Seu Repositório Forkado:**

```
git clone https://github.com/SEU-USUSARIO/Subdomain-Enumerator.git

cd SubEnum
```

---
**3. Instalar dependências**

pip install -r requirements.txt

---
**4. (Opcional) Instalar como pacote**

pip install -e .

---

### Como Usar
**1. Modo básico**

python -m subenum.cli --domain exemplo.com --wordlist wordlists/default.txt

---
**2. Enumeração híbrida avançada**

python -m subenum.cli \
  --domain target.com \
  --wordlist wordlists/ultimate_50k.txt \
  --passive all \
  --doh \
  --async \
  --threads 200 \
  --dashboard dashboard.html \
  --log logs/output.log

---
**3. Modo Passivo**

**crt.sh**

python -m subenum.cli --domain target.com --passive crtsh

---
**SecurityTrails**

export SECURITYTRAILS_KEY="SUA_API_KEY"

python -m subenum.cli --domain target.com --passive securitytrails

---
**Shodan**

export SHODAN_KEY="SUA_API_KEY"

python -m subenum.cli --domain target.com --passive shodan

 ---
 
### Detecção de Wildcard DNS
**Exemplo de aviso:**

Wildcard DNS detected; results will be marked but still returned.
Resultado marcado:
{"subdomain": "test.example.com", "wildcard": true}

---

### Testes Automatizados

pytest -v

---

### Benchmark

python -m subenum.cli \
  --domain target.com \
  --wordlist wordlists/ultimate_50k.txt \
  --benchmark \
  --threads 200
---
**Saída típica:**

[Benchmark] 50.000 resoluções em 8.2s (6.097 qps)

---


*Contribuição*
Pull requests são bem-vindos.
Issues podem ser abertas para sugestões, dúvidas ou melhorias.

---

#### Autor
Professor: Max Müller

Se este projeto ajudou você a evoluir, deixe uma ⭐ e compartilhe o conhecimento. Obrigado por usar este repositório!
