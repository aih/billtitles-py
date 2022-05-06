from typing import List, Optional

from sqlalchemy.sql.sqltypes import ARRAY, String
from sqlmodel import Field, SQLModel, Column


class Status(SQLModel):
    success: bool
    message: str


class BillPath(SQLModel):
    billnumber_version: str = ""
    filePath: str = ""
    fileName: str = ""


class SectionMeta(SQLModel):
    billnumber_version: Optional[str] = None
    section_id: Optional[str] = None
    label: Optional[str] = None
    header: Optional[str] = None
    length: Optional[int] = None


class SimilarSection(SectionMeta):
    score_es: Optional[float] = None
    score: Optional[float] = None
    score_to: Optional[float] = None


class Section(SectionMeta):
    similar_sections: List[SimilarSection]


# This is the basis for making queries, using billsim.bill_similarity.py getSimilarSectionItem
class QuerySection(SectionMeta):
    query_text: str


# Result of the similarity search, collecting top similar sections for each section of the bill
class BillSections(SQLModel):
    billnumber_version: str
    length: int
    sections: List[Section]


class SimilarSectionHit(SQLModel):
    billnumber_version: str  # from _source.id
    score: float  # from _score


class BillToBillModel(SQLModel):
    bill_id: Optional[int] = Field(
        default=None, foreign_key="bill.id", primary_key=True
    )
    bill_to_id: Optional[int] = Field(
        default=None, foreign_key="bill.id", primary_key=True
    )
    billnumber_version: str = Field(index=True)
    billnumber_version_to: str = Field(index=True)
    billnumber: Optional[str] = Field(index=True)
    version: Optional[str] = Field(index=True)
    billnumber_to: Optional[str] = Field(index=True)
    version_to: Optional[str] = Field(index=True)
    titles: Optional[dict] = None
    titles_to: Optional[dict] = None
    title: Optional[str] = None
    title_to: Optional[str] = None
    length: Optional[int] = None
    length_to: Optional[int] = None
    score_es: Optional[float] = None
    score: Optional[float] = None
    score_to: Optional[float] = None
    reasons: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(String)))
    identified_by: Optional[str] = None
    sections_num: Optional[int] = None
    sections_match: Optional[int] = None
    sections: Optional[
        List[Section]
    ] = None  # for BillToBill, the Section.sections has just the highest scoring similar section between the bills


class BillModelDeep(SQLModel):
    bill_id: Optional[int] = Field(
        default=None, foreign_key="bill.id", primary_key=True
    )
    billnumber_version: Optional[str] = Field(index=True)
    billnumber: Optional[str] = Field(index=True)
    version: Optional[str] = Field(index=True)
    titles: Optional[dict] = None
    title: Optional[str] = None
    length: Optional[int] = None
    score_es: Optional[float] = None
    score: Optional[float] = None
    score_to: Optional[float] = None
    reasons: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(String)))
    identified_by: Optional[str] = None
    sections_num: Optional[int] = None
    sections_match: Optional[int] = None
    sections: Optional[List[Section]] = None  #


class BillToBillModelDeep(SQLModel):
    bill: BillModelDeep
    bill_to: BillModelDeep
    reasons: Optional[List[str]] = Field(default=None, sa_column=Column(ARRAY(String)))
    identified_by: Optional[str] = None
    sections_num: Optional[int] = None
    sections_match: Optional[int] = None
    sections: Optional[
        List[Section]
    ] = None  # for BillToBill, the Section.sections has just the highest scoring similar section between the bills


# For display (from billtitles-py)
class BillTitlePlus(SQLModel):
    id: Optional[int] = Field(default=None, primary_key=True)
    billnumber: str = Field(index=True)
    titles: str
    is_for_whole_bill: bool = Field(default=False)


class TitlesItem(SQLModel):
    whole: List[str]
    all: List[str]


class BillTitleResponse(SQLModel):
    billnumber: str
    titles: TitlesItem


class TitleBillsResponseItem(SQLModel):
    id: int
    title: str
    billnumbers: List[str]


class TitleBillsResponse(SQLModel):
    titles: List[TitleBillsResponseItem]
    titles_whole: List[TitleBillsResponseItem]