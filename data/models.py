import string
from pydantic import BaseModel, constr


class ProfessionalAd(BaseModel):
    id: int | None
    min_salary: float
    max_salary: float
    description: str
    remote: bool
    status: int
    professional_id: int
    city_id: int

    @classmethod
    def from_query_result(cls, id: int, min_salary: float, max_salary:float, description: string, remote: bool, status: int, professional_id: int, city_id: int):
        return cls(id = id, min_salary = min_salary, max_salary = max_salary, description = description, remote = remote, status = status, professional_id = professional_id, city_id = city_id)

class Skill(BaseModel):
    id: int | None
    name: str
    level: str
    category_id: int

class SkillResponse(BaseModel):
    name: str
    level: str

class CategorySkillset(BaseModel):
    category_name: str
    skillset: list[SkillResponse] = []


TUsername = constr(regex='^\w{2,30}$')

class UserType:
    COMPANY = 'company'
    PROFESSIONAL = 'professional'
    ADMIN = 'admin'

class Admin(BaseModel):
    id: int | None
    username: TUsername
    password: str

    @classmethod
    def from_query_result(cls, id: int, username: str, password: str):
        return cls(id = id, username = username, password = password)

class Company(BaseModel):
    id: int | None
    username: TUsername
    password: str
    name: str
    info: str
    city_id: int

    @classmethod
    def from_query_result(cls, id: int, username: str, password: str, name: str, info: str, city_id: int):
        return cls(id = id, username = username, password = password, name = name, info = info, city_id=city_id)

class CompanyResponse(BaseModel):
    id: int
    name: str
    info: str
    location: str
    active_ads: int
    matched_ads: int

class ProfessionalMatchVisibility:
    VISIBLE = 'visible'
    HIDDEN = 'hidden'

class ProfessionalStatus:
    ACTIVE = 'active'
    BUSY = 'busy'

class Professional(BaseModel):
    id: int | None
    username: TUsername
    password: str
    first_name: str
    last_name: str
    info: str | None
    status: int = 0
    city_id: int
    main_ad: int | None
    hide_matches: int = 0

    @classmethod
    def from_query_result(cls, id: int, username: str, password: str, first_name: str, last_name: str,
                            info: str | None, status: int, city_id: int, main_ad: int | None, hide_matches: int):
        return cls(
            id = id,
            username = username,
            password = password,
            first_name = first_name,
            last_name = last_name,
            info = info,
            status = status,
            city_id = city_id,
            main_ad = main_ad,
            hide_matches = hide_matches)

class ProfessionalResponse(BaseModel):
    id: int
    fullname: str
    info: str
    status: str
    location: str
    active_ads: int
    match_visability: str
    matched_ads: list[ProfessionalAd] | None

class LoginData(BaseModel):
    username: TUsername
    password: str

class AdminRegisterData(BaseModel):
    username: TUsername
    password: str

class CompanyRegisterData(BaseModel):
    username: TUsername
    password: str
    name: str
    info: str
    location: str

class ProfessionalRegisterData(BaseModel):
    username: TUsername
    password: str
    first_name: str
    last_name: str
    info: str | None
    location: str

class Location(BaseModel):
    id: int | None
    name: str

    @classmethod
    def from_query_result(cls, id: int, name: str):
        return cls(id = id, name = name)
