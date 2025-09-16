from enum import Enum

class GenderEnum(str, Enum):
    MALE = "М"
    FEMALE = "Ж"

class ParticipationStatusEnum(str, Enum):
    ACTIVE = "Активный"
    CLUB_ONLY = "В клубе, без промоушена"
    PROMOTION_ONLY = "В промоушене, без клуба"
    FREE_AGENT = "Свободный агент"
    UNDER_REVIEW = "На рассмотрении"

class VerificationStatusEnum(str, Enum):
    UNDER_REVIEW = "На проверке"
    VERIFIED = "Проверен"
    REJECTED = "Отклонён"

class ContractStatusEnum(str, Enum):
    UNDER_REVIEW = "На проверке"
    VERIFIED = "Верифицирован"
    REJECTED = "Отклонён"
    EXPIRED = "Истёк"
    EXHAUSTED = "Исчерпан"
    ABSENT = "Отсутствует"

class ApplicationStatusEnum(str, Enum):
    DRAFT = "Черновик"
    SUBMITTED = "Отправлена"
    UNDER_MATCHMAKER_REVIEW = "На проверке матчмейкера"
    APPROVED = "Утверждена"
    WAITING_LIST = "В листе ожидания"
    REJECTED = "Отклонена"
    CONFIRMED = "Подтверждена"
    BLOCKED = "Заблокирована"
    COMPLETED = "Завершена"
    NEEDS_CORRECTION = "Требует исправлений"
    WITHDRAWN = "Отозвана"
    OVERDUE = "Просрочена"

class FightResultEnum(str, Enum):
    WIN = "Победа"
    LOSS = "Поражение"
    DRAW = "Ничья"
    NO_CONTEST = "No Contest"

class FightMethodEnum(str, Enum):
    KO = "KO"
    SUBMISSION = "Submission" 
    TKO = "TKO"
    DECISION = "Decision"
    DQ = "DQ"

class EventTypeEnum(str, Enum):
    FIGHT = "Бой"
    TOURNAMENT = "Турнир"
    F2F = "F2F"
    SELECTION = "Selection"

class UserRoleEnum(str, Enum):
    FIGHTER = "Боец"
    TRAINER = "Тренер"
    MANAGER = "Менеджер"
    PROMOTION = "Промоушен"
    CLUB = "Клуб"
    MATCHMAKER = "Матчмейкер"
    ADMIN = "Админ"

class TaskStatusEnum(str, Enum):
    TODO = "К выполнению"
    IN_PROGRESS = "В работе"
    DONE = "Выполнено"
    OVERDUE = "Просрочено"