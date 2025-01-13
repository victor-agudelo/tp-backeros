from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import func
from sqlalchemy.sql import Select


class PaginatorRepository:
    def __init__(self, db: AsyncSession):
        self.db = db

    async def paginate_query(self, query: Select, page: int = 1, page_size: int = 10):
        offset = (page - 1) * page_size

        paginated_query = query.limit(page_size).offset(offset)
        result = await self.db.execute(paginated_query)
        items = result.scalars().all()

        total_query = select(func.count()).select_from(query.subquery())
        total_result = await self.db.execute(total_query)
        total = total_result.scalar()

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }
