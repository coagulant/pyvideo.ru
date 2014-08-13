# coding: utf-8
class ProposalError(Exception):
    pass


class TemplateError(ProposalError):
    """Failed to meet the correct file structure."""
    pass


class ObjectError(ProposalError):
    """Failed to deserialize an object."""
    pass
