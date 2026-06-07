import asyncio
import random
from sqlalchemy import create_engine, Column, Integer, String, select

from sqlalchemy.orm import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

Base = declarative_base()

class Node(Base):
    __tablename__ = 'nodes'

    id = Column(Integer, primary_key=True)
    ip_address = Column(String, nullable=False)
    status = Column(String, default='offline')

engine = create_async_engine('sqlite+aiosqlite:///network2.db', echo=False)
AsyncSessionLocal = async_sessionmaker(engine, expire_on_commit=False)


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)



async def get_all_nodes(session):
        stmt = select(Node)
        result = await session.execute(stmt)
        nodes = result.scalars().all()
        return list(nodes)

async def ping_node(node):
    delay = random.uniform(0.5, 2.5)
    await asyncio.sleep(delay)

    new_status = random.choices(
        ['online', 'offline', 'maintenance'],
        weights=[70, 20, 10]
    )[0]

    print(f"[ID: {node.id}] IP {node.ip_address} відповів за {delay:.2f}с -> {new_status.upper()}")

    return node, new_status


async def collect_all_statuses(nodes):
    print("\nПочинаємо асинхронне опитування мережі...")
    tasks = [ping_node(node) for node in nodes]

    results = await asyncio.gather(*tasks)

    print("Опитування завершено!")
    return results



async def main():
        await init_models()

        async with AsyncSessionLocal() as session:

            nodes_list = await get_all_nodes(session)
            if not nodes_list:
                print("База порожня. Створюємо тестові мережеві вузли...")
                test_ips = [f"192.168.1. {100 + i}" for i in range(1,16)]

                for ip in test_ips:
                    new_node = Node(ip_address=ip)
                    session.add(new_node)

                await session.commit()

                nodes_list = await get_all_nodes()

            new_statuses = await collect_all_statuses(nodes_list)

            print("\n Оновлюємо дані в базі...")
            for node, status in new_statuses:
                node.status = status

            await session.commit()
            print(" Всі статуси успішно оновлено в базі даних!")

        print("\n Перевірка збережених даних з бази (ПІСЛЯ оновлення):")
        saved_nodes = await get_all_nodes(session)
        for n in saved_nodes:
            print(f"База підтверджує: [ID: {n.id}] {n.ip_address} -> {n.status.upper()}")


if __name__ == "__main__":
    asyncio.run(main())


 # if __name__ == "__main__":
    #     asyncio.run(main())

# Base.metadata.create_all(engine)


# nodes = Node
# nod = nodes.query(Node).all()
# for node in nodes:
#     print(node.id, node.ip, node.status)