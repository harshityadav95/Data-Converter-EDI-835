from typing import Optional

from elements import Element


class Dollars(Element):

	def parser(self, value: str) -> Optional[float]:
		if value != '':
			return float(value)
