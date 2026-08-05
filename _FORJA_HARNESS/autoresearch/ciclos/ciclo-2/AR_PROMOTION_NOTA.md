# Nota da bancada — ciclo AR-2: NENHUMA PROMOÇÃO

O comando `promotion` retornou `technical_candidate_passed`, mas essa saída NÃO se aplica ao varH:
o julgamento cego válido de t1b elegeu por hash o artefato `fad08dc6…` — que é o VIGENTE (e3),
não a variante (e1 = `f2c8e868…`). Em t2b o resultado foi empate (kappa 0.0, sem vencedor).

**Gap v1 nº 2 (registrado para correção na v1.1):** o promotion gate valida kappa, canários e
não-inferioridade, mas não confere se `winnerArtifactSha256` pertence à VARIANTE. A camada
evolutiva (`forja_ar_evolucao.py selecionar`) fez essa checagem e recusou: geração 1 fechada
com `winner: null`, contador de convergência 1/3.

Decisão da bancada: varH NÃO é candidata a nada; o prompt vigente permanece o baseline.
Revisão independente (A6a) não instaurada — não há candidata a revisar.
