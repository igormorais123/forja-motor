import re
from pathlib import Path

texto = Path(r"..\Cafelana\CAFELANA_CR_EDCL_1-07-2026.docx.md").read_text(encoding='utf-8')

print('Contagens:')
print(f'  embargante: {len(re.findall(r"\bembargante(s)?\b", texto, re.I))}')
print(f'  embargada: {len(re.findall(r"\bembargada(s)?\b", texto, re.I))}')
print(f'  embargado: {len(re.findall(r"\bembargado(s)?\b", texto, re.I))}')
print(f'  embargad[oa] (união): {len(re.findall(r"\bembargad[oa](s)?\b", texto, re.I))}')
print(f'  provimento: {len(re.findall(r"\bprovimento\b", texto, re.I))}')
print(f'  desprovimento: {len(re.findall(r"\bdesprovimento\b", texto, re.I))}')
print(f'  procedência: {len(re.findall(r"\bprocedência\b", texto, re.I))}')
print(f'  improcedência: {len(re.findall(r"\bimprocedência\b", texto, re.I))}')
