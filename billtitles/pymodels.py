#!/usr/bin/env python3
# Keep in sync with billsim

from sqlalchemy.sql.schema import UniqueConstraint
from sqlalchemy.sql.sqltypes import VARCHAR
from sqlmodel import Field, SQLModel, Column
from typing import List, Optional

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
    similar_sections: list[SimilarSection]


class Bill(SQLModel, table=True):
    __table_args__ = (UniqueConstraint('billnumber',
                                       'version',
                                       name='billnumber_version'),)
    id: Optional[int] = Field(default=None, primary_key=True)
    length: Optional[int] = None
    # TODO: when indexing/storing Bill initially, calculate number of sections
    #sections_num: Optional[int] = None
    billnumber: str
    version: str

    @classmethod
    def getBillnumberversion(cls):
        return "{cls.billnumber}{cls.version}".format(cls=cls)


class BillToBillModel(SQLModel):
    bill_id: Optional[int] = Field(default=None,
                                   foreign_key="bill.id",
                                   primary_key=True)
    bill_to_id: Optional[int] = Field(default=None,
                                      foreign_key="bill.id",
                                      primary_key=True)
    billnumber_version: str
    length: Optional[int] = None
    billnumber_version_to: str
    score_es: Optional[float] = None
    score: Optional[float] = None
    score_to: Optional[float] = None
    #reasons: Optional[List[str]] = Field(default=None,
    #                                     sa_column=Column(ARRAY(String)))
    reasonsstring: Optional[str] = Field(default=None,
                                         sa_column=Column(VARCHAR(100)))
    identified_by: Optional[str] = None
    sections_num: Optional[int] = None
    sections_match: Optional[int] = None
    sections: Optional[list[
        Section]] = None    # for BillToBill, the Section.sections has just the highest scoring similar section between the bills


# Model used to store in db
class BillToBill(SQLModel, table=True):
    bill_id: Optional[int] = Field(default=None,
                                   foreign_key="bill.id",
                                   primary_key=True)
    bill_to_id: Optional[int] = Field(default=None,
                                      foreign_key="bill.id",
                                      primary_key=True)
    score_es: Optional[float] = None
    score: Optional[float] = None
    score_to: Optional[float] = None
    #reasons: Optional[List[str]] = Field(default=None,
    #                                         sa_column=Column(ARRAY(String)))
    reasonsstring: Optional[str] = Field(default=None,
                                         sa_column=Column(VARCHAR(100)))
    identified_by: Optional[str] = None
    sections_num: Optional[int] = None
    sections_match: Optional[int] = None


# NOTE: section_id is the id attribute from the XML. It may not be unique.
# However, the SQL bill_id + section_id is unique.
class SectionItem(SQLModel, table=True):
    __table_args__ = (UniqueConstraint('bill_id',
                                       'section_id',
                                       name='billnumber_version_section_id'),)
    id: Optional[int] = Field(default=None, primary_key=True)
    bill_id: Optional[int] = Field(default=None, foreign_key="bill.id")
    section_id: Optional[str] = Field(default=None)
    label: Optional[str]
    header: Optional[str]
    length: int


class SectionToSection(SQLModel, table=True):
    """
    This is a self-join of the SectionItem table.
    """
    id: Optional[int] = Field(default=None,
                              foreign_key="sectionitem.id",
                              primary_key=True)
    id_to: Optional[int] = Field(default=None,
                                 foreign_key="sectionitem.id",
                                 primary_key=True)
    score_es: Optional[float] = None
    score: Optional[float] = None
    score_to: Optional[float] = None


