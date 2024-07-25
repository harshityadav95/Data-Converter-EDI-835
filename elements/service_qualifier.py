from elements import Element
from elements.utilities import split_element


class ServiceQualifer(Element):

	def parser(self, value: str) -> str:
		value = split_element(value)
		qualifier, *_ = value
		return qualifier
