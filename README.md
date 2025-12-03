# 🕒 Simulador de Ponto e Salário v2.0

Um aplicativo **Python** com interface gráfica (**Tkinter**) que simula o controle de ponto, cálculo de salário e gestão de presença de funcionários. Ideal para estudos, aprendizado de Python e simulação de ambientes corporativos.

---

## 🚀 Funcionalidades

- Registro e login de usuários por **cargo**.
- Simulação de dias de trabalho, incluindo:
  - Clima do dia (Ensolarado, Nublado, Chuva, Tempestade, Neve)
  - Tolerância de atrasos ou folgas de acordo com o clima
- Controle de **salário diário e acumulado**
- Gestão de **faltas justificadas e injustificadas**
- Alteração de cargo e reinício do ciclo de 30 dias
- Interface gráfica moderna com botões, mensagens e prompts interativos
- Compatível com múltiplos cargos e perfis

---

## 💼 Cargos Suportados

| Cargo        | Descrição                               | Dias de Trabalho | Salário Diário |
|--------------|----------------------------------------|----------------|----------------|
| func         | Segunda a Sexta, 9h-18h                | Seg-Sex        | R$ 120,00      |
| segurança    | Segunda a Sexta, 9h-18h                | Seg-Sex        | R$ 110,00      |
| t.i          | Apenas aos Sábados, 19h-22h            | Sábado         | R$ 250,00      |
| ceo          | Trabalho flexível                       | Flexível       | R$ 800,00      |
| dono         | Você é o dono, não bate ponto           | —              | R$ 2.000,00    |
| marketing    | Híbrido: Seg, Qua, Sex                  | Seg, Qua, Sex  | R$ 180,00      |
| rh           | Segunda a Sexta, 8h-17h                | Seg-Sex        | R$ 160,00      |
| estagiario   | Segunda a Sexta, 6h/dia                 | Seg-Sex        | R$ 60,00       |

---

## 🛠 Tecnologias

- **Python 3.x**
- **Tkinter** – para interface gráfica
- **JSON** – para armazenamento de usuários e dados de simulação
- **datetime** – controle de datas e ciclos de pagamento

---
