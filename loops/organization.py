from typing import Iterator, Tuple, Optional

from segments.organization import Organization as OrganizationSegment
from segments.claim import Claim as ClaimSegment
from segments.address import Address as AddressSegment
from segments.location import Location as LocationSegment
from utilities import find_identifier


class Organization:
	initiating_identifier = OrganizationSegment.identification
	terminating_identifiers = [
		ClaimSegment.identification,
		OrganizationSegment.identification,
		'SE'
	]

	def __init__(self, organization: OrganizationSegment = None, location: LocationSegment = None,
				 address: AddressSegment = None):
		self.organization = organization
		self.location = location
		self.address = address

	def __repr__(self):
		return '\n'.join(str(item) for item in self.__dict__.items())

	@classmethod
	def build(cls, current_segment: str, segments: Iterator[str]) -> Tuple[
		'OrganizationSegment', Optional[Iterator[str]], Optional[str]
	]:
		organization = Organization()
		organization.organization = OrganizationSegment(current_segment)
		while True:
			try:
				segment = segments.__next__()
				identifier = find_identifier(segment)

				if identifier == AddressSegment.identification:
					organization.address = AddressSegment(segment)

				elif identifier == LocationSegment.identification:
					organization.location = LocationSegment(segment)

				elif identifier in cls.terminating_identifiers:
					return organization, segments, segment

			except StopIteration:
				return organization, None, None


if __name__ == '__main__':
	pass