from dataclasses import dataclass
from enum import Enum
from typing import Any, TYPE_CHECKING, Dict

from ..hardware import SysInfo
from ..output import info

if TYPE_CHECKING:
	_: Any


@dataclass
class Firewall(Enum):
	Iptables = 'iptables'
	Nftables = 'nftables'

	@staticmethod
	def no_firewall_text() -> str:
		return str(_('No Firewall'))


@dataclass
class FirewallConfiguration:
	firewall: Firewall

	def __dump__(self) -> Dict[str, Any]:
		return {
			'firewall': self.firewall.value
		}

	@staticmethod
	def parse_arg(arg: Dict[str, Any]) -> 'FirewallConfiguration':
		return FirewallConfiguration(
			Firewall(arg['firewall'])
		)

	def install_firewall_config(
		self,
		installation: Any
	):
		info(f'Installing Firewall backend/frontend: {self.firewall.name}')

		match self.firewall:
			case Firewall.Iptables:
				installation.add_additional_packages("iptables ufw ufw-extras")
			case Firewall.Nftables:
				installation.add_additional_packages("nftables firewalld")