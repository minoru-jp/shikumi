"""A tiny layered application described with Shikumi information."""

from ..shikumi_lib.norms import depends_on, layer


@layer("domain")
class Order:
    """Domain entity."""


@layer("application")
class PlaceOrder:
    """Application service that depends on the domain model."""

    depends_on @= Order


@layer("infrastructure")
class SqlOrderRepository:
    """Infrastructure adapter that depends on the domain model."""

    depends_on @= Order
