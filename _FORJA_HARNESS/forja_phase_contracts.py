"""Load and validate versioned FORJA N3 phase contracts."""

from __future__ import annotations


from forja_n3_common import FORJA, PHASES, ForjaN3Error, canonical_hash, read_json


CONTRACT_DIR = FORJA / "phase_contracts"
N4_CONTRACT_DIR = FORJA / "phase_contracts_n4"


def load_contract(phase: str) -> dict:
    if phase not in PHASES:
        raise ForjaN3Error(f"fase desconhecida: {phase}")
    path = CONTRACT_DIR / f"F{PHASES.index(phase)}.json"
    contract = read_json(path, None)
    if not isinstance(contract, dict):
        raise ForjaN3Error(f"contrato ausente ou inválido: {path}")
    required = {
        "schemaVersion", "phase", "order", "producerRole", "reviewerRole",
        "requiredInputs", "requiredOutputs", "requiredGates", "nextPhase", "retryPolicy",
    }
    missing = sorted(required - set(contract))
    if missing:
        raise ForjaN3Error(f"contrato {path.name} sem campos: {missing}")
    if contract["phase"] != phase or contract["order"] != PHASES.index(phase):
        raise ForjaN3Error(f"contrato {path.name} diverge da ordem canônica")
    if contract["producerRole"] == contract["reviewerRole"]:
        raise ForjaN3Error(f"contrato {path.name} não separa produtor e revisor")
    if contract["nextPhase"] != (PHASES[contract["order"] + 1] if contract["order"] + 1 < len(PHASES) else None):
        raise ForjaN3Error(f"nextPhase inválida em {path.name}")
    contract["contractPath"] = str(path)
    contract["contractHash"] = canonical_hash({key: value for key, value in contract.items() if not key.startswith("contract")})
    candidate = read_json(N4_CONTRACT_DIR / path.name, None)
    if isinstance(candidate, dict):
        contract["n4Candidate"] = {
            "specVersion": candidate.get("specVersion"),
            "mode": candidate.get("mode"),
            "requiredOutputs": candidate.get("n4RequiredOutputs") or [],
            "requiredGates": candidate.get("n4RequiredGates") or [],
            "contractPath": str(N4_CONTRACT_DIR / path.name),
            "contractHash": canonical_hash(candidate),
        }
    return contract


def validate_all() -> list[dict]:
    return [load_contract(phase) for phase in PHASES]


if __name__ == "__main__":
    for item in validate_all():
        print(item["phase"], item["contractHash"])
