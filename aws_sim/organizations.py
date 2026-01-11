"""AWS Organizations simulator.

Tracks accounts, organizational units, and service control policies (SCP).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Dict, List


@dataclass(frozen=True)
class Account:
    account_id: str
    name: str
    email: str


@dataclass(frozen=True)
class OrganizationalUnit:
    ou_id: str
    name: str
    accounts: List[Account] = field(default_factory=list)


@dataclass(frozen=True)
class ServiceControlPolicy:
    policy_id: str
    name: str
    denied_actions: List[str]


class OrganizationsService:
    def __init__(self) -> None:
        self._accounts: Dict[str, Account] = {}
        self._ous: Dict[str, OrganizationalUnit] = {}
        self._scps: Dict[str, ServiceControlPolicy] = {}
        self._counter = 0

    def create_account(self, name: str, email: str) -> Account:
        self._counter += 1
        account_id = f"{self._counter:012d}"
        account = Account(account_id=account_id, name=name, email=email)
        self._accounts[account_id] = account
        return account

    def create_organizational_unit(self, name: str) -> OrganizationalUnit:
        self._counter += 1
        ou_id = f"ou-{self._counter:04d}"
        ou = OrganizationalUnit(ou_id=ou_id, name=name)
        self._ous[ou_id] = ou
        return ou

    def move_account(self, account_id: str, ou_id: str) -> None:
        account = self._accounts.get(account_id)
        if account is None:
            raise KeyError("Account not found")
        ou = self._ous.get(ou_id)
        if ou is None:
            raise KeyError("OU not found")
        ou.accounts.append(account)

    def create_scp(self, name: str, denied_actions: List[str]) -> ServiceControlPolicy:
        self._counter += 1
        policy_id = f"p-{self._counter:04d}"
        policy = ServiceControlPolicy(policy_id=policy_id, name=name, denied_actions=denied_actions)
        self._scps[policy_id] = policy
        return policy

    def list_accounts(self) -> List[Account]:
        return list(self._accounts.values())

    def list_organizational_units(self) -> List[OrganizationalUnit]:
        return list(self._ous.values())

    def list_scps(self) -> List[ServiceControlPolicy]:
        return list(self._scps.values())
