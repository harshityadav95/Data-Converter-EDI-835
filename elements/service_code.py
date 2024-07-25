from elements import Element
from elements.utilities import split_element


class ServiceCode(Element):

	def parser(self, value: str) -> str:
		value = split_element(value)
		_, code, *_ = value
		return code
