from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

class Tarea(BaseModel):
    titulo: str
    completada: bool

app = FastAPI()

datos = {
  "tareas": [
    {
      "id": 1,
      "titulo": "Aprender FastAPI",
      "completada": False
    },
    {
      "id": 2,
      "titulo": "Practicar Python",
      "completada": True
    }
  ]
}

@app.get('/')
def inicio():
    return datos

@app.post('/crear')
def crear(nueva_tarea: Tarea):
    
    ultimo_id = 0

    for tarea in datos['tareas']:
        ultimo_id = tarea['id']
        ultimo_id += 1

    tarea_nueva = { 
        "id": ultimo_id,
        "titulo": nueva_tarea.titulo, 
        "completada": nueva_tarea.completada
    }

    datos['tareas'].append(tarea_nueva)
    
    return {
        "mensaje": "Tarea creada con exito"
    }

@app.get('/consultar/{id}')
def consultar(id: int):
    for tarea in datos['tareas']:
        if id == tarea['id']:
            tarea_encontrada = {
                "id": id, 
                "titulo": tarea['titulo'], 
                "completada": tarea['completada']
            }

            return {
                "mensaje": "Tarea encontrada",
                "informacion": tarea_encontrada
            }
    
    raise HTTPException(
        status_code=404,
        detail="La tarea buscada no existe!!"
    )

@app.put('/editar/{id}')
def editar(id: int, editar_tarea: Tarea):
    for tarea in datos['tareas']:
        if id == tarea['id']:

            tarea['titulo'] = editar_tarea.titulo
            tarea['completada'] = editar_tarea.completada

            return {
                "mensaje": "Tarea actualizada con exito!!"
            }

    raise HTTPException(
        status_code=404,
        detail="La tarea buscada no existe!!"
    )

@app.delete('/eliminar/{id}')
def eliminar(id: int):
    for i, tarea in enumerate(datos['tareas']):
        if id == tarea['id']:
            datos['tareas'].pop(i)

            return {
                "Mensaje": "Tarea eliminada correctamente!!"
            }
    
    raise HTTPException(
        status_code=404,
        detail="La tarea buscada no existe!!"
    )    