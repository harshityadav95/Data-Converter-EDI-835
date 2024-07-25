from typing import Optional

from elements import Element
from elements.utilities import split_element


class ServiceModifier(Element):

	def parser(self, value: str) -> Optional[str]:
		value = split_element(value)
		if len(value) > 2:
			return value[2]
