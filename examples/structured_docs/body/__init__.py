"""Command catalog used by the structured-document example."""

from ..shikumi_lib.norms import category, command, content


@command("deploy")
@content
class Deploy:
    """Deploy the current build to the selected environment."""

    category @= "operations"


@command("status")
@content
class Status:
    """Show the current deployment status."""

    category @= "inspection"
