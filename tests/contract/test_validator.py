"""Contract test cases for ready."""
from typing import Any

from aiohttp import ClientSession, hdrs, MultipartWriter
import pytest
from rdflib import Graph
from rdflib.compare import graph_diff, isomorphic


@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_with_file(http_service: Any) -> None:
    """Should return OK and successful validation."""
    url = f"{http_service}/validator"
    filename = "tests/files/catalog_1.ttl"

    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(open(filename, "rb"))
        p.set_content_disposition("attachment", name="file", filename=filename)

    session = ClientSession()
    async with session.post(url, data=mpwriter) as resp:
        body = await resp.text()
    await session.close()

    assert resp.status == 200
    assert "text/turtle" in resp.headers[hdrs.CONTENT_TYPE]

    # results_graph (validation report) should be isomorphic to the following:
    src = """
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    [] a sh:ValidationReport ;
         sh:conforms true
         .
    """
    g1 = Graph().parse(data=body, format="text/turtle")
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic, "results_graph is incorrect"


@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_with_text(http_service: Any) -> None:
    """Should return OK and successful validation."""
    url = f"{http_service}/validator"
    with open("tests/files/catalog_1.ttl", "r") as file:
        text = file.read()

    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(text, {"CONTENT-TYPE": "text/turtle"})
        p.set_content_disposition("inline", name="text")

    session = ClientSession()
    async with session.post(url, data=mpwriter) as resp:
        body = await resp.text()
    await session.close()

    assert resp.status == 200
    assert "text/turtle" in resp.headers[hdrs.CONTENT_TYPE]

    # results_graph (validation report) should be isomorphic to the following:
    src = """
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    [] a sh:ValidationReport ;
         sh:conforms true
         .
    """
    g1 = Graph().parse(data=body, format="text/turtle")
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic, "results_graph is incorrect"


@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_with_text_json_ld(http_service: Any) -> None:
    """Should return OK and successful validation."""
    url = f"{http_service}/validator"
    with open("tests/files/catalog_1.json", "r") as file:
        text = file.read()

    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(text, {"CONTENT-TYPE": "application/ld+json"})
        p.set_content_disposition("inline", name="text")

    session = ClientSession()
    async with session.post(url, data=mpwriter) as resp:
        body = await resp.text()
    await session.close()

    assert resp.status == 200
    assert "text/turtle" in resp.headers[hdrs.CONTENT_TYPE]

    # results_graph (validation report) should be isomorphic to the following:
    src = """
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    [] a sh:ValidationReport ;
         sh:conforms true
         .
    """
    g1 = Graph().parse(data=body, format="text/turtle")
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic, "results_graph is incorrect"


@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_accept_json_ld(http_service: Any) -> None:
    """Should return OK and successful validation and content-type should be json-ld."""
    url = f"{http_service}/validator"
    filename = "tests/files/catalog_1.ttl"
    headers = {"Accept": "application/ld+json"}

    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(open(filename, "rb"))
        p.set_content_disposition("attachment", name="file", filename=filename)

    session = ClientSession()
    async with session.post(url, headers=headers, data=mpwriter) as resp:
        # ...
        body = await resp.text()
    await session.close()

    assert resp.status == 200
    assert "application/ld+json" in resp.headers[hdrs.CONTENT_TYPE]

    # results_graph (validation report) should be isomorphic to the following:
    src = """
    [
      {
        "@type": [
          "http://www.w3.org/ns/shacl#ValidationReport"
        ],
        "http://www.w3.org/ns/shacl#conforms": [
          {
            "@value": true
          }
        ]
      },
      {
        "@id": "http://www.w3.org/ns/shacl#ValidationReport"
      }
    ]
    """
    g1 = Graph().parse(data=body, format="application/ld+json")
    g2 = Graph().parse(data=src, format="application/ld+json")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic, "results_graph is incorrect"


