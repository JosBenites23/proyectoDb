from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session, selectinload
from client import get_db
from dataBase.modelDep import Dep, Link
from dataBase.schemaDep import DepartamentoSchema, DepartamentoCard, LinkSchema
from fastapi import UploadFile, File, Form
from typing import Optional, List
from slugify import slugify

router = APIRouter(prefix="/departamento", tags=["Departamentos"])

@router.post("/", response_model=DepartamentoSchema)
async def crear_departamento(
    titulo: str = Form(..., max_length=500),
    descripcion: str = Form(..., max_length=500),
    imagen: UploadFile = File(...),
    titulo_link: Optional[str] = Form(None),
    link_file: Optional[UploadFile] = File(None),
    link_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    try:
        existing_dep = db.query(Dep).filter(Dep.titulo == titulo).first()
        if existing_dep:
            raise HTTPException(status_code=400, detail="Ya existe un departamento con ese nombre.")

        # Guardar imagen principal
        upload_dir = "uploads"
        file_location = f"{upload_dir}/{imagen.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(imagen.file.read())

        url_contenido = f"http://9.0.1.247:8081/uploads/{imagen.filename}"

        # Crear el departamento
        nuevo_dep = Dep(
            titulo=titulo,
            descripcion=descripcion,
            imagen=url_contenido,
            slug=slugify(titulo)
        )
        db.add(nuevo_dep)
        db.commit()
        db.refresh(nuevo_dep)

        # Crear el link solo si hay título y uno de los dos tipos de link
        if titulo_link and (link_file or link_url):
            if link_file:
                file_location = f"{upload_dir}/{link_file.filename}"
                with open(file_location, "wb+") as file_object:
                    file_object.write(link_file.file.read())

                url_file = f"http://9.0.1.247:8081/uploads/{link_file.filename}"
                nuevo_link = Link(
                    titulo_link=titulo_link,
                    url=url_file,
                    dep_id=nuevo_dep.id
                )
                db.add(nuevo_link)

            elif link_url:
                nuevo_link = Link(
                    titulo_link=titulo_link,
                    url=link_url,
                    dep_id=nuevo_dep.id
                )
                db.add(nuevo_link)

        db.commit()

        # Recargar el departamento con sus links
        dep_con_links = db.query(Dep).options(selectinload(Dep.links)).filter(Dep.id == nuevo_dep.id).first()
        return dep_con_links

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"No se pudo crear el departamento: {str(e)}")

@router.get("/cards", response_model=List[DepartamentoCard])
def obtener_departamentos_cards(db: Session = Depends(get_db)):
    departamentos = db.query(Dep).order_by(Dep.fecha_creacion.desc()).all()
    return departamentos

@router.get("/page-dep/{slug}", response_model=DepartamentoSchema)
def obtener_departamento_por_slug(slug: str, db: Session = Depends(get_db)):
    departamento = db.query(Dep).filter(Dep.slug == slug).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    return departamento


@router.delete("/eliminar-dep/{id}", response_model=DepartamentoSchema)
def eliminar_departamento(id: int, db: Session = Depends(get_db)):
    departamento = db.query(Dep).filter(Dep.id == id).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

    db.delete(departamento)
    db.commit()
    return departamento

@router.get("/id/{id}", response_model=DepartamentoSchema)
def obtener_departamento_por_id(id: int, db: Session = Depends(get_db)):
    departamento = db.query(Dep).filter(Dep.id == id).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")
    return departamento

@router.post("/{dep_id}/agregar-link", response_model=DepartamentoSchema)
async def agregar_links_a_departamento(
    dep_id: int,
    titulo_link: str=Form(..., max_legnth=500),
    link_file: Optional[UploadFile] = File(None),
    link_url: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    departamento = db.query(Dep).filter(Dep.id == dep_id).first()
    if not departamento:
        raise HTTPException(status_code=404, detail="Departamento no encontrado")

    upload_dir = "uploads"

    if link_file:
        file_location = f"{upload_dir}/{link_file.filename}"
        with open(file_location, "wb+") as file_object:
            file_object.write(link_file.file.read())

        url_file = f"http://9.0.1.247:8081/uploads/{link_file.filename}"
        nuevo_link = Link(
            titulo_link=titulo_link,
            url=url_file,
            dep_id=dep_id
        )
        db.add(nuevo_link)

    if link_url:
        nuevo_link = Link(
            titulo_link=titulo_link,
            url=link_url,
            dep_id=dep_id
        )
        db.add(nuevo_link)

    db.commit()
    db.refresh(departamento)
    return departamento

@router.delete("/link/{link_id}", response_model=LinkSchema)
def eliminar_link(link_id: int, db: Session = Depends(get_db)):
    link = db.query(Link).filter(Link.id == link_id).first()
    if not link:
        raise HTTPException(status_code=404, detail="Link no encontrado")

    db.delete(link)
    db.commit()
    return link

