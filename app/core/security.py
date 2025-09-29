from passlib.context import CryptContext

# Argon2id
pwd_context = CryptContext(
    schemes=["argon2"],
    deprecated="auto",
    argon2__type="ID",  # именно Argon2id
    argon2__rounds=3,  # сколько «проходов» (время)
    argon2__memory_cost=256 * 1024,  # память в КБ → 256 MB
    argon2__parallelism=2,  # количество потоков
)


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def needs_rehash(hashed: str) -> bool:
    # true для старых bcrypt-хэшей
    return pwd_context.needs_update(hashed)
