"""
Factory classes for generating test data using factory_boy.
"""

from datetime import datetime, timedelta

import factory
from faker import Faker

fake = Faker()


class PaperUploadFactory(factory.Factory):
    """Factory for creating PaperUpload test data."""

    class Meta:
        model = dict  # Since we're using Pydantic models, we'll create dicts

    title = factory.LazyFunction(lambda: fake.sentence(nb_words=6).rstrip("."))
    authors = factory.LazyFunction(
        lambda: [fake.name() for _ in range(fake.random_int(1, 4))]
    )
    abstract = factory.LazyFunction(lambda: fake.text(max_nb_chars=500))
    file_url = factory.LazyFunction(lambda: fake.url())


class PaperResponseFactory(factory.Factory):
    """Factory for creating PaperResponse test data."""

    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    title = factory.LazyFunction(lambda: fake.sentence(nb_words=6).rstrip("."))
    authors = factory.LazyFunction(
        lambda: [fake.name() for _ in range(fake.random_int(1, 4))]
    )
    abstract = factory.LazyFunction(lambda: fake.text(max_nb_chars=500))
    upload_date = factory.LazyFunction(
        lambda: datetime.utcnow() - timedelta(days=fake.random_int(0, 365))
    )
    status = factory.Iterator(["processing", "completed", "failed", "pending"])


class QueryRequestFactory(factory.Factory):
    """Factory for creating QueryRequest test data."""

    class Meta:
        model = dict

    query = factory.LazyFunction(lambda: fake.sentence(nb_words=8))
    limit = factory.LazyFunction(lambda: fake.random_int(1, 50))


class QueryResponseFactory(factory.Factory):
    """Factory for creating QueryResponse test data."""

    class Meta:
        model = dict

    results = factory.LazyFunction(
        lambda: [
            {
                "id": fake.random_int(1, 1000),
                "title": fake.sentence(nb_words=6).rstrip("."),
                "score": fake.random.uniform(0.1, 1.0),
                "snippet": fake.text(max_nb_chars=200),
            }
            for _ in range(fake.random_int(0, 10))
        ]
    )
    total_results = factory.LazyAttribute(lambda obj: len(obj.results))
    query_time = factory.LazyFunction(lambda: fake.random.uniform(0.001, 2.0))


class UserFactory(factory.Factory):
    """Factory for creating User test data."""

    class Meta:
        model = dict

    id = factory.Sequence(lambda n: n + 1)
    email = factory.LazyFunction(lambda: fake.email())
    username = factory.LazyFunction(lambda: fake.user_name())
    full_name = factory.LazyFunction(lambda: fake.name())
    is_active = True
    created_at = factory.LazyFunction(
        lambda: datetime.utcnow() - timedelta(days=fake.random_int(0, 365))
    )


# Helper functions for common test scenarios
def create_sample_papers(count: int = 5) -> list[dict]:
    """Create a list of sample papers for testing."""
    return [PaperResponseFactory() for _ in range(count)]


def create_sample_query_results(query: str, count: int = 3) -> dict:
    """Create sample query results for testing."""
    return QueryResponseFactory(
        results=[
            {
                "id": fake.random_int(1, 1000),
                "title": fake.sentence(nb_words=6).rstrip("."),
                "score": fake.random.uniform(0.5, 1.0),
                "snippet": f"Sample snippet containing '{query}' for testing purposes.",
            }
            for _ in range(count)
        ]
    )
