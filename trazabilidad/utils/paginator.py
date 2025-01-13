
class MongoPaginatorRepository:
    def __init__(self, collection):
        self.collection = collection

    async def paginate_query(
            self,
            query: dict,
            pipeline: list = None,
            page: int = 1,
            page_size: int = 10,
            order: str = None,
            direction: int = 1,
            fields: dict = None,
            add_fields: dict = None,
            group_by: dict = None
    ):
        if pipeline is None:
            pipeline = []

        offset = (page - 1) * page_size

        pipeline.append({"$match": query})

        if add_fields:
            pipeline.append(add_fields)

        if group_by:
            pipeline.append({"$group": group_by})

        if order:
            pipeline.append({"$sort": {order: direction}})

        pipeline.append({"$skip": offset})
        pipeline.append({"$limit": page_size})

        if fields:
            pipeline.append({"$project": fields})

        cursor = self.collection.aggregate(pipeline)
        items = await cursor.to_list(length=page_size)

        total = await self.collection.count_documents(query)

        return {
            "total": total,
            "page": page,
            "page_size": page_size,
            "items": items
        }
