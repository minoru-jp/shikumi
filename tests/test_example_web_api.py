from shikumi import StructuralKind
from web_api import api
from web_api.api import users
from web_api.api.users import GetUser
from web_api.shikumi_lib.realizers.markdown import MarkdownRealizer
from web_api.shikumi_lib.norms import Method, Path, web_api, web_api_structure


def test_web_api_example_supports_entity_module_and_package_foci() -> None:
    entity_result = web_api.validate(GetUser)
    module_result = web_api.validate(users, placement=("example", "web_api", "api", "users"))
    package_result = web_api.validate(api, structure_specification=web_api_structure)

    assert entity_result.is_valid
    assert module_result.is_valid
    assert package_result.is_valid

    entity_view = web_api.view(GetUser)
    assert entity_view.focused.values(Method) == ("GET",)
    assert entity_view.focused.values(Path) == ("/users/{user_id}",)

    module_view = web_api.view(users)
    assert {item.subject.__name__ for item in module_view.entities} == {
        "GetUser",
        "ListUsers",
        "UpdateUser",
    }

    package_view = web_api.view(api)
    assert len(package_view.entities) == 6


def test_web_api_example_realizes_markdown_from_package_view() -> None:
    view = web_api.view(api)
    realizer = MarkdownRealizer()
    assert realizer.check(view).is_realizable
    artifact = realizer.realize(view)

    assert artifact.startswith("# Example Web API\n")
    assert "### GET `/users/{user_id}`" in artifact
    assert "### POST `/articles`" in artifact
    assert "Related: ListArticles, GetUser" in artifact


def test_web_api_exposes_descriptor_use_rules() -> None:
    from web_api.shikumi_lib.norms import web_api

    assert len(web_api.descriptor_rules) == 5
    assert all(rule.allowed.kind is StructuralKind.ENTITY for rule in web_api.descriptor_rules)
