import string
from pydantic import BaseModel, constr


class ProfessionalAd(BaseModel):
    id: int | None
    min_salary: float
    max_salary: float
    description: str
    remote: bool
    professional_id: int | None
    city_id: int | None
    ad_state_id: int

    @classmethod
    def from_query_result(cls, id: int | None, min_salary: float, max_salary:float, description: string, remote: bool, professional_id: int | None, city_id: int | None, ad_state_id: int):
        return cls(id = id, min_salary = min_salary, max_salary = max_salary, description = description, remote = remote, professional_id = professional_id, city_id = city_id, ad_state_id = ad_state_id)

class Level(BaseModel):
    id: int | None
    level_name: str

    @classmethod
    def from_query_result(cls, id: int | None, level_name: str):
        return cls(id = id, level_name = level_name)

class Skill(BaseModel):
    id: int | None
    name: str
    category_id: int

    @classmethod
    def from_query_result(cls, id: int | None, name: str, category_id: int):
        return cls(id = id, name = name, category_id = category_id)

class Skillset(BaseModel):
    ad_id: int | None
    skill_id: int
    level_id: int

    @classmethod
    def from_query_result(cls, ad_id: int | None, skill_id: int, level_id: int):
        return cls(ad_id = ad_id, skill_id = skill_id, level_id = level_id)

class SkillResponse(BaseModel):
    id: int | None
    name: str
    level: list[Level] = []

    @classmethod
    def from_query_result(cls, id: int | None, name: str):
        return cls(id = id, name = name)

class AdSkillsetResponse(BaseModel):
    category_name: str
    skillset: list[SkillResponse] = []

    @classmethod
    def from_query_result(cls, category_name: str):
        return cls(category_name=category_name)

class ProfessionalAdResponse(BaseModel):
    id: int | None
    min_salary: float
    max_salary: float
    description: str
    remote: bool
    status: str
    city_name: str | None
    professional_first_name: str
    professional_last_name: str
    skillset: list[AdSkillsetResponse] = []

    @classmethod
    def from_query_result(cls, id: int, min_salary: float, max_salary:float, description: string, remote: bool, status: str, 
                            city_name: str | None, professional_first_name: str, professional_last_name: str):
        return cls(id = id, min_salary = min_salary, max_salary = max_salary, description = description, remote = remote, 
                    status = status, city_name = city_name, professional_first_name = professional_first_name, 
                    professional_last_name = professional_last_name)


class AdState(BaseModel):
    id: int | None
    name: str

    @classmethod
    def from_query_result(cls, id: int, name: str):
        return cls(id = id, name=name)

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
    name: str | None

    @classmethod
    def from_query_result(cls, id: int, name: str):
        return cls(id = id, name = name)

class ContactsCreationData(BaseModel):
    phone_number: str 
    email: str
    website: str | None
    linkedin: str | None
    facebook: str | None
    twitter: str | None
    user_id: int | None

class Contacts(BaseModel):
    id: int
    phone_number: str
    email: str
    website: str | None
    linkedin: str | None
    facebook: str | None
    twitter: str | None
    user_id: int

    @classmethod
    def from_query_result(cls, id: int, phone_number: str, email: str, website: str, linkedin: str, facebook: str, twitter: str, user_id: int):
        return cls(
            id = id,
            phone_number = phone_number,
            email = email,
            website = website,
            linkedin = linkedin,
            facebook = facebook,
            twitter = twitter,
            user_id = user_id)

class ContactsResponse(BaseModel):
    phone_number: str
    email: str
    website: str | None
    linkedin: str | None
    facebook: str | None
    twitter: str | None

class JobAd(BaseModel):
    id: int | None
    min_salary: int
    max_salary: int
    description: str
    remote: bool
    status: bool
    company_id: int | None
    city_id: int | None
    

    @classmethod 
    def from_query_result(cls, id: int, min_salary: int, max_salary: int, description: str, remote: bool, status: int, company_id: int, city_id: int):
        return cls(id = id, min_salary = min_salary, max_salary = max_salary, description = description, remote = remote, status = status, company_id = company_id, city_id = city_id)


class JobAdResponse(BaseModel):
    id:int
    min_salary: int
    max_salary: int
    description: str
    remote: str
    status: str
    company: str
    location: str | None
    skill_set: list

class ConfirmedMatchResponse(BaseModel):
    id: int
    company_id: int | None
    company_name: str | None
    professional_id: int | None
    professional_name: str | None

class CompanyResponse(BaseModel):
    id: int
    name: str
    info: str
    location: str
    contacts: ContactsResponse | None
    active_ads_num: int
    active_ads_list: list[JobAdResponse]
    successfull_matches: int

class ProfessionalResponse(BaseModel):
    id: int
    fullname: str
    info: str | None
    status: str
    location: str
    contacts: ContactsResponse | None
    active_ads_num: int
    active_ads_list: list[ProfessionalAdResponse]
    hide_matches: bool
    successfull_matches: list[ConfirmedMatchResponse] | None

class MatchRequestResponse(BaseModel):
    id: int | None
    ad: ProfessionalAdResponse | JobAdResponse
    user: CompanyResponse | ProfessionalResponse

class SkillCategory(BaseModel):
    id: int | None
    name: str

