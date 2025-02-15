from typing import List, Dict, Optional

from fastapi import Depends, FastAPI, HTTPException
from fastapi.openapi.utils import get_openapi
from sqlalchemy.orm import Session
from sqlmodel import SQLModel

from . import crud, pymodels
from .database import SessionLocal, engine
from .version import __version__

BILL_VERSION_DEFAULT = '--'

SQLModel.metadata.create_all(engine)

# Run in uvicorn with:
# uvicorn billtitles.main:app --reload
app = FastAPI()


# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#@app.get("/bills/related", response_model=List[pymodels.BillToBillModel or pypymodels.BillToBillModelDeep])
#@app.get("/bills/related/{billnumber}", response_model=List[pymodels.BillToBillModel or pymodels.BillToBillModelDeep])
#@app.get("/bills/related/{billnumber}/{version}", response_model=List[pymodels.BillToBillModel or pymodels.BillToBillModelDeep])
@app.get("/bills/related")
@app.get("/bills/related/{billnumber}")
@app.get("/bills/related/{billnumber}/{version}")
def related_bills(billnumber: str,  version: Optional[str] = None, flat: Optional[bool] = True, billsonly: Optional[bool] = False, db: Session = Depends(get_db)):
    if version is None:
        version = BILL_VERSION_DEFAULT
    # TODO: get the latest version of the bill and get resuls from that
    db_bills = crud.get_related_bills(db, billnumber=billnumber, version=version, flat=flat, billsonly=billsonly)
    if db_bills is None:
        raise HTTPException(status_code=404, detail="Bills related to {billnumber} ({version}) not found".format(billnumber=billnumber, version=version))
    return db_bills

@app.get("/bills/titles/{billnumber}", response_model=pymodels.BillTitleResponse)
def read_bills(billnumber: str, db: Session = Depends(get_db)) -> pymodels.BillTitleResponse:
    db_bill = crud.get_bill_titles_by_billnumber(db, billnumber=billnumber)
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Bill {billnumber} not found".format(billnumber=billnumber))
    return db_bill

@app.post("/related/" )
def create_related(db: Session = Depends(get_db)):
    # TODO: Use POST data to create a new related bill
    if db is None:
        raise HTTPException(status_code=404, detail="Bill {billnumber} not found".format(billnumber=billnumber))
    return db

@app.get("/titles/{title_id}" )
def read_title(title_id: int, db: Session = Depends(get_db) ) -> pymodels.TitleBillsResponse:
    db_bill = crud.get_title_by_id(db, title_id=title_id)
    if db_bill is None:
        raise HTTPException(status_code=404, detail="Title with id {title_id} not found".format(title_id=title_id))
    return db_bill

# TODO This returns three different kind of responses depending on whether
# there is a title parameter, a title id parameter or neither (with skip & limit)
# Need to split these responses to different queries or return the same
# response type for all three 
@app.get("/titles/" )
def read_titles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db), title_id: int = None, title: str = None):
    if title_id is not None:
        return crud.get_title_by_id(db, title_id=title_id)
    elif title is not None:
        return crud.get_title(db, title=title)
    else:
        return crud.get_titles(db, skip=skip, limit=limit)

@app.post("/titles/" )
def add_title_to_db(title: str, billnumbers: List[str], db: Session = Depends(get_db), is_for_whole_bill: bool = False):
    return crud.add_title(db, title=title, billnumber=billnumbers, is_for_whole_bill=is_for_whole_bill)

@app.delete("/titles/" )
def remove_title_from_db(title: str, db: Session = Depends(get_db)):
    return crud.remove_title(db, title=title)

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="BillTitles API",
        version=__version__,
        description="API for related bills",
        routes=app.routes,
    )
    openapi_schema["info"]["x-logo"] = {
        "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    }
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi