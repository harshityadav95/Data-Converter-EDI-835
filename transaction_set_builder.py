from typing import List, Dict, Iterator, Optional, Tuple
from collections import namedtuple

from loop_builder import LoopBuilder
from segments.interchange import Interchange as InterchangeSegment
from segments.financial_information import FinancialInformation as FinancialInformationSegment
from utilities import find_identifier
from loops.organization import Organization as OrganizationLoop
from loops.claim import Claim as ClaimLoop
from loops.provider_adjustment import ProviderAdjustment as ProviderAdjustmentLoop

BuildAttributeResponse = namedtuple('BuildAttributeResponse', 'key value segment segments')


class TransactionSetBuilder:
    """Constructs the complete EDI 835 transaction set."""

    def __init__(self, segment_delimiter: str = "*"):
        self.loop_builder = LoopBuilder(segment_delimiter)

    def build(self, segments: Iterator[str]) -> 'TransactionSet':
        """Builds the EDI 835 transaction set from the segments.

        Args:
            segments (Iterator[str]): An iterator of EDI segments.

        Returns:
            TransactionSet: The built transaction set.
        """

        interchange = None
        financial_information = None
        claims = []
        organizations = []
        provider_adjustments = []  # Add a list to store provider adjustments

        loop_structure = self.loop_builder.build(segments)
        segments = iter(loop_structure)
        segment = None

        while True:
            response = self._build_attribute(segment, segments)
            segment = response.segment
            segments = response.segments

            if response.segments is None:
                break

            if response.key == 'interchange':
                interchange = response.value

            if response.key == 'financial information':
                financial_information = response.value

            if response.key == 'organization':
                organizations.append(response.value)

            if response.key == 'claim':
                claims.append(response.value)
            
            if response.key == 'provider_adjustment':  # Handle provider adjustments
                provider_adjustments.append(response.value)

        return TransactionSet(interchange, financial_information, claims, organizations, provider_adjustments)

    def _build_attribute(self, segment: Optional[Dict], segments: Iterator[List[Dict]]) -> BuildAttributeResponse:
        if segment is None:
            try:
                segment = segments.__next__()
            except StopIteration:
                return BuildAttributeResponse(None, None, None, None)

        identifier = find_identifier(segment)

        if identifier == InterchangeSegment.identification:
            interchange = InterchangeSegment(segment[identifier][0])
            return BuildAttributeResponse('interchange', interchange, None, segments)

        if identifier == FinancialInformationSegment.identification:
            financial_information = FinancialInformationSegment(segment[identifier][0])
            return BuildAttributeResponse('financial information', financial_information, None, segments)

        if identifier == OrganizationLoop.initiating_identifier:
            organization, segments, segment = OrganizationLoop.build(segment, segments)
            return BuildAttributeResponse('organization', organization, segment, segments)

        elif identifier == ClaimLoop.initiating_identifier:
            claim, segments, segment = ClaimLoop.build(segment, segments)
            return BuildAttributeResponse('claim', claim, segment, segments)
        
        elif identifier == ProviderAdjustmentLoop.initiating_identifier:  # Handle provider adjustments
            provider_adjustment, segments, segment = ProviderAdjustmentLoop.build(segment, segments)
            return BuildAttributeResponse('provider_adjustment', provider_adjustment, segment, segments)

        else:
            return BuildAttributeResponse(None, None, segment, segments)


class TransactionSet:
    """Represents a complete EDI 835 transaction set."""

    def __init__(
            self,
            interchange: InterchangeSegment,
            financial_information: FinancialInformationSegment,
            claims: List[ClaimLoop],
            organizations: List[OrganizationLoop],
            provider_adjustments: List[ProviderAdjustmentLoop] = None, # Add provider adjustments
    ):
        self.interchange = interchange
        self.financial_information = financial_information
        self.claims = claims
        self.organizations = organizations
        self.provider_adjustments = provider_adjustments if provider_adjustments else [] # Add provider adjustments

    def __repr__(self):
        return '\n'.join(str(item) for item in self.__dict__.items())

    @property
    def payer(self) -> OrganizationLoop:
        payer = [o for o in self.organizations if o.organization.type == 'payer']
        assert len(payer) == 1
        return payer[0]

    @property
    def payee(self) -> OrganizationLoop:
        payee = [o for o in self.organizations if o.organization.type == 'payee']
        assert len(payee) == 1
        return payee[0]

if __name__ == "__main__":
    pass