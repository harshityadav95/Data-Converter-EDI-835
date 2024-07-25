import json
from typing import Dict, List

from segments.interchange import Interchange as InterchangeSegment
from segments.financial_information import FinancialInformation as FinancialInformationSegment
from utilities import find_identifier
from loops.organization import Organization as OrganizationLoop
from loops.claim import Claim as ClaimLoop
from loops.service import Service as ServiceLoop
from loops.provider_adjustment import ProviderAdjustment as ProviderAdjustmentLoop
from transaction_set_builder import TransactionSet


def json_to_edi(json_data: str) -> str:
    """Converts a JSON representation back to EDI 835 format.

    Args:
        json_data (str): The JSON string representing an EDI 835 transaction set.

    Returns:
        str: The EDI 835 representation of the JSON data.
    """

    data = json.loads(json_data)
    transaction_set = _build_transaction_set(data)

    segments = []
    segments.append(transaction_set.interchange.to_edi())
    segments.append(transaction_set.financial_information.to_edi())

    for organization in transaction_set.organizations:
        segments.extend(organization.to_edi())

    for claim in transaction_set.claims:
        segments.append(claim.claim.to_edi())
        segments.extend(entity.to_edi() for entity in claim.entities)

        for reference in claim.references:
            segments.append(reference.to_edi())

        for date in claim.dates:
            segments.append(date.to_edi())

        if claim.amount:
            segments.append(claim.amount.to_edi())

        for service in claim.services:
            segments.append(service.service.to_edi())
            segments.extend(date.to_edi() for date in service.dates)
            segments.extend(reference.to_edi() for reference in service.references)
            segments.extend(remark.to_edi() for remark in service.remarks)

            if service.amount:
                segments.append(service.amount.to_edi())

            segments.extend(adjustment.to_edi() for adjustment in service.adjustments)

    # Add provider adjustments to EDI output
    for provider_adjustment in transaction_set.provider_adjustments:
        segments.extend(provider_adjustment.to_edi())

    segments.append('SE*')
    segments.append('GE*')
    segments.append('IEA*')

    return '~'.join(segments)



def _build_transaction_set(data: Dict) -> TransactionSet:
    """Builds a TransactionSet object from JSON data."""

    interchange = InterchangeSegment.from_dict(data['interchange'])
    financial_information = FinancialInformationSegment.from_dict(data['financial_information'])
    claims = [_build_claim(claim_data) for claim_data in data['claims']]
    organizations = [_build_organization(org_data) for org_data in data['organizations']]
    return TransactionSet(interchange, financial_information, claims, organizations)


def _build_claim(claim_data: Dict) -> ClaimLoop:
    """Builds a ClaimLoop object from JSON data."""

    claim = ClaimSegment.from_dict(claim_data['claim'])
    entities = [EntitySegment.from_dict(entity_data) for entity_data in claim_data['entities']]
    services = [_build_service(service_data) for service_data in claim_data['services']]
    references = [ReferenceSegment.from_dict(reference_data) for reference_data in claim_data['references']]
    dates = [DateSegment.from_dict(date_data) for date_data in claim_data['dates']]
    amount = AmountSegment.from_dict(claim_data.get('amount'))
    return ClaimLoop(claim, entities, services, references, dates, amount)


def _build_service(service_data: Dict) -> ServiceLoop:
    """Builds a ServiceLoop object from JSON data."""

    service = ServiceSegment.from_dict(service_data['service'])
    dates = [DateSegment.from_dict(date_data) for date_data in service_data['dates']]
    references = [ReferenceSegment.from_dict(reference_data) for reference_data in service_data['references']]
    remarks = [RemarkSegment.from_dict(remark_data) for remark_data in service_data['remarks']]
    amount = AmountSegment.from_dict(service_data.get('amount'))
    adjustments = [ServiceAdjustmentSegment.from_dict(adjustment_data)
                    for adjustment_data in service_data['adjustments']]
    return ServiceLoop(service, dates, references, remarks, amount, adjustments)


def _build_organization(org_data: Dict) -> OrganizationLoop:
    """Builds an OrganizationLoop object from JSON data."""

    organization = OrganizationSegment.from_dict(org_data['organization'])
    location = LocationSegment.from_dict(org_data.get('location'))
    address = AddressSegment.from_dict(org_data.get('address'))
    return OrganizationLoop(organization, location, address)

if __name__ == "__main__":
    pass 