class AdminApprovals(BaseModel):
    id: int | None
    type: str
    name: str
    category_id: int | None

    @classmethod
    def from_query_result(cls, id: int, type: str, name: str, category_id: int | None):
        return cls(id = id, type = type, name = name, category_id = category_id)

class SearchResult(BaseModel):
    ad_id: int
    min_salary: int
    max_salary: int
    description: str
    remote: int
    city_id: int | None
    city_name: str | None
    skill_id: int | None
    skill_name: str | None
    skill_level_id: int | None
    skill_level_name: str | None
    skill_category_id: int | None
    skill_category_name: str | None
    owner_id: str
    owner_name: str 
    owner_info: str
    contacts_id: int | None
    phone_number: str | None
    email: str | None
    website: str | None
    linkedin: str | None
    facebook: str | None
    twitter: str | None

    @classmethod
    def from_query_result(cls, ad_id: int, min_salary: int, max_salary: int, description: str, remote: int, city_id: int | None,
    city_name: str | None, skill_id: int | None, skill_name: str | None, skill_level_id: int | None, skill_level_name: str | None, 
    skill_category_id: int | None, skill_category_name: str | None, owner_id: str, owner_name: str, owner_info: str, contacts_id: int | None,
    phone_number: str | None, email: str | None, website: str | None, linkedin: str | None, facebook: str | None, twitter: str | None):
        return cls(ad_id=ad_id, min_salary=min_salary, max_salary=max_salary, description=description, remote=remote, city_id=city_id,
        city_name=city_name, skill_id=skill_id, skill_name=skill_name, skill_level_id=skill_level_id, skill_level_name=skill_level_name,
        skill_category_id=skill_category_id, skill_category_name=skill_category_name, owner_id=owner_id, owner_name=owner_name, owner_info=owner_info,
        contacts_id=contacts_id, phone_number=phone_number, email=email, website=website, linkedin=linkedin, facebook=facebook, twitter=twitter)

class SearchResultSkillResponse(BaseModel):
    skill_name: str | None
    skill_level_name: str | None

    def __eq__(self, other):
        return (self.skill_name == other.skill_name and self.skill_level_name == other.skill_level_name)

class SearchResultSkillsetResponse(BaseModel):
    category_id: int | None
    category_name: str | None
    skills_in_category: list[SearchResultSkillResponse] = []

    def __eq__(self, other):
        if self is None and other is None:
            return True
        elif self is None and other is not None:
            return False
        elif self is not None and other is None:
            return False
        else:
            return (self.category_id == other.category_id and self.category_name == other.category_name
                    and self.skills_in_category == other.skills_in_category
                    and len(self.skills_in_category) == len(other.skills_in_category))  

class SearchResponse(BaseModel):
    ad_id: int
    min_salary: float
    max_salary: float
    skillset: list[SearchResultSkillsetResponse] = []
    description: str
    remote: bool
    location: Location | None
    ad_owner_id: int
    ad_owner_name: str
    ad_owner_info: str
    ad_owner_contacts: ContactsResponse | None

    def __eq__(self, other):
        return (self.ad_id == other.ad_id and
                self.min_salary == other.min_salary and
                self.max_salary == other.max_salary and
                len(self.skillset) == len(other.skillset) and
                self.skillset == other.skillset and
                self.description == other.description and
                self.remote == other.remote and
                self.location == other.location and
                self.ad_owner_id == other.ad_owner_id and
                self.ad_owner_name and other.ad_owner_name and
                self.ad_owner_info and other.ad_owner_info and
                self.ad_owner_contacts and other.ad_owner_contacts)

    def __lt__(self, other):
        return (self.ad_id < other.ad_id)

    def __le__(self, other):
        return (self.ad_id <= other.ad_id)

class ApprovalType:
    SKILL = 'skill'
    SKILL_CATEGORY = 'category'
    CITY = 'city'

class DBTable:
    ADMINS = 'admins'
    COMPANIES = 'companies'
    PROFESSIONALS = 'professionals'
    PROFESSIONAL_CONTACTS = 'professional_contacts'
    COMPANY_CONTACTS = 'company_contacts'
    PROFESSIONAL_ADS = 'professional_ads'
    JOB_ADS = 'job_ads'
    PROFESSIONAL_ADS_SKILLSETS = 'professional_ads_skillsets'
    JOB_ADS_SKILLSETS = 'job_ads_skillsets'
    JOB_ADS_MATCH_REQUESTS = 'job_ads_match_requests'
    PROFESSIONAL_ADS_MATCH_REQUESTS = 'professional_ads_match_requests'
        
class DBColumn:
    PROFESSIONAL_AD_ID = 'professional_ad_id'
    JOB_AD_ID = 'job_ad_id'
    JOB_AD = 'job_ad'
    PROFESSIONAL_AD = 'professional_ad'
    JOB_AD_STATE_COLUMN = 'status'
    PROFESSIONAL_AD_STATE_COLUMN = 'ad_state_id'
    COMPANY_NAME_COLUMN_FOR_SEARCH = 'O.name'
    PROFESSIONAL_NAME_COLUMN_FOR_SEARCH = 'concat(O.first_name, \' \', O.last_name) AS name'
    COMPANY = 'company'
    PROFESSIONAL = 'professional'

class DBAdStates:
    ACTIVE = 'active'
    HIDDEN = 'hidden'
    PRIVATE = 'private'
    MATCHED = 'matched'
    ARCHIVED = 'archived'
