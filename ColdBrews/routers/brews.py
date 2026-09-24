from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from database import get_db
from models import Brew, BrewCreate, BrewRead, BrewUpdate

router = APIRouter(prefix="/brews", tags=["brews"])


def _get_or_404(db: Session, brew_id: int) -> Brew:
    brew = db.get(Brew, brew_id)
    if brew is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"Brew {brew_id} not found")
    return brew


def _commit(db: Session) -> None:
    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status.HTTP_409_CONFLICT, "A brew with that name already exists")


@router.get("", response_model=list[BrewRead])
def list_brews(db: Session = Depends(get_db)):
    return db.scalars(select(Brew).order_by(Brew.id)).all()


@router.post("", response_model=BrewRead, status_code=status.HTTP_201_CREATED)
def create_brew(payload: BrewCreate, db: Session = Depends(get_db)):
    brew = Brew(**payload.model_dump())
    db.add(brew)
    _commit(db)
    db.refresh(brew)
    return brew


@router.get("/{brew_id}", response_model=BrewRead)
def get_brew(brew_id: int, db: Session = Depends(get_db)):
    return _get_or_404(db, brew_id)


@router.patch("/{brew_id}", response_model=BrewRead)
def update_brew(brew_id: int, payload: BrewUpdate, db: Session = Depends(get_db)):
    brew = _get_or_404(db, brew_id)
    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(brew, field, value)
    _commit(db)
    db.refresh(brew)
    return brew


@router.delete("/{brew_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_brew(brew_id: int, db: Session = Depends(get_db)):
    db.delete(_get_or_404(db, brew_id))
    db.commit()