@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_file_content_type_json_ld(http_service: Any) -> None:
    """Should return OK and successful validation."""
    url = f"{http_service}/validator"
    filename = "tests/files/catalog_1.json"

    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(
            open(filename, "rb"), {"CONTENT-TYPE": "application/ld+json"}
        )
        p.set_content_disposition("attachment", name="file", filename=filename)

    session = ClientSession()
    async with session.post(url, data=mpwriter) as resp:
        body = await resp.text()
    await session.close()

    assert resp.status == 200
    assert "text/turtle" in resp.headers[hdrs.CONTENT_TYPE]

    # results_graph (validation report) should be isomorphic to the following:
    src = """
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    [] a sh:ValidationReport ;
         sh:conforms true
         .
    """
    g1 = Graph().parse(data=body, format="text/turtle")
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic, "results_graph is incorrect"


@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_url(http_service: Any) -> None:
    """Should return OK and successful validation."""
    url = f"{http_service}/validator"

    url_to_graph = "https://raw.githubusercontent.com/Informasjonsforvaltning/dcat-ap-no-validator-service/main/tests/files/catalog_1.ttl"  # noqa: B950
    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(url_to_graph)
        p.set_content_disposition("inline", name="url")

    session = ClientSession()
    async with session.post(url, data=mpwriter) as resp:
        body = await resp.text()
    await session.close()

    assert resp.status == 200
    assert "text/turtle" in resp.headers[hdrs.CONTENT_TYPE]

    # results_graph (validation report) should be isomorphic to the following:
    src = """
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    [] a sh:ValidationReport ;
         sh:conforms true
         .
    """

    g1 = Graph().parse(data=body, format="text/turtle")
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic, "results_graph is incorrect"


@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_with_file_content_encoding(http_service: Any) -> None:
    """Should return OK and successful validation."""
    url = f"{http_service}/validator"
    filename = "tests/files/catalog_1.ttl"

    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(open(filename, "rb"))
        p.set_content_disposition("attachment", name="file", filename=filename)
        p.headers[hdrs.CONTENT_ENCODING] = "gzip"

    session = ClientSession()
    async with session.post(url, data=mpwriter) as resp:
        body = await resp.text()
    await session.close()

    assert resp.status == 200
    assert "text/turtle" in resp.headers[hdrs.CONTENT_TYPE]

    # results_graph (validation report) should be isomorphic to the following:
    src = """
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    [] a sh:ValidationReport ;
         sh:conforms true
         .
    """
    g1 = Graph().parse(data=body, format="text/turtle")
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic, "results_graph is incorrect"


@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_with_minimal_file(http_service: Any) -> None:
    """Should return OK and unsuccessful validation."""
    url = f"{http_service}/validator"
    filename = "tests/files/catalog_1_minimal.ttl"

    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(open(filename, "rb"))
        p.set_content_disposition("attachment", name="file", filename=filename)

    session = ClientSession()
    async with session.post(url, data=mpwriter) as resp:
        body = await resp.text()
    await session.close()

    assert resp.status == 200
    assert "text/turtle" in resp.headers[hdrs.CONTENT_TYPE]

    # results_graph (validation report) should not be isomorphic to the following:
    src = """
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .

    [] a sh:ValidationReport ;
         sh:conforms true
         .
    """
    g1 = Graph().parse(data=body, format="text/turtle")
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert not _isomorphic, "results_graph is incorrect"


@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_with_not_valid_file(http_service: Any) -> None:
    """Should return OK and unsuccessful validation."""
    url = f"{http_service}/validator"
    filename = "tests/files/catalog_2_not_valid.ttl"
    version = "2"

    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(open(filename, "rb"))
        p.set_content_disposition("attachment", name="file", filename=filename)
        p = mpwriter.append(version)
        p.set_content_disposition("inline", name="version")

    session = ClientSession()
    async with session.post(url, data=mpwriter) as resp:
        body = await resp.text()
    await session.close()

    assert resp.status == 200
    assert "text/turtle" in resp.headers[hdrs.CONTENT_TYPE]

    # results_graph (validation report) should be isomorphic to the following:
    src = """
    @prefix sh: <http://www.w3.org/ns/shacl#> .
    @prefix xsd: <http://www.w3.org/2001/XMLSchema#> .
    [] a sh:ValidationReport ;
         sh:conforms false ;
         sh:result [ a sh:ValidationResult ;
                sh:focusNode <http://dataset-publisher:8080/datasets/1> ;
                sh:resultMessage "Less than 1 values on <http://dataset-publisher:8080/datasets/1>->dct:description" ;
                sh:resultPath <http://purl.org/dc/terms/description> ;
                sh:resultSeverity sh:Violation ;
                sh:sourceConstraintComponent sh:MinCountConstraintComponent ;
                sh:sourceShape [ sh:minCount 1 ;
                        sh:nodeKind sh:Literal ;
                        sh:path <http://purl.org/dc/terms/description> ;
                        sh:severity sh:Violation ] ],
            [ a sh:ValidationResult ;
                sh:focusNode <http://dataset-publisher:8080/catalogs/1> ;
                sh:resultMessage "Value does not have class foaf:Agent" ;
                sh:resultPath <http://purl.org/dc/terms/publisher> ;
                sh:resultSeverity sh:Violation ;
                sh:sourceConstraintComponent sh:ClassConstraintComponent ;
                sh:sourceShape [ sh:class <http://xmlns.com/foaf/0.1/Agent> ;
                        sh:maxCount 1 ;
                        sh:minCount 1 ;
                        sh:path <http://purl.org/dc/terms/publisher> ;
                        sh:severity sh:Violation ] ;
                sh:value <https://organization-catalogue.fellesdatakatalog.digdir.no/organizations/961181399> ]
    .
    """
    g1 = Graph().parse(data=body, format="text/turtle")
    g2 = Graph().parse(data=src, format="text/turtle")

    _isomorphic = isomorphic(g1, g2)
    if not _isomorphic:
        _dump_diff(g1, g2)
        pass
    assert _isomorphic, "results_graph is incorrect"


# --- bad cases ---
@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_notexisting_url(http_service: Any) -> None:
    """Should return 400."""
    url = f"{http_service}/validator"

    url_to_graph = "https://raw.githubusercontent.com/Informasjonsforvaltning/dcat-ap-no-validator-service/main/tests/files/does_not_exist.ttl"  # noqa: B950
    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(url_to_graph)
        p.set_content_disposition("inline", name="url")

    session = ClientSession()
    async with session.post(url, data=mpwriter) as resp:
        _ = await resp.text()
    await session.close()

    assert resp.status == 400


@pytest.mark.contract
@pytest.mark.asyncio
async def test_validator_url_to_invalid_rdf(http_service: Any) -> None:
    """Should return 400."""
    url = f"{http_service}/validator"

    url_to_graph = "https://raw.githubusercontent.com/Informasjonsforvaltning/dcat-ap-no-validator-service/main/tests/files/invalid_rdf.txt"  # noqa: B950
    with MultipartWriter("mixed") as mpwriter:
        p = mpwriter.append(url_to_graph)
        p.set_content_disposition("inline", name="url")

    session = ClientSession()
    async with session.post(url, data=mpwriter) as resp:
        _ = await resp.text()
    await session.close()

    assert resp.status == 400


# ---------------------------------------------------------------------- #
# Utils for displaying debug information


def _dump_diff(g1: Graph, g2: Graph) -> None:
    in_both, in_first, in_second = graph_diff(g1, g2)
    print("\nin both:")
    _dump_turtle(in_both)
    print("\nin first:")
    _dump_turtle(in_first)
    print("\nin second:")
    _dump_turtle(in_second)


def _dump_turtle(g: Graph) -> None:
    for _l in g.serialize(format="text/turtle").splitlines():
        if _l:
            print(_l.decode())